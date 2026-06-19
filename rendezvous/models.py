from django.db import models
from django.conf import settings

class RendezVous(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmé'),
        ('annule', 'Annulé'),
        ('termine', 'Terminé'),
    ]
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rdv_patient')
    medecin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rdv_medecin')
    creneau_id = models.IntegerField(null=True, blank=True)  # temporaire
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    motif = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"RDV patient#{self.patient_id} -> medecin#{self.medecin_id} ({self.statut})"

    class Meta:
        verbose_name = "Rendez-vous"
        verbose_name_plural = "Rendez-vous"
        ordering = ['-date_creation']


class Notification(models.Model):
    destinataire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    lu = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notif -> {self.destinataire.username}"

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-date_creation']