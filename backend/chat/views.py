from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Message
from .serializers import MessageSerializer

from items.models import Item
from claims.models import Claim


class ChatView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, item_id):

        try:
            item = Item.objects.get(pk=item_id)
        except Item.DoesNotExist:
            return Response(
                {"message": "Item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Find the latest active/completed claim
        claim = Claim.objects.filter(
            item=item,
            status__in=[
                'PENDING',
                'APPROVED',
                'COMPLETED'
            ]
        ).order_by('-created_at').first()

        if not claim:
            return Response(
                {"message": "No conversation available"},
                status=status.HTTP_404_NOT_FOUND
            )

        reporter = item.reported_by
        claimant = claim.claimed_by

        # Only reporter or claimant can access
        if request.user not in [reporter, claimant]:
            return Response(
                {"message": "You are not allowed to access this chat"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Show only messages between these two users
        messages = Message.objects.filter(
            item=item,
            sender__in=[reporter, claimant],
            receiver__in=[reporter, claimant]
        ).order_by('created_at')

        serializer = MessageSerializer(
            messages,
            many=True
        )

        return Response(serializer.data)

    def post(self, request, item_id):

        try:
            item = Item.objects.get(pk=item_id)
        except Item.DoesNotExist:
            return Response(
                {"message": "Item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        message_text = request.data.get('message')

        if not message_text or not message_text.strip():
            return Response(
                {"message": "Message is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Find active claim
        claim = Claim.objects.filter(
            item=item,
            status__in=[
                'PENDING',
                'APPROVED'
            ]
        ).order_by('-created_at').first()

        if not claim:
            return Response(
                {"message": "No active claim found for this item"},
                status=status.HTTP_400_BAD_REQUEST
            )

        reporter = item.reported_by
        claimant = claim.claimed_by

        # Decide receiver
        if request.user == reporter:
            receiver = claimant

        elif request.user == claimant:
            receiver = reporter

        else:
            return Response(
                {"message": "You are not allowed to send messages in this chat"},
                status=status.HTTP_403_FORBIDDEN
            )

        message = Message.objects.create(
            item=item,
            sender=request.user,
            receiver=receiver,
            message=message_text.strip()
        )

        serializer = MessageSerializer(message)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class MyConversationsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        # Items reported by the current user
        reported_items = Item.objects.filter(
            reported_by=request.user
        )

        # Items where the current user has claimed
        claimed_item_ids = Claim.objects.filter(
            claimed_by=request.user
        ).values_list(
            'item_id',
            flat=True
        )

        claimed_items = Item.objects.filter(
            id__in=claimed_item_ids
        )

        # Combine both
        item_ids = set(
            reported_items.values_list('id', flat=True)
        )

        item_ids.update(
            claimed_items.values_list('id', flat=True)
        )

        conversations = []

        for item_id in item_ids:

            item = Item.objects.get(id=item_id)

            claim = Claim.objects.filter(
                item=item,
                status__in=[
                    'PENDING',
                    'APPROVED',
                    'COMPLETED'
                ]
            ).order_by('-created_at').first()

            if not claim:
                continue

            # Only include if current user is reporter or claimant
            if (
                item.reported_by != request.user
                and claim.claimed_by != request.user
            ):
                continue

            conversations.append({
                "item_id": item.id,
                "item_name": item.item_name,
                "item_type": item.item_type,
                "status": item.status,
                "claim_id": claim.id
            })

        return Response(conversations)