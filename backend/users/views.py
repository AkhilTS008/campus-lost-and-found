from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer

from rest_framework.permissions import IsAuthenticated


class RegisterView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "User registered successfully"
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):

    def post(self, request):

        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(
            username=username,
            password=password
        )

        if user is not None:

            token, created = Token.objects.get_or_create(
                user=user
            )

            return Response(
                {
                    "message": "Login successful",
                    "token": token.key,
                    "username": user.username,
                    "is_staff": user.is_staff
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "message": "Invalid username or password"
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response(
            {
                "message": "You are authenticated",
                "username": request.user.username
            }
        )