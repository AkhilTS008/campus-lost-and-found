from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Item(models.Model):

    ITEM_TYPES = [
        ('LOST', 'Lost'),
        ('FOUND', 'Found'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('RETURNED', 'Returned'),
    ]

    item_name = models.CharField(max_length=100)

    category = models.CharField(max_length=100)

    description = models.TextField()

    location = models.CharField(max_length=200)

    date = models.DateField()

    image = models.ImageField(
        upload_to='items/',
        blank=True,
        null=True
    )

    item_type = models.CharField(
        max_length=10,
        choices=ITEM_TYPES
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )

    reported_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.item_name