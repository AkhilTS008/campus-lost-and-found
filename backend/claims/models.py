# from django.db import models
# from django.contrib.auth.models import User
# from items.models import Item


# class Claim(models.Model):

#     STATUS_CHOICES = [
#         ('PENDING', 'Pending'),
#         ('APPROVED', 'Approved'),
#         ('REJECTED', 'Rejected'),
#         ('COMPLETED', 'Completed'),
#     ]

#     item = models.ForeignKey(
#         Item,
#         on_delete=models.CASCADE
#     )

#     claimed_by = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE
#     )

#     reason = models.TextField()

#     status = models.CharField(
#         max_length=20,
#         choices=STATUS_CHOICES,
#         default='PENDING'
#     )

#     created_at = models.DateTimeField(
#         auto_now_add=True
#     )
#     completed_at = models.DateTimeField(
#     null=True,
#     blank=True
#     )

#     def __str__(self):
#         return f"{self.claimed_by.username} - {self.item.item_name}"




# backend/claims/models.py

from django.db import models
from django.contrib.auth.models import User
from items.models import Item


class Claim(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('COMPLETED', 'Completed'),
    ]

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE
    )

    claimed_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.claimed_by.username} - {self.item.item_name}"



