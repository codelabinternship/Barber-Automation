from .models import CustomUser


from rest_framework import serializers
from .models import *



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "date_joined", "role", 'phone')




class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'



class BarberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barber
        fields = '_all__'



class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'



class BarberServiceSerializer(serializers):
    barber = BarberSerializer()
    service = ServiceSerializer
    class Meta:
        model = BarberService
        fields = '__all_'




class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ''

