from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.template.loader import get_template
from pathlib import Path
import io
import base64
from datetime import datetime

from xhtml2pdf import pisa
import qrcode 

from contacts.models import Participant
from encadreur.models import CodeEncadreur
from contacts.constants import DIOCESES, GROUPES_SANGUINS, FIELDS
from dortoires.models import Dortoire

# Create your views here.

def index(request):
    # gestion alerte
    alerte = request.session.get('alerte', None)
    if alerte :
        del request.session['alerte']
    context={
        'dioceses': DIOCESES, 
        'alerte': alerte, 
        'ages': range(16,46),
        'groupes_sangs': GROUPES_SANGUINS
    }

    return render(request, 'contacts/index.html', context=context)

# ajouter un participant
def add_contact(request):
    
    participant = Participant(
            first_name=request.POST.get('first_name').title(),
            last_name=request.POST.get('last_name').upper(),
            phone_number=request.POST.get('phone_number'),
            diocese = request.POST.get('diocese'),
            sexe = request.POST.get('sexe'),
            person_contacter_name = request.POST.get('person_contacter_name'),
            person_contacter_phone = request.POST.get('person_contacter_phone'),
            paroisse = request.POST.get('paroisse'),
            code = request.POST.get('code'),
            allergies = request.POST.get('allergies'),
            cni = request.POST.get('cni', None),
            age = int(request.POST.get('age')),
            polo = request.POST.get('polo'),
            type = request.POST.get('type'),
            photo = request.POST.get('resizephoto'),
            groupe_sanguin = request.POST.get('groupe_sanguin'),
            maladies = request.POST.get('maladies')
        )    

    # code encadreur
    code_encadeur = None
    if request.POST.get('encadreur', None)  :
        try:
            code_encadeur = CodeEncadreur.objects.get(code = request.POST.get('encadreur'), active = False)
        except CodeEncadreur.DoesNotExist:
            request.session['alerte'] = {'success': False, 'message': f'Code accompagnateur invalide !'}
            return redirect('index')

    # enregistrement code
    if code_encadeur : 
        participant.encadreur = code_encadeur.code
        code_encadeur.active = True
        code_encadeur.save()
    
    # enregistrement du participant pour avoir l'id et produir le code
    participant.save()

    # code participant
    participant.code = code_generator(participant.diocese, participant.pk)
    participant.save()
    
    # production du badge
    render_pdf_view(participant)

    request.session['alerte'] = {'success': True, 'message': 'Opération effectuée avec succès'}
    return redirect(f'inscrits/{participant.pk}')

# modifier les données d'un participant
def modifier_participant(request, id: int):
    # verification id
    if not request.POST.get('id', None):
        request.session['alerte'] = {'success': False, 'message': 'Participant invalide'}
        return redirect(f'inscrits')

    # récupération participant
    part = Participant.objects.get(pk=int(request.POST.get('id')))

    # vérifier que le badge n'est pas encore produit, si oui on ne modifie plus
    if part.produit :
        request.session['alerte'] = {'success': False, 'message': 'Le badge de ce participant a déjà été produit. Ses informations ne peuvent plus être modifiées.'}
        return redirect(f'inscrits/{part.pk}')

    part.first_name = request.POST.get('first_name').title()
    part.last_name = request.POST.get('last_name').upper()
    part.phone_number = request.POST.get('phone_number')
    part.diocese = request.POST.get('diocese')
    part.person_contacter_name = request.POST.get('person_contacter_name')
    part.person_contacter_phone = request.POST.get('person_contacter_phone')
    part.paroisse = request.POST.get('paroisse')
    part.allergies = request.POST.get('allergies')
    part.cni = request.POST.get('cni', None)
    part.age = int(request.POST.get('age'))
    part.polo = request.POST.get('polo')
    part.type = request.POST.get('type')
    part.groupe_sanguin = request.POST.get('groupe_sanguin')
    part.maladies = request.POST.get('maladies')

    if request.POST.get('resizephoto', None) : 
        part.photo = request.POST.get('resizephoto')

    # update occupation du dortoir
    dortoir = None
    if part.paye and part.sexe != request.POST.get('sexe') :
        dortoir = select_dortoir(request.POST.get('sexe'))
        if not dortoir :
            request.session['alerte'] = {'success': False, 'message': f'Enregistrement impossible : Tous les dortoirs {part.sexe} sont occupés  !'}
            return redirect(f'inscrits/{part.pk}')

    # code encadreur
    code = None
    if request.POST.get('encadreur', None) and not part.encadreur :
        try:
            code = CodeEncadreur.objects.get(code = request.POST.get('encadreur'), active = False)
        except CodeEncadreur.DoesNotExist:
            request.session['alerte'] = {'success': False, 'message': f'Code accompagnateur invalide !'}
            return redirect(f'inscrits/{part.pk}')
    
    # enregistrement code accompagnateur
    if code : 
        part.encadreur = code.code
        code.active = True
        code.save()
    
    # enregistrement changement dortoir
    
    if dortoir :
        part.sexe = request.POST.get('sexe')
        part.dortoir.occupation -=1
        part.dortoir.save()
        dortoir.occupation +=1
        dortoir.save()
        part.dortoir = dortoir


    part.save()
    render_pdf_view(part)

    return redirect(f'inscrits/{part.pk}')

def code_generator(diocese: str, id: int): 
    return f'{diocese.split(" ").pop()[:4].upper()}-2022-JNJ-{"0000"[:4-len(str(id))]}{id}'

def render_pdf_view(part: Participant):
    # make qrcode
    qr = qrcode.QRCode(border=0)
    qr.add_data(part.code + (('-' + part.encadreur) if part.encadreur else ''))
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

    # html template
    
    name = part.last_name.split(' ')[0] + ' ' + part.first_name.split(' ')[0]
    name = (name[:15] + '.') if len(name) > 15 else name

    diocese = ' '.join(part.diocese.split(' ')[2:]).upper()

    person_contacter_name = (part.person_contacter_name[:20] + '.') if len(part.person_contacter_name) > 20 else part.person_contacter_name
    context = {
        'qrcode': img_str, 
        'part': part, 
        'name': name, 
        'diocese': diocese,
        'person_contacter_name': person_contacter_name
    }
    template_name = 'accompagnateur.html' if part.encadreur else 'pelerin.html'
    template = get_template(template_name)
    html = template.render(context)

    # fichier pdf
    STATIC_DIR = Path(__file__).resolve().parent / 'static' / 'badges'
    output_filename = STATIC_DIR / f'{part.pk}.pdf'
    result_file = open(output_filename, "w+b")

    # create a pdf
    pisa.CreatePDF(html, dest=result_file)

@login_required(login_url='connexion')
def delete_contact(request, id:int):
    part = Participant.objects.get(pk=id)

    # libération dortoir
    if part.dortoir :
        part.dortoir.occupation -=1
        part.dortoir.save()

    # suppression code accompgnateur
    if part.encadreur : 
        part.encadreur.delete()

    part.delete()
    return redirect('inscrits')

# liste des inscrits
@login_required(login_url='connexion')
def inscrits(request):
    diocese = request.GET.get('diocese', 'Diocèse de Yaoundé')
    person_of_diocese = request.GET.get('person_of_diocese', None)

    if person_of_diocese :
        users = Participant.objects.values(*FIELDS).filter(diocese = person_of_diocese)
    else :
        users = Participant.objects.values(*FIELDS).all().order_by('-pk')

    # répartition pour un diocese
    chart_of_diocese = Participant.objects.filter(diocese = diocese).values('create_date').annotate(total=Count('create_date')).order_by('create_date')
    chart_of_diocese_datas = {'labels': [], 'datas': []}
    for data in chart_of_diocese :
        chart_of_diocese_datas['labels'].append(data.get('create_date').strftime("%d/%m/%Y"))
        chart_of_diocese_datas['datas'].append(data.get('total'))
    
    # evolution générale des inscriptions
    main_chart = Participant.objects.all().values('create_date').annotate(total=Count('create_date')).order_by('create_date')
    main_chart_datas = {'labels': [], 'datas': []}
    for data in main_chart :
        main_chart_datas['labels'].append(data.get('create_date').strftime("%d/%m/%Y"))
        main_chart_datas['datas'].append(data.get('total'))
    
    # repartition par diocese
    chart_by_diocese = Participant.objects.all().values('diocese').annotate(total=Count('diocese')).order_by('diocese')
    chart_by_diocese_datas = {'labels': [], 'datas': []}
    for data in chart_by_diocese :
        chart_by_diocese_datas['labels'].append(data.get('diocese'))
        chart_by_diocese_datas['datas'].append(data.get('total'))
    
    # nombre de carte produite
    produit = Participant.objects.filter(produit = True).annotate(total=Count('pk')).count()

    # nombre de paiement reçu
    paiements = Participant.objects.filter(paye__isnull = False).annotate(total=Count('pk')).count()

    return render(request, 'contacts/inscrits.html', context={
        'users': users,
        'main_chart_datas': main_chart_datas,
        'total': sum(main_chart_datas['datas']),
        'chart_by_diocese_datas': chart_by_diocese_datas,
        'chart_of_diocese_datas': chart_of_diocese_datas,
        'total_diocese': sum(chart_of_diocese_datas['datas']),
        'produit': produit,
        'paiements': paiements,
        'dioceses': DIOCESES, 
        'selectdiocese': diocese,
        'person_of_diocese': person_of_diocese
        })

# récupérer un inscrit
def inscrit(request, id: int):
    part = Participant.objects.get(pk=id)
    # make qrcode
    qr = qrcode.QRCode(border=0)
    qr.add_data(part.code + (('-' + part.encadreur) if part.encadreur else ''))
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

    # gestion alerte
    alerte = request.session.get('alerte', None)
    if alerte :
        del request.session['alerte']
    
    return render(request, 'contacts/inscrit.html', context={
        'person': part, 
        'alerte': alerte,
        'ages': range(15,46),
        'dioceses': DIOCESES, 
        'createdat': part.createat.strftime("%d/%m/%Y %H:%M"),
        'qrcode': img_str,
        'groupes_sangs': GROUPES_SANGUINS
        })

# marquer badge produit
@login_required(login_url='connexion')
def check_badge_produit(request) :
    part = Participant.objects.get(pk=int(request.POST.get('id')))
    part.produit = True
    part.save()
    request.session['alerte'] = {'success': True, 'message': 'Opération effectuée avec succès'}
    return redirect(f'inscrits/{part.pk}')

# supprimer photo badge
def delete_photo(request) :
    part = Participant.objects.get(pk=int(request.POST.get('id')))
    part.photo = None
    part.save()
    # production du badge
    render_pdf_view(part)
    request.session['alerte'] = {'success': True, 'message': 'Photo supprimée !'}
    return redirect(f'inscrits/{part.pk}')

@login_required(login_url='connexion')
def paiement_participant(request, id:int) :

    part = Participant.objects.get(pk=id)

    part.dortoir = select_dortoir(part.sexe)
    # update occupation du dortoir
    if not part.dortoir :
        request.session['alerte'] = {'success': False, 'message': 'Enregistrement impossible : Tous les dortoirs sont occupés !'}
        return redirect(f'inscrits/{part.pk}')

    # enregistrement dortoir
    part.dortoir.occupation +=1
    part.dortoir.save()

    # celui qui valide la réception d'argent
    part.paye = datetime.now().strftime("%d/%m/%Y %H:%M") + 'GMT : ' + request.user.username

    part.save()
    render_pdf_view(part)

    request.session['alerte'] = {'success': True, 'message': 'Paiement enregistré !'}
    return redirect(f'/inscrits/{part.pk}')

# attribution d'un dortoir par sexe
def select_dortoir(sexe):
    dortoirs = [dortoir for dortoir in Dortoire.objects.all() if dortoir.occupation < dortoir.capacite ]
    if len(dortoirs) == 0 :
        return None
    else:
        dortoirs = [dortoir for dortoir in dortoirs if dortoir.site.sexe == sexe]
        if len(dortoirs) == 0 :
            return None
        else:
            return dortoirs[0]
