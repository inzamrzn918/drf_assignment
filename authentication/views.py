from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import UserRegistrationSerializer, UserDetailsSerializer


class CSRFTokenView(APIView):
    permission_classes = [AllowAny]

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        csrf_token = get_token(request)
        return Response({'csrf_token': csrf_token})


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=UserRegistrationSerializer,
        responses={201: 'User registered successfully'}
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {'message': 'User registered successfully', 'user_id': str(user.id)},
            status=status.HTTP_201_CREATED
        )


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={200: 'Login Successful'}
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Set secure HTTP-only cookie
            response = Response({'message': 'Login successful'})
            response.set_cookie(
                'auth_token',
                str(user.id),
                httponly=True,
                secure=True,
                samesite='Strict'
            )
            return response

        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserDetailsSerializer(request.user)
        return Response(serializer.data)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        response = Response({'message': 'Logout successful'})
        response.delete_cookie('auth_token')
        return response