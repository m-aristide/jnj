from django.db import models

# Create your models here.

class Site(models.Model):
    designation = models.CharField(max_length=255)
    description = models.TextField()
    sexe = models.CharField(max_length=5, default='M')

    def __repr__(self):
        return f"Site({self.pk}, {self.designation}, {self.description}, {self.sexe})"

    def __str__(self):
        return f"Site({self.pk}, {self.designation}, {self.description}, {self.sexe})"

    
class Dortoire(models.Model):
    code = models.CharField(max_length=20)
    capacite = models.IntegerField()
    occupation = models.IntegerField(default=0)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)



