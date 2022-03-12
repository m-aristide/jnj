from django.shortcuts import redirect, render
from django.db.models import Count
from django.template.loader import get_template
from pathlib import Path
import io
import base64

from django.urls import reverse

from xhtml2pdf import pisa
import qrcode 

from contacts.models import Participant, CodeEncadreur
from contacts.diocese import DIOCESES
from dortoires.models import Dortoire

# Create your views here.

def index(request):
    return render(request, 'contacts/index.html', context={'dioceses': DIOCESES})

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
            groupe_sanguin = request.POST.get('groupe_sanguin'),
            maladies = request.POST.get('maladies')
        )
    
    if request.POST.get('id', None):
        participant.pk = int(request.POST.get('id'))

    # code encadreur
    if request.POST.get('encadreur', None):
        code = CodeEncadreur.objects.get(code = request.POST.get('encadreur'))
        if code and code.active == False : 
            code.active = True
            participant.encadreur = code.code
            code.save()
    
    if not participant.dortoir:
        participant.dortoir = select_dortoir()
        # update occupation
        participant.dortoir.occupation +=1
        participant.dortoir.save()

    participant.save()

    # code participant
    code = code_generator(participant.diocese, participant.pk)
    if not participant.code == code :
        participant.code = code
        participant.save()
    
    # production du badge
    if not participant.produit :
        render_pdf_view(participant)

    request.session['alerte'] = {'success': True, 'message': 'Opération effectuée avec succès'}
    return redirect(f'inscrits/{participant.pk}')


def code_generator(diocese: str, id: int): 
    return f'{diocese.split(" ").pop()[:4].upper()}-2022-JNJ-{"0000"[:4-len(str(id))]}{id}'

def select_dortoir():
    dortoirs = [dortoir for dortoir in Dortoire.objects.all() if dortoir.occupation < dortoir.capacite ]
    if len(dortoirs) < 0 :
        return None
    else:
        return dortoirs[0]

def render_pdf_view(participant: Participant):
    # make qrcode
    qr = qrcode.QRCode()
    qr.add_data(participant.code)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

    # html template
    template_path = 'user_printer.html'
    name = participant.last_name + ' ' + participant.first_name
    name = (name[:22] + '.') if len(name) > 22 else name
    diocese = ' '.join(participant.diocese.split(' ')[2:])
    person_contacter_name = (participant.person_contacter_name[:20] + '.') if len(participant.person_contacter_name) > 20 else participant.person_contacter_name
    context = {'qrcode': img_str, 'part': participant, 'name': name, 'diocese': diocese, 'person_contacter_name': person_contacter_name}
    template = get_template(template_path)
    html = template.render(context)

    # fichier pdf
    STATIC_DIR = Path(__file__).resolve().parent / 'static' / 'badges'
    output_filename = STATIC_DIR / f'{participant.pk}.pdf'
    result_file = open(output_filename, "w+b")

    # create a pdf
    pisa.CreatePDF(html, dest=result_file)

def delete_contact(request, id:int):
    part = Participant.objects.get(pk=id)
    part.delete()
    return redirect('index')

def inscrits(request):
    diocese = request.GET.get('diocese', 'Diocèse de Yaoundé')
    person_of_diocese = request.GET.get('person_of_diocese', None)

    if person_of_diocese :
        users = Participant.objects.filter(diocese = person_of_diocese)
    else :
        users = Participant.objects.all().order_by('-pk')

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

    return render(request, 'contacts/inscrits.html', context={
        'users': users,
        'main_chart_datas': main_chart_datas,
        'total': sum(main_chart_datas['datas']),
        'chart_by_diocese_datas': chart_by_diocese_datas,
        'chart_of_diocese_datas': chart_of_diocese_datas,
        'total_diocese': sum(chart_of_diocese_datas['datas']),
        'produit': produit,
        'dioceses': DIOCESES, 
        'selectdiocese': diocese,
        'person_of_diocese': person_of_diocese
        })

def inscrit(request, id: int):
    part = Participant.objects.get(pk=id)
    # make qrcode
    qr = qrcode.QRCode()
    qr.add_data(part.code)
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
        'dioceses': DIOCESES, 
        'createdat': part.createat.strftime("%d/%m/%Y %H:%M"),
        'qrcode': img_str
        })

def check_badge_produit(request) :

    part = Participant.objects.get(pk=int(request.POST.get('id')))
    part.produit = True
    part.save()
    request.session['alerte'] = {'success': True, 'message': 'Opération effectuée avec succès'}
    return redirect(f'inscrits/{part.pk}')


