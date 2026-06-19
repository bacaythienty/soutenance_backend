from django.contrib import admin
from .models import User, MedecinProfile, PatientProfile

admin.site.register(User)
admin.site.register(MedecinProfile)
admin.site.register(PatientProfile)