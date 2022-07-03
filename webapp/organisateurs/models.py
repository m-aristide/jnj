from django.db import models

# Create your models here.

class Organisateur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    paroisse = models.CharField(max_length=255)
    poste = models.CharField(max_length=255)
    commission = models.CharField(max_length=100)
    sexe = models.CharField(max_length=15, default='M')
    telephone = models.CharField(max_length=15)

    def __repr__(self):
        return f"Organisateur({self.pk}, {self.nom}, {self.prenom}, {self.poste}, {self.commission})"

    def __str__(self):
        return f"Organisateur({self.pk}, {self.nom}, {self.prenom}, {self.poste}, {self.commission})"
