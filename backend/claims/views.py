# from datetime import timedelta

# from django.utils import timezone
# from django.db.models import Q
# from django.db import transaction

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated

# from .models import Claim
# from .serializers import ClaimSerializer
# from items.models import Item
# from chat.models import Message


# # ==========================================
# # 1. STUDENT CLAIMS
# # ==========================================

# class ClaimListCreateView(APIView):

#     permission_classes = [IsAuthenticated]

#     # View the logged-in student's claims
#     def get(self, request):

#         cutoff = timezone.now() - timedelta(hours=24)

#         claims = Claim.objects.filter(
#             claimed_by=request.user
#         ).filter(
#             Q(
#                 status__in=[
#                     'PENDING',
#                     'APPROVED',
#                     'REJECTED'
#                 ]
#             )
#             |
#             Q(
#                 status='COMPLETED',
#                 completed_at__gte=cutoff
#             )
#         ).order_by('-created_at')

#         serializer = ClaimSerializer(
#             claims,
#             many=True
#         )

#         return Response(serializer.data)

#     # Create a new claim
#     def post(self, request):

#         item_id = request.data.get('item')
#         reason = request.data.get('reason')

#         if not item_id or not reason:
#             return Response(
#                 {"message": "Item and reason are required"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         try:
#             item = Item.objects.get(pk=item_id)

#         except Item.DoesNotExist:
#             return Response(
#                 {"message": "Item not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         if item.item_type != 'FOUND':
#             return Response(
#                 {"message": "Only found items can be claimed"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         if item.reported_by == request.user:
#             return Response(
#                 {"message": "You cannot claim your own item"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         if item.status == 'RETURNED':
#             return Response(
#                 {"message": "This item has already been returned"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         active_claim_exists = Claim.objects.filter(
#             item=item,
#             status__in=['PENDING', 'APPROVED']
#         ).exists()

#         if active_claim_exists:
#             return Response(
#                 {"message": "This item already has an active claim"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         claim = Claim.objects.create(
#             item=item,
#             claimed_by=request.user,
#             reason=reason
#         )

#         serializer = ClaimSerializer(claim)

#         return Response(
#             serializer.data,
#             status=status.HTTP_201_CREATED
#         )


# # ==========================================
# # 2. STUDENT DELETE OWN CLAIM
# # ==========================================

# class ClaimDeleteView(APIView):

#     permission_classes = [IsAuthenticated]

#     def delete(self, request, pk):

#         try:
#             claim = Claim.objects.get(
#                 pk=pk,
#                 claimed_by=request.user
#             )

#         except Claim.DoesNotExist:
#             return Response(
#                 {"message": "Claim not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         # Do not allow deletion of completed claims
#         if claim.status == 'COMPLETED':
#             return Response(
#                 {
#                     "message":
#                     "Completed claims cannot be deleted."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         claim.delete()

#         return Response(
#             {"message": "Claim deleted successfully"},
#             status=status.HTTP_200_OK
#         )


# # ==========================================
# # 3. ADMIN VIEW ALL CLAIMS
# # ==========================================

# class AdminClaimListView(APIView):

#     permission_classes = [IsAuthenticated]

#     def get(self, request):

#         if not request.user.is_staff:
#             return Response(
#                 {"message": "Admin access required"},
#                 status=status.HTTP_403_FORBIDDEN
#             )

#         claims = Claim.objects.exclude(
#             status='COMPLETED'
#         ).order_by('-created_at')

#         serializer = ClaimSerializer(
#             claims,
#             many=True
#         )

#         return Response(serializer.data)


# # ==========================================
# # 4. ADMIN UPDATE CLAIM
# # ==========================================

# class AdminClaimUpdateView(APIView):

#     permission_classes = [IsAuthenticated]

#     def put(self, request, pk):

#         if not request.user.is_staff:
#             return Response(
#                 {"message": "Admin access required"},
#                 status=status.HTTP_403_FORBIDDEN
#             )

#         try:
#             claim = Claim.objects.get(pk=pk)

#         except Claim.DoesNotExist:
#             return Response(
#                 {"message": "Claim not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         new_status = request.data.get('status')

#         allowed_statuses = [
#             'PENDING',
#             'APPROVED',
#             'REJECTED',
#             'COMPLETED'
#         ]

#         if new_status not in allowed_statuses:
#             return Response(
#                 {"message": "Invalid claim status"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Do not modify completed claims
#         if claim.status == 'COMPLETED':
#             return Response(
#                 {
#                     "message":
#                     "Completed claims cannot be changed."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Only pending claims can be approved or rejected
#         if new_status in ['APPROVED', 'REJECTED']:
#             if claim.status != 'PENDING':
#                 return Response(
#                     {
#                         "message":
#                         "Only pending claims can be approved or rejected."
#                     },
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#         # A rejected claim can be reopened as pending
#         if new_status == 'PENDING':
#             if claim.status != 'REJECTED':
#                 return Response(
#                     {
#                         "message":
#                         "Only rejected claims can be reopened."
#                     },
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             claim.status = 'PENDING'
#             claim.save(update_fields=['status'])

#             return Response({
#                 "message": "Claim reopened successfully",
#                 "status": claim.status
#             })

#         # Do not approve or complete a returned item
#         if claim.item.status == 'RETURNED':
#             return Response(
#                 {
#                     "message":
#                     "This item has already been returned."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Prevent more than one approved claim
#         if new_status == 'APPROVED':

#             another_approved_claim = Claim.objects.filter(
#                 item=claim.item,
#                 status='APPROVED'
#             ).exclude(
#                 id=claim.id
#             ).exists()

#             if another_approved_claim:
#                 return Response(
#                     {
#                         "message":
#                         "Another claim for this item is already approved."
#                     },
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#         # Complete a claim and return the item
#         if new_status == 'COMPLETED':

#             if claim.status not in ['REJECTED', 'APPROVED']:
#                 return Response(
#                     {
#                         "message":
#                         "Only rejected or approved claims can be completed."
#                     },
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             with transaction.atomic():

#                 claim.status = 'COMPLETED'
#                 claim.completed_at = timezone.now()
#                 claim.save()

#                 item = claim.item
#                 item.status = 'RETURNED'
#                 item.save(update_fields=['status'])

#             return Response({
#                 "message": "Claim completed and item returned",
#                 "status": claim.status
#             })

#         # Save approval or rejection
#         claim.status = new_status
#         claim.save(update_fields=['status'])

#         # Automatically send a message when rejected
#         if new_status == 'REJECTED':

#             Message.objects.create(
#                 item=claim.item,
#                 sender=request.user,
#                 receiver=claim.claimed_by,
#                 message=(
#                     "Your claim has been rejected by the administrator. "
#                     "If you believe this decision was made by mistake, "
#                     "please contact the administrator."
#                 )
#             )

#         serializer = ClaimSerializer(claim)

#         return Response(serializer.data)


# # ==========================================
# # 5. COMPLETE CLAIM
# # ==========================================

# class CompleteClaimView(APIView):

#     permission_classes = [IsAuthenticated]

#     def put(self, request, pk):

#         try:
#             claim = Claim.objects.get(pk=pk)

#         except Claim.DoesNotExist:
#             return Response(
#                 {"message": "Claim not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         if (
#             claim.claimed_by != request.user
#             and not request.user.is_staff
#         ):
#             return Response(
#                 {"message": "You cannot complete this claim"},
#                 status=status.HTTP_403_FORBIDDEN
#             )

#         if claim.status != 'APPROVED':
#             return Response(
#                 {"message": "Only approved claims can be completed"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         with transaction.atomic():

#             claim.status = 'COMPLETED'
#             claim.completed_at = timezone.now()
#             claim.save()

#             item = claim.item
#             item.status = 'RETURNED'
#             item.save(update_fields=['status'])

#         serializer = ClaimSerializer(claim)

#         return Response(serializer.data)




from datetime import timedelta

from django.utils import timezone
from django.db.models import Q
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Claim
from .serializers import ClaimSerializer

from items.models import Item
from chat.models import Message


# ==========================================================
# 1. STUDENT CLAIMS
# ==========================================================

class ClaimListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    # ------------------------------------------------------
    # GET - Logged-in user's claims
    # ------------------------------------------------------

    def get(self, request):

        cutoff = timezone.now() - timedelta(hours=24)

        claims = Claim.objects.filter(
            claimed_by=request.user
        ).filter(
            Q(
                status__in=[
                    'PENDING',
                    'APPROVED',
                    'REJECTED'
                ]
            )
            |
            Q(
                status='COMPLETED',
                completed_at__gte=cutoff
            )
        ).order_by('-created_at')

        serializer = ClaimSerializer(
            claims,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # ------------------------------------------------------
    # POST - Submit a claim
    # ------------------------------------------------------

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
            item = Item.objects.get(
                pk=item_id
            )

        except Item.DoesNotExist:
            return Response(
                {
                    "message": "Item not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Only FOUND items can be claimed
        if item.item_type != 'FOUND':
            return Response(
                {
                    "message":
                    "Only found items can be claimed"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # User cannot claim their own item
        if item.reported_by == request.user:
            return Response(
                {
                    "message":
                    "You cannot claim your own item"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Returned item cannot be claimed
        if item.status == 'RETURNED':
            return Response(
                {
                    "message":
                    "This item has already been returned"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check for active claim
        active_claim_exists = Claim.objects.filter(
            item=item,
            status__in=[
                'PENDING',
                'APPROVED'
            ]
        ).exists()

        if active_claim_exists:
            return Response(
                {
                    "message":
                    "This item already has an active claim"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create claim
        claim = Claim.objects.create(
            item=item,
            claimed_by=request.user,
            reason=reason,
            status='PENDING'
        )

        serializer = ClaimSerializer(claim)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


# ==========================================================
# 2. STUDENT DELETE OWN CLAIM
# ==========================================================

class ClaimDeleteView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        try:
            claim = Claim.objects.get(
                pk=pk,
                claimed_by=request.user
            )

        except Claim.DoesNotExist:
            return Response(
                {
                    "message":
                    "Claim not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Completed claims cannot be deleted
        if claim.status == 'COMPLETED':
            return Response(
                {
                    "message":
                    "Completed claims cannot be deleted."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        claim.delete()

        return Response(
            {
                "message":
                "Claim deleted successfully"
            },
            status=status.HTTP_200_OK
        )


# ==========================================================
# 3. ADMIN VIEW CLAIMS
# ==========================================================

class AdminClaimListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        # Admin only
        if not request.user.is_staff:
            return Response(
                {
                    "message":
                    "Admin access required"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # Completed claims are not shown to admin
        claims = Claim.objects.exclude(
            status='COMPLETED'
        ).order_by('-created_at')

        serializer = ClaimSerializer(
            claims,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


# ==========================================================
# 4. ADMIN APPROVE / REJECT / REOPEN CLAIM
# ==========================================================

class AdminClaimUpdateView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        # --------------------------------------------------
        # Check admin
        # --------------------------------------------------

        if not request.user.is_staff:
            return Response(
                {
                    "message":
                    "Admin access required"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # --------------------------------------------------
        # Get claim
        # --------------------------------------------------

        try:
            claim = Claim.objects.get(
                pk=pk
            )

        except Claim.DoesNotExist:
            return Response(
                {
                    "message":
                    "Claim not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # --------------------------------------------------
        # Requested status
        # --------------------------------------------------

        new_status = request.data.get(
            'status'
        )

        allowed_statuses = [
            'PENDING',
            'APPROVED',
            'REJECTED'
        ]

        if new_status not in allowed_statuses:
            return Response(
                {
                    "message":
                    "Admin can only approve, reject or reopen claims."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # --------------------------------------------------
        # Completed claim cannot be changed
        # --------------------------------------------------

        if claim.status == 'COMPLETED':
            return Response(
                {
                    "message":
                    "Completed claims cannot be changed."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # --------------------------------------------------
        # Returned item cannot be changed
        # --------------------------------------------------

        if claim.item.status == 'RETURNED':
            return Response(
                {
                    "message":
                    "This item has already been returned."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # --------------------------------------------------
        # Approve / Reject
        # Only PENDING can be approved/rejected
        # --------------------------------------------------

        if new_status in [
            'APPROVED',
            'REJECTED'
        ]:

            if claim.status != 'PENDING':
                return Response(
                    {
                        "message":
                        "Only pending claims can be approved or rejected."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        # --------------------------------------------------
        # Reopen
        # Only REJECTED can become PENDING
        # --------------------------------------------------

        if new_status == 'PENDING':

            if claim.status != 'REJECTED':
                return Response(
                    {
                        "message":
                        "Only rejected claims can be reopened."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        # --------------------------------------------------
        # Prevent multiple approved claims
        # --------------------------------------------------

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

        # --------------------------------------------------
        # Save status
        # --------------------------------------------------

        claim.status = new_status

        claim.save(
            update_fields=[
                'status'
            ]
        )

        # --------------------------------------------------
        # Send rejection message
        # --------------------------------------------------

        if new_status == 'REJECTED':

            Message.objects.create(
                item=claim.item,
                sender=request.user,
                receiver=claim.claimed_by,
                message=(
                    "Your claim has been rejected by the administrator. "
                    "If you believe this decision was made by mistake, "
                    "please contact the administrator."
                )
            )

        # --------------------------------------------------
        # Return updated claim
        # --------------------------------------------------

        serializer = ClaimSerializer(
            claim
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


# ==========================================================
# 5. USER COMPLETES APPROVED CLAIM
# ==========================================================

class CompleteClaimView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        # --------------------------------------------------
        # Get user's claim
        # --------------------------------------------------

        try:
            claim = Claim.objects.get(
                pk=pk,
                claimed_by=request.user
            )

        except Claim.DoesNotExist:
            return Response(
                {
                    "message":
                    "Claim not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # --------------------------------------------------
        # Only APPROVED claim can be completed
        # --------------------------------------------------

        if claim.status != 'APPROVED':
            return Response(
                {
                    "message":
                    "Only approved claims can be completed."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # --------------------------------------------------
        # Check item
        # --------------------------------------------------

        if claim.item.status == 'RETURNED':
            return Response(
                {
                    "message":
                    "This item has already been returned."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # --------------------------------------------------
        # Complete claim + return item + delete conversation
        # --------------------------------------------------

        with transaction.atomic():

            # 1. Complete claim
            claim.status = 'COMPLETED'

            claim.completed_at = timezone.now()

            claim.save(
                update_fields=[
                    'status',
                    'completed_at'
                ]
            )

            # 2. Mark item as returned
            item = claim.item

            item.status = 'RETURNED'

            item.save(
                update_fields=[
                    'status'
                ]
            )

            # 3. Delete conversation/messages
            #
            # Your chat model uses "item" to identify
            # the conversation, so all messages belonging
            # to this item are deleted after completion.
            #
            Message.objects.filter(
                item=item
            ).delete()

        # --------------------------------------------------
        # Response
        # --------------------------------------------------

        return Response(
            {
                "message":
                "Claim completed. Item returned. Conversation deleted."
            },
            status=status.HTTP_200_OK
        )




