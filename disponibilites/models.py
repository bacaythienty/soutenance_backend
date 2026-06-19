from django.db import models

class Specialite(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Spécialité"
        verbose_name_plural = "Spécialités"
        ordering = ['nom']


class Medecin(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, blank=True)
    specialite = models.ForeignKey(Specialite, on_delete=models.SET_NULL, null=True, related_name='medecins')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.prenom} {self.nom}"

    class Meta:
        verbose_name = "Médecin"
        verbose_name_plural = "Médecins"
        ordering = ['nom']


class Disponibilite(models.Model):
    JOURS_CHOICES = [
        ('lundi',    'Lundi'),
        ('mardi',    'Mardi'),
        ('mercredi', 'Mercredi'),
        ('jeudi',    'Jeudi'),
        ('vendredi', 'Vendredi'),
        ('samedi',   'Samedi'),
    ]

    medecin     = models.ForeignKey(Medecin, on_delete=models.CASCADE, related_name='disponibilites')
    jour        = models.CharField(max_length=20, choices=JOURS_CHOICES)
    heure_debut = models.TimeField()
    heure_fin   = models.TimeField()
    est_disponible = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medecin} — {self.jour} {self.heure_debut}→{self.heure_fin}"

    class Meta:
        verbose_name = "Disponibilité"
        verbose_name_plural = "Disponibilités"
        ordering = ['jour', 'heure_debut']
        unique_together = ['medecin', 'jour', 'heure_debut']