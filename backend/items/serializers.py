from rest_framework import serializers
from .models import Item


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = [
            'id',
            'item_name',
            'category',
            'description',
            'location',
            'date',
            'image',
            'item_type',
            'status',
            'reported_by',
            'created_at'
        ]

        read_only_fields = [
            'id',
            'status',
            'reported_by',
            'created_at'
        ]