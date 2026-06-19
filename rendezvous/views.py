from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from django.db.models import Count
from .models import RendezVous, Notification
from .serializers import RendezVousSerializer, NotificationSerializer

class PrendreRendezVousView(generics.CreateAPIView):
    serializer_class = RendezVousSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def perform_create(self, serializer):
        creneau = serializer.validated_data['creneau']
        if not creneau.est_disponible:
            raise Exception("Ce créneau n'est plus disponible.")
        creneau.est_disponible = False
        creneau.save()
        rdv = serializer.save(patient=self.request.user, medecin=creneau.medecin)
        Notification.objects.create(
            destinataire=rdv.medecin,
            message=f"Nouveau rendez-vous de {rdv.patient.get_full_name()} le {rdv.creneau.date}."
        )

class MesRendezVousView(generics.ListAPIView):
    serializer_class = RendezVousSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RendezVous.objects.filter(patient=self.request.user).order_by('-date_creation')

class AnnulerRendezVousPatientView(generics.DestroyAPIView):
    serializer_class = RendezVousSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RendezVous.objects.filter(patient=self.request.user)

class MedecinRendezVousView(generics.ListAPIView):
    serializer_class = RendezVousSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RendezVous.objects.filter(medecin=self.request.user).order_by('-date_creation')

class ValiderRendezVousView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        rdv = RendezVous.objects.get(pk=pk, medecin=request.user)
        rdv.statut = 'confirme'
        rdv.save()
        Notification.objects.create(
            destinataire=rdv.patient,
            message=f"Votre rendez-vous du {rdv.creneau.date} a été confirmé."
        )
        return Response(RendezVousSerializer(rdv).data)

class AnnulerRendezVousMedecinView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        rdv = RendezVous.objects.get(pk=pk, medecin=request.user)
        rdv.statut = 'annule'
        rdv.creneau.est_disponible = True
        rdv.creneau.save()
        rdv.save()
        Notification.objects.create(
            destinataire=rdv.patient,
            message=f"Votre rendez-vous du {rdv.creneau.date} a été annulé par le médecin."
        )
        return Response(RendezVousSerializer(rdv).data)

class AdminRendezVousView(generics.ListAPIView):
    serializer_class = RendezVousSerializer
    queryset = RendezVous.objects.all()
    permission_classes = [permissions.IsAdminUser]

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(destinataire=self.request.user).order_by('-date_creation')

class MarquerLuView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        notif = Notification.objects.get(pk=pk, destinataire=request.user)
        notif.lu = True
        notif.save()
        return Response(NotificationSerializer(notif).data)

class StatistiquesView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        data = {
            'total_rdv': RendezVous.objects.count(),
            'confirmes': RendezVous.objects.filter(statut='confirme').count(),
            'annules': RendezVous.objects.filter(statut='annule').count(),
            'en_attente': RendezVous.objects.filter(statut='en_attente').count(),
            'rdv_par_medecin': list(
                RendezVous.objects.values('medecin__username').annotate(total=Count('id'))
            ),
        }
        return Response(data)