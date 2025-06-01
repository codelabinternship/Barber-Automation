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



class BarberServiceSerializer(serializers):
    barber = BarberSerializer()
    service = ServiceSerializer
    class Meta:
        model = BarberService
        fields = 'barber, service, price '




class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = 'barber, weekday, start_time,  end_time '

