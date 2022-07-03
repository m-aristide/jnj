from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from pathlib import Path
from xhtml2pdf import pisa

from organisateurs.models import Organisateur
# Create your views here.

# Create your views here.
@login_required(login_url='connexion')
def organisateurs(request) :
    
    organisateurs = Organisateur.objects.all()

    # gestion alerte
    alerte = request.session.get('alerte', None)
    if alerte :
        del request.session['alerte']
    return render(request, 'organisateurs.html', context={'organisateurs': organisateurs, 'alerte': alerte})


@login_required(login_url='connexion')
def organisateur(request, id=None) :

    organisateur = {}

    if request.method == 'POST':
        organisateur = Organisateur(
            nom=request.POST.get('nom').upper(),
            prenom=request.POST.get('prenom').title(),
            telephone=request.POST.get('telephone'),
            paroisse = request.POST.get('paroisse'),
            sexe = request.POST.get('sexe'),
            poste = request.POST.get('poste'),
            commission = request.POST.get('commission'),
        )

        id = int(request.POST.get('id'))
        if id :
            organisateur.pk = id
        organisateur.save()

        # prod badge
        render_pdf_view(organisateur)

        request.session['alerte'] = {'success': True, 'message': 'Opération effectuée avec succès'}
        return redirect('organisateurs')

    else :
        print(id)
        if id :
            organisateur = Organisateur.objects.get(pk = id)

    return render(request, 'organisateur.html', context={'org': organisateur})


@login_required(login_url='connexion')
def delete_organisateur(request, id:int):
    organisateur = Organisateur.objects.get(pk = id)
    organisateur.delete()
    request.session['alerte'] = {'success': True, 'message': 'Opération effectuée avec succès'}
    return redirect('organisateurs')

def render_pdf_view(org: Organisateur):
    # html template
    html = get_template('badge_org.html').render({'org': org})

    # fichier pdf
    STATIC_DIR = Path(__file__).resolve().parent / 'static' / 'badges'
    output_filename = STATIC_DIR / f'org_{org.pk}.pdf'
    result_file = open(output_filename, "w+b")

    # create a pdf
    pisa.CreatePDF(html, dest=result_file)