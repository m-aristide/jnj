from datetime import date, datetime

from django.db import models

from dortoires.models import Dortoire

class Participant(models.Model):
    code = models.CharField(max_length=20, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    diocese = models.CharField(max_length=100)
    sexe = models.CharField(max_length=100)
    person_contacter_name = models.CharField(max_length=100)
    paroisse = models.CharField(max_length=100)
    person_contacter_phone = models.CharField(max_length=100)
    allergies = models.CharField(max_length=255, null=True)
    groupe_sanguin = models.CharField(max_length=3, null=True)
    maladies = models.CharField(max_length=500,null=True)
    produit = models.BooleanField(default=False)
    encadreur = models.CharField(max_length=20,null=True)
    type = models.CharField(max_length=20, default='Laïc')
    age = models.IntegerField(default=15)
    polo = models.CharField(max_length=5, default='L')
    photo = models.TextField(null=True)
    paye = models.TextField(max_length=20, null=True)
    cni = models.CharField(max_length=20, null=True)
    dortoir = models.ForeignKey(Dortoire, on_delete=models.SET_NULL, blank=True, null=True)
    create_date = models.DateField(default=date.today)
    createat = models.DateTimeField(default=datetime.now)

    def __repr__(self):
        return f"Participant({self.pk}, {self.first_name}, {self.last_name})"

    def __str__(self):
        return f"Participant({self.pk}, {self.first_name}, {self.last_name}{self.phone_number}{self.diocese})"


class CodeEncadreur(models.Model):
    code = models.CharField(max_length=20, unique=True, null=True)
    active = models.BooleanField(default=False)

if __name__ == "__main__":
    martin = Participant(first_name = "Martin", last_name = "Voisin")
    martin.save()