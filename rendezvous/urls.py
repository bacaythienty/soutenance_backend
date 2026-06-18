from django.urls import path
from .views import (
    PrendreRendezVousView, MesRendezVousView, AnnulerRendezVousPatientView,
    MedecinRendezVousView, ValiderRendezVousView, AnnulerRendezVousMedecinView,
    AdminRendezVousView, NotificationListView, MarquerLuView, StatistiquesView
)

urlpatterns = [
    path('rendezvous/', PrendreRendezVousView.as_view()),
    path('rendezvous/mes-rdv/', MesRendezVousView.as_view()),
    path('rendezvous/<int:pk>/', AnnulerRendezVousPatientView.as_view()),
    path('medecin/rendezvous/', MedecinRendezVousView.as_view()),
    path('rendezvous/<int:pk>/valider/', ValiderRendezVousView.as_view()),
    path('rendezvous/<int:pk>/annuler/', AnnulerRendezVousMedecinView.as_view()),
    path('admin/rendezvous/', AdminRendezVousView.as_view()),
    path('notifications/', NotificationListView.as_view()),
    path('notifications/<int:pk>/lire/', MarquerLuView.as_view()),
    path('admin/statistiques/', StatistiquesView.as_view()),
]