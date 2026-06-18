from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import RendezVous, Notification

# Cacher les modèles par défaut de Django
admin.site.unregister(User)
admin.site.unregister(Group)

# Enregistrer tes modèles
admin.site.register(RendezVous)
admin.site.register(Notification)