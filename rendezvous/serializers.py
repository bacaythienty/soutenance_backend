from rest_framework import serializers
from .models import RendezVous, Notification

class RendezVousSerializer(serializers.ModelSerializer):
    class Meta:
        model = RendezVous
        fields = '__all__'
        read_only_fields = ['patient', 'statut', 'date_creation']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'