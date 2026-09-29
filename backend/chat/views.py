from datetime import timedelta

from django.utils import timezone
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Message
from .serializers import MessageSerializer

from items.models import Item
from claims.models import Claim


# ==========================================
# 1. CHAT BETWEEN REPORTER AND CLAIMANT
# ==========================================

class ChatView(APIView):

    permission_classes = [IsAuthenticated]

    # View messages
    def get(self, request, item_id):

        try:
            item = Item.objects.get(pk=item_id)

        except Item.DoesNotExist:
            return Response(
                {"message": "Item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Calculate the time 24 hours ago
        cutoff = timezone.now() - timedelta(hours=24)

        # Find the latest active claim or
        # a completed claim within 24 hours
        claim = Claim.objects.filter(
            item=item
        ).filter(
            Q(
                status__in=[
                    'PENDING',
                    'APPROVED'
                ]
            )
            |
            Q(
                status='COMPLETED',
                completed_at__gte=cutoff
            )
        ).order_by('-created_at').first()

        if not claim:
            return Response(
                {
                    "message":
                    "No conversation available"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        reporter = item.reported_by
        claimant = claim.claimed_by

        # Only the reporter or claimant can access
        if request.user not in [reporter, claimant]:
            return Response(
                {
                    "message":
                    "You are not allowed to access this chat"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # Get messages between these two users
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

    # Send a message
    def post(self, request, item_id):

        try:
            item = Item.objects.get(pk=item_id)

        except Item.DoesNotExist:
            return Response(
                {"message": "Item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        message_text = request.data.get('message')

        # Check that the message is not empty
        if not message_text or not message_text.strip():
            return Response(
                {
                    "message": "Message is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Find the latest active claim
        claim = Claim.objects.filter(
            item=item,
            status__in=[
                'PENDING',
                'APPROVED'
            ]
        ).order_by('-created_at').first()

        if not claim:
            return Response(
                {
                    "message":
                    "Item has returned to the reporter or no active claim exists"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        reporter = item.reported_by
        claimant = claim.claimed_by

        # Decide who receives the message
        if request.user == reporter:
            receiver = claimant

        elif request.user == claimant:
            receiver = reporter

        else:
            return Response(
                {
                    "message":
                    "You are not allowed to send messages in this chat"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # Create the message
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


# ==========================================
# 2. MY CONVERSATIONS
# ==========================================

class MyConversationsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        # Calculate the time 24 hours ago
        cutoff = timezone.now() - timedelta(minutes=1)

        # Get items reported by the current user
        reported_items = Item.objects.filter(
            reported_by=request.user
        )

        # Get items claimed by the current user
        claimed_item_ids = Claim.objects.filter(
            claimed_by=request.user
        ).values_list(
            'item_id',
            flat=True
        )

        claimed_items = Item.objects.filter(
            id__in=claimed_item_ids
        )

        # Combine reported and claimed item IDs
        item_ids = set(
            reported_items.values_list(
                'id',
                flat=True
            )
        )

        item_ids.update(
            claimed_items.values_list(
                'id',
                flat=True
            )
        )

        conversations = []

        # Check each item
        for item_id in item_ids:

            item = Item.objects.get(id=item_id)

            # Find the latest active claim or
            # completed claim within 24 hours
            claim = Claim.objects.filter(
                item=item
            ).filter(
                Q(
                    status__in=[
                        'PENDING',
                        'APPROVED'
                    ]
                )
                |
                Q(
                    status='COMPLETED',
                    completed_at__gte=cutoff
                )
            ).order_by('-created_at').first()

            if not claim:
                continue

            # Only the reporter or claimant can see it
            if (
                item.reported_by != request.user
                and claim.claimed_by != request.user
            ):
                continue

            # Add conversation to the response
            conversations.append({
                "item_id": item.id,
                "item_name": item.item_name,
                "item_type": item.item_type,
                "status": item.status,
                "claim_id": claim.id
            })

        return Response(conversations)