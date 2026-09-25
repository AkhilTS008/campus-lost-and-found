from django.urls import path

from .views import (
    ItemListCreateView,
    ItemDetailView,
    MyReportsView
)


urlpatterns = [

    path(
        'items/',
        ItemListCreateView.as_view(),
        name='items'
    ),

    path(
        'items/<int:pk>/',
        ItemDetailView.as_view(),
        name='item-detail'
    ),

    path(
        'my-reports/',
        MyReportsView.as_view(),
        name='my-reports'
    ),

]