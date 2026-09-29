# from rest_framework import serializers
# from .models import Claim


# class ClaimSerializer(serializers.ModelSerializer):

#     item_name = serializers.CharField(
#         source='item.item_name',
#         read_only=True
#     )

#     claimed_by_username = serializers.CharField(
#         source='claimed_by.username',
#         read_only=True
#     )

#     class Meta:
#         model = Claim

#         fields = [
#             'id',
#             'item',
#             'item_name',
#             'claimed_by',
#             'claimed_by_username',
#             'reason',
#             'status',
#             'created_at',
#             'completed_at'
#         ]

#         read_only_fields = [
#             'id',
#             'claimed_by',
#             'claimed_by_username',
#             'item_name',
#             'status',
#             'created_at',
#             'completed_at'
#         ]



# backend/claims/serializers.py

from rest_framework import serializers
from .models import Claim


class ClaimSerializer(serializers.ModelSerializer):

    item_name = serializers.CharField(
        source='item.item_name',
        read_only=True
    )

    claimed_by_username = serializers.CharField(
        source='claimed_by.username',
        read_only=True
    )

    class Meta:
        model = Claim

        fields = [
            'id',
            'item',
            'item_name',
            'claimed_by',
            'claimed_by_username',
            'reason',
            'status',
            'created_at',
            'completed_at'
        ]

        read_only_fields = [
            'id',
            'claimed_by',
            'claimed_by_username',
            'item_name',
            'status',
            'created_at',
            'completed_at'
        ]