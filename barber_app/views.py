from django.contrib.auth import get_user_model, authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from barber_app.serializers import (
    CustomTokenObtainSerializer,
    AdminCreateSerializer,
    CustomUserSerializer,
    DevPasswordResetSerializer
)

User = get_user_model()


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from barber_app.serializers import RegisterSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(APIView):

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            if User.objects.filter(username=username).exists():
                return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

            User.objects.create_user(username=username, email=email, password=password)
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer


class MeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)


class ProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .serializers import AdminCreateSerializer
from .models import CustomUser


class CreateAdminBySuperadminView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        if request.user.role != 'super_admin':
            return Response({'error': 'Only super_admin can create admin'}, status=403)

        serializer = AdminCreateSerializer(data=request.data)
        if serializer.is_valid():
            admin = serializer.save()
            return Response({'message': 'Admin user created successfully'}, status=201)
        return Response(serializer.errors, status=400)



class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        role = request.user.role
        target_user_id = request.data.get('user_id')
        new_password = request.data.get('new_password')
        old_password = request.data.get('old_password')

        try:
            target_user = User.objects.get(id=target_user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        if role == 'developer':
            target_user.set_password(new_password)
            target_user.save()
            return Response({'message': 'Password reset successfully by developer'})

        elif role == 'superadmin':
            if target_user.role != 'admin':
                return Response({'error': 'Superadmin can only reset admin passwords'}, status=403)
            target_user.set_password(new_password)
            target_user.save()
            return Response({'message': 'Password reset by superadmin'})

        elif role == 'admin':
            if target_user != request.user:
                return Response({'error': 'Admins can only reset their own password'}, status=403)
            if not request.user.check_password(old_password):
                return Response({'error': 'Old password incorrect'}, status=400)
            target_user.set_password(new_password)
            target_user.save()
            return Response({'message': 'Password reset successfully'})

        return Response({'error': 'Invalid role'}, status=403)


class DevPasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, user_id):
        serializer = DevPasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'detail': 'User not found.'}, status=404)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'detail': 'Password reset successfully.'})
        return Response(serializer.errors, status=400)

class ProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = CustomUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

