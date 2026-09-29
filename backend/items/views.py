from django.db.migrations import serializer
from django.http import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Item
from .serializers import ItemSerializer


class ItemListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        items = Item.objects.filter(
            status='ACTIVE'
        ).order_by('-created_at')

        search = request.query_params.get('search')
        item_type = request.query_params.get('item_type')
        category = request.query_params.get('category')
        location = request.query_params.get('location')

        if search:
            items = items.filter(
                item_name__icontains=search
            )

        if item_type:
            items = items.filter(
                item_type__iexact=item_type
            )

        if category:
            items = items.filter(
                category__icontains=category
            )

        if location:
            items = items.filter(
                location__icontains=location
            )

        serializer = ItemSerializer(
            items,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = ItemSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                reported_by=request.user
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ItemDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        try:
            item = Item.objects.get(pk=pk)

        except Item.DoesNotExist:

            return Response(
                {"message": "Item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ItemSerializer(item)

        return Response(serializer.data)

    def put(self, request, pk):

        try:
            item = Item.objects.get(pk=pk)

        except Item.DoesNotExist:

            return Response(
                {"message": "Item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if item.reported_by != request.user and not request.user.is_staff:

            return Response(
                {"message": "You cannot edit this item"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ItemSerializer(
            item,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):

        try:
            item = Item.objects.get(pk=pk)

        except Item.DoesNotExist:

            return Response(
                {"message": "Item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if item.reported_by != request.user and not request.user.is_staff:

            return Response(
                {"message": "You cannot delete this item"},
                status=status.HTTP_403_FORBIDDEN
            )

        item.delete()

        return Response(
            {"message": "Item deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )



class MyReportsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        items = Item.objects.filter(
            reported_by=request.user,
            status='ACTIVE'
        ).order_by('-created_at')

        serializer = ItemSerializer(
        items,
            many=True
        )

        return Response(serializer.data)