from django.urls import path
from . import views

urlpatterns = [
    # Spécialités
    path('specialites/',        views.SpecialiteListCreateView.as_view(),  name='specialite-list'),
    path('specialites/<int:pk>/', views.SpecialiteDetailView.as_view(),    name='specialite-detail'),

    # Médecins
    path('medecins/',           views.MedecinListCreateView.as_view(),     name='medecin-list'),
    path('medecins/<int:pk>/',  views.MedecinDetailView.as_view(),         name='medecin-detail'),

    # Disponibilités
    path('disponibilites/',          views.DisponibiliteListCreateView.as_view(), name='dispo-list'),
    path('disponibilites/<int:pk>/', views.DisponibiliteDetailView.as_view(),     name='dispo-detail'),

    # Disponibilités par médecin
    path('medecins/<int:medecin_id>/disponibilites/', views.MedecinDisponibilitesView.as_view(), name='medecin-dispos'),
]