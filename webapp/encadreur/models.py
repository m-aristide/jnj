from django.db import models

# Create your models here.

class CodeEncadreur(models.Model):
    code = models.CharField(max_length=20, unique=True, null=True)
    active = models.BooleanField(default=False)
