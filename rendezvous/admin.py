from django.contrib import admin
from django.contrib.auth.models import Group
from .models import RendezVous, Notification

# Cacher le modèle Group par défaut de Django
admin.site.unregister(Group)

# Enregistrer tes modèles
admin.site.register(RendezVous)
admin.site.register(Notification)