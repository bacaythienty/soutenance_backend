from rest_framework import serializers
from .models import RendezVous, Notification

class RendezVousSerializer(serializers.ModelSerializer):
    class Meta:
        model = RendezVous
        fields = '_all_'
        read_only_fields = ['patient', 'statut', 'date_creation']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '_all_'