from django.db import models
from django.contrib.auth.models import User
from items.models import Item


class Message(models.Model):

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.sender.username}: {self.message[:30]}"