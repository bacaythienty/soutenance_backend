

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, PatientProfile, MedecinProfile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'telephone']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data, role='patient')
        PatientProfile.objects.create(user=user)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'telephone']


class MedecinProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = MedecinProfile
        fields = '__all__'