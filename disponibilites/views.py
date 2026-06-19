from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Specialite, Medecin, Disponibilite
from .serializers import (
    SpecialiteSerializer, MedecinSerializer,
    DisponibiliteDetailSerializer
)


# ── Spécialités ───────────────────────────────────────────
class SpecialiteListCreateView(generics.ListCreateAPIView):
    queryset         = Specialite.objects.all()
    serializer_class = SpecialiteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SpecialiteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset         = Specialite.objects.all()
    serializer_class = SpecialiteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# ── Médecins ──────────────────────────────────────────────
class MedecinListCreateView(generics.ListCreateAPIView):
    queryset         = Medecin.objects.select_related('specialite').all()
    serializer_class = MedecinSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends  = [filters.SearchFilter]
    search_fields    = ['nom', 'prenom', 'specialite__nom']


class MedecinDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset         = Medecin.objects.all()
    serializer_class = MedecinSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# ── Disponibilités ────────────────────────────────────────
class DisponibiliteListCreateView(generics.ListCreateAPIView):
    serializer_class = DisponibiliteDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset   = Disponibilite.objects.select_related('medecin').all()
        medecin_id = self.request.query_params.get('medecin')
        jour       = self.request.query_params.get('jour')
        if medecin_id:
            queryset = queryset.filter(medecin_id=medecin_id)
        if jour:
            queryset = queryset.filter(jour=jour)
        return queryset


class DisponibiliteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset         = Disponibilite.objects.all()
    serializer_class = DisponibiliteDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# ── Disponibilités d'un médecin spécifique ────────────────
class MedecinDisponibilitesView(APIView):
    def get(self, request, medecin_id):
        dispos = Disponibilite.objects.filter(
            medecin_id=medecin_id,
            est_disponible=True
        ).order_by('jour', 'heure_debut')
        serializer = DisponibiliteDetailSerializer(dispos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)