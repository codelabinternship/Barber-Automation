from .models import CustomUser


from rest_framework import serializers
from .models import *



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = 'id', 'username', 'email', 'phone_number'



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "date_joined", "role", 'phone')




class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = 'name'



class BarberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barber
        fields = 'user, region, bio, rating, created_at'



class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = 'name ,  default_price '



class BarberServiceSerializer(serializers.Serializer):
    barber = BarberSerializer()
    service = ServiceSerializer
    class Meta:
        model = BarberService
        fields = 'barber, service, price '




class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = 'barber, weekday, start_time,  end_time '


from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()




from rest_framework import serializers
from .models import CustomUser

class AdminCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            role='admin'
        )
        user.set_password(validated_data['password'])
        user.save()
        return user




from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        data['role'] = self.user.role
        return data




from rest_framework import serializers

class DevPasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate_new_password(self, value):
        return value


from rest_framework import serializers

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserSessionSerializer(serializers.ModelSerializer):
    user_telegram_id = serializers.CharField(source='user.telegram_id', read_only=True)

    class Meta:
        model = UserSession
        fields = ['id', 'user', 'user_telegram_id', 'session_data', 'created_at', 'updated_at']





class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['user', 'barber', 'service', ' scheduled_time', 'status', 'notes', 'created_at']



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['appointment', 'amount', 'transaction_id','status','paid_at']


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        field = ['method','sent_at', 'status', 'send_time','user',' appointment']



class AppointmentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentHistory
        field = ['appointment','user', 'action','notes', 'created_at']


class AppointmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentList
        field = ['user', 'barber', 'created_at']


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        field = ['user', 'role', 'create_at']

