from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import random


from contacts.constants import FIELDS
from contacts.models import Participant, CodeEncadreur

# Create your views here.

@login_required(login_url='connexion')
def encadreurs(request):
    encadreurs = Participant.objects.values(*FIELDS).exclude(encadreur__isnull=True).order_by('-pk')
    codes = CodeEncadreur.objects.all().order_by('-pk')
    return render(request, 'contacts/encadreurs.html', context={'encadreurs': encadreurs, 'codes': codes})

@login_required(login_url='connexion')
def creer_code_encadreur(request):
    code = CodeEncadreur(code = f'ENC_{random.randint(1235, 9999)}')
    code.save()
    return redirect('encadreurs')

@login_required(login_url='connexion')
def delete_code_encadreur(request):
    code = CodeEncadreur.objects.get(pk = int(request.POST.get('id')))
    if code.active :
        part = Participant.objects.get(encadreur = code.code)
        part.encadreur = None
        part.save()
    code.delete()
    return redirect('encadreurs')


