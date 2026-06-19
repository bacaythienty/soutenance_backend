from django.contrib import admin
from .models import Specialite, Medecin, Disponibilite


@admin.register(Specialite)
class SpecialiteAdmin(admin.ModelAdmin):
    list_display  = ['nom', 'created_at']
    search_fields = ['nom']


@admin.register(Medecin)
class MedecinAdmin(admin.ModelAdmin):
    list_display  = ['nom', 'prenom', 'specialite', 'email', 'telephone']
    list_filter   = ['specialite']
    search_fields = ['nom', 'prenom', 'email']


@admin.register(Disponibilite)
class DisponibiliteAdmin(admin.ModelAdmin):
    list_display  = ['medecin', 'jour', 'heure_debut', 'heure_fin', 'est_disponible']
    list_filter   = ['jour', 'est_disponible', 'medecin__specialite']
    search_fields = ['medecin__nom', 'medecin__prenom']