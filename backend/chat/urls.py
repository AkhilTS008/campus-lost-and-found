from django.urls import path

from .views import (
    ChatView,
    MyConversationsView
)


urlpatterns = [

    path(
        'chat/',
        MyConversationsView.as_view(),
        name='my-conversations'
    ),

    path(
        'chat/<int:item_id>/',
        ChatView.as_view(),
        name='chat'
    ),

]