from django.shortcuts import redirect, render
import random

from contacts.models import Participant, CodeEncadreur

# Create your views here.

def encadreurs(request):
    encadreurs = Participant.objects.exclude(encadreur__isnull=True).order_by('-pk')
    codes = CodeEncadreur.objects.all().order_by('-pk')
    return render(request, 'contacts/encadreurs.html', context={'encadreurs': encadreurs, 'codes': codes})

def creer_code_encadreur(request):
    code = CodeEncadreur(code = f'ENC_{random.randint(1235, 9999)}')
    code.save()
    return redirect('encadreurs')

def delete_code_encadreur(request):
    code = CodeEncadreur.objects.get(pk = int(request.POST.get('id')))
    if code.active :
        part = Participant.objects.get(encadreur = code.code)
        part.encadreur = None
        part.save()
    code.delete()
    return redirect('encadreurs')


