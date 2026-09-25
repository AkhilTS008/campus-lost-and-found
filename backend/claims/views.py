from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Claim
from .serializers import ClaimSerializer
from items.models import Item

class AdminClaimUpdateView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        if not request.user.is_staff:
            return Response(
                {"message": "Admin access required"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            claim = Claim.objects.get(pk=pk)
        except Claim.DoesNotExist:
            return Response(
                {"message": "Claim not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        new_status = request.data.get('status')

        if new_status not in ['APPROVED', 'REJECTED']:
            return Response(
                {"message": "Status must be APPROVED or REJECTED"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Only PENDING claims can be approved or rejected
        if claim.status != 'PENDING':
            return Response(
                {
                    "message":
                    f"This claim is already {claim.status} "
                    "and cannot be changed."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Item cannot be claimed again after it is returned
        if claim.item.status == 'RETURNED':
            return Response(
                {
                    "message":
                    "This item has already been returned."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Prevent multiple approved claims for one item
        if new_status == 'APPROVED':

            another_approved_claim = Claim.objects.filter(
                item=claim.item,
                status='APPROVED'
            ).exclude(
                id=claim.id
            ).exists()

            if another_approved_claim:
                return Response(
                    {
                        "message":
                        "Another claim for this item is already approved."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        claim.status = new_status
        claim.save()

        serializer = ClaimSerializer(claim)

        return Response(serializer.data)
    


class ClaimListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        claims = Claim.objects.filter(
            claimed_by=request.user
        ).order_by('-created_at')

        serializer = ClaimSerializer(
            claims,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        item_id = request.data.get('item')
        reason = request.data.get('reason')

        if not item_id or not reason:
            return Response(
                {
                    "message": "Item and reason are required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            item = Item.objects.get(pk=item_id)
        except Item.DoesNotExist:
            return Response(
                {
                    "message": "Item not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if item.item_type != 'FOUND':
            return Response(
                {
                    "message": "Only found items can be claimed"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if item.reported_by == request.user:
            return Response(
                {
                    "message": "You cannot claim your own item"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        active_claim_exists = Claim.objects.filter(
            item=item,
            status__in=['PENDING', 'APPROVED']
        ).exists()

        if active_claim_exists:
            return Response(
                {
                    "message": "This item already has an active claim"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        claim = Claim.objects.create(
            item=item,
            claimed_by=request.user,
            reason=reason
        )

        serializer = ClaimSerializer(claim)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

class AdminClaimListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if not request.user.is_staff:
            return Response(
                {"message": "Admin access required"},
                status=status.HTTP_403_FORBIDDEN
            )

        claims = Claim.objects.all().order_by('-created_at')

        serializer = ClaimSerializer(
            claims,
            many=True
        )

        return Response(serializer.data)
    
class CompleteClaimView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        try:
            claim = Claim.objects.get(pk=pk)

        except Claim.DoesNotExist:
            return Response(
                {"message": "Claim not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if (
            claim.claimed_by != request.user
            and not request.user.is_staff
        ):
            return Response(
                {"message": "You cannot complete this claim"},
                status=status.HTTP_403_FORBIDDEN
            )

        if claim.status != 'APPROVED':
            return Response(
                {
                    "message": "Only approved claims can be completed"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        claim.status = 'COMPLETED'
        claim.save()

        item = claim.item
        item.status = 'RETURNED'
        item.save()

        serializer = ClaimSerializer(claim)

        return Response(serializer.data)
