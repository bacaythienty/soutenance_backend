

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('medecin', 'Médecin'),
        ('patient', 'Patient'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    telephone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    date_naissance = models.DateField(null=True, blank=True)
    sexe = models.CharField(max_length=10, blank=True)
    adresse = models.TextField(blank=True)

    def __str__(self):
        return f"Patient: {self.user.username}"


class MedecinProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='medecin_profile')
    specialite = models.ForeignKey('disponibilites.Specialite', on_delete=models.SET_NULL, null=True)
    numero_ordre = models.CharField(max_length=50, blank=True)
    biographie = models.TextField(blank=True)
    ville = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"