from django.shortcuts import render
from django.views.generic import TemplateView
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
from urllib3 import request

from .models import OTPVerification
import random

from .serializers import UserRegistrationSerializer, UserDetailsSerializer
from .utils import send_otp_email


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
        
        # Check if the serializer is valid
        if not serializer.is_valid():
            print(serializer.errors)  # Log the errors for debugging
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()

        # Generate OTP
        otp = str(random.randint(100000, 999999))  # Generate a 6-digit OTP
        OTPVerification.objects.create(user=user, otp=otp)

        # Here you would send the OTP to the user's email
        # send_otp_email(user.email, otp)  # Implement this function
        send_otp_email(user.email, otp)
        return Response(
            {'message': 'User registered successfully. An OTP has been sent to your email.', 'user_id': str(user.id)},
            status=status.HTTP_201_CREATED
        )


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={200: 'Login Successful'}
    )
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        print(f"Attempting to log in with email: {email} and password: {password}")

        user = authenticate(request, email=email, password=password)

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

        print("Login failed: Invalid credentials")
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


class OTPVerificationView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_STRING),
                'otp': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={200: 'OTP verified successfully', 400: 'Invalid or expired OTP'}
    )
    def post(self, request):
        user_id = request.data.get('user_id')
        otp = request.data.get('otp')

        try:
            otp_verification = OTPVerification.objects.get(user__id=user_id, otp=otp, is_verified=False)
            otp_verification.is_verified = True
            otp_verification.save()
            return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
        except OTPVerification.DoesNotExist:
            return Response({'error': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)


class LoginPageViewHtml(TemplateView):
    template_name = "ui/index.html"