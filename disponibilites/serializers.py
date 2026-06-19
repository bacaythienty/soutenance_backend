from rest_framework import serializers
from .models import Specialite, Medecin, Disponibilite


class SpecialiteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Specialite
        fields = ['id', 'nom', 'description', 'created_at']


class DisponibiliteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Disponibilite
        fields = ['id', 'jour', 'heure_debut', 'heure_fin', 'est_disponible']


class MedecinSerializer(serializers.ModelSerializer):
    specialite      = SpecialiteSerializer(read_only=True)
    specialite_id   = serializers.PrimaryKeyRelatedField(
        queryset=Specialite.objects.all(), source='specialite', write_only=True
    )
    disponibilites  = DisponibiliteSerializer(many=True, read_only=True)

    class Meta:
        model  = Medecin
        fields = ['id', 'nom', 'prenom', 'email', 'telephone',
                  'specialite', 'specialite_id', 'disponibilites', 'created_at']


class DisponibiliteDetailSerializer(serializers.ModelSerializer):
    medecin = MedecinSerializer(read_only=True)
    medecin_id = serializers.PrimaryKeyRelatedField(
        queryset=Medecin.objects.all(), source='medecin', write_only=True
    )

    class Meta:
        model  = Disponibilite
        fields = ['id', 'medecin', 'medecin_id', 'jour',
                  'heure_debut', 'heure_fin', 'est_disponible', 'created_at']

    def validate(self, data):
        if data['heure_debut'] >= data['heure_fin']:
            raise serializers.ValidationError(
                "L'heure de début doit être avant l'heure de fin."
            )
        return data