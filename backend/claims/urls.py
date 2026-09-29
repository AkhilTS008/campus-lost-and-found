# from django.urls import path

# from .views import (
#     ClaimListCreateView,
#     ClaimDeleteView,
#     AdminClaimListView,
#     AdminClaimUpdateView,
#     CompleteClaimView
# )

# urlpatterns = [

#     path(
#         'claims/',
#         ClaimListCreateView.as_view(),
#         name='claims'
#     ),

#     path(
#         'claims/<int:pk>/',
#         ClaimDeleteView.as_view(),
#         name='claim-delete'
#     ),

#     path(
#         'claims/<int:pk>/complete/',
#         CompleteClaimView.as_view(),
#         name='complete-claim'
#     ),

#     path(
#         'admin/claims/',
#         AdminClaimListView.as_view(),
#         name='admin-claims'
#     ),

#     path(
#         'admin/claims/<int:pk>/',
#         AdminClaimUpdateView.as_view(),
#         name='admin-claim-update'
#     ),


from django.urls import path

from .views import (
    ClaimListCreateView,
    ClaimDeleteView,
    AdminClaimListView,
    AdminClaimUpdateView,
    CompleteClaimView
)


urlpatterns = [

    path(
        'claims/',
        ClaimListCreateView.as_view(),
        name='claims'
    ),

    path(
        'claims/<int:pk>/',
        ClaimDeleteView.as_view(),
        name='claim-delete'
    ),

    path(
        'claims/<int:pk>/complete/',
        CompleteClaimView.as_view(),
        name='complete-claim'
    ),

    path(
        'admin/claims/',
        AdminClaimListView.as_view(),
        name='admin-claims'
    ),

    path(
        'admin/claims/<int:pk>/',
        AdminClaimUpdateView.as_view(),
        name='admin-claim-update'
    ),
]