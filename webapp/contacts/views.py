from django.shortcuts import redirect, render
from django.db.models import Count

from api.diocese import DIOCESES
from contacts.models import Participant

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
            paroisse = request.POST.get('paroisse')
        )
    
    if request.POST.get('id', None):
        participant.pk = int(request.POST.get('id'))
    
    participant.save()
    return redirect(f'inscrits/{participant.pk}')

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
        users = Participant.objects.all()

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

    return render(request, 'contacts/inscrits.html', context={
        'users': users,
        'main_chart_datas': main_chart_datas,
        'total': sum(main_chart_datas['datas']),
        'chart_by_diocese_datas': chart_by_diocese_datas,
        'chart_of_diocese_datas': chart_of_diocese_datas,
        'total_diocese': sum(chart_of_diocese_datas['datas']),
        'dioceses': DIOCESES, 
        'selectdiocese': diocese,
        'person_of_diocese': person_of_diocese
        })

def inscrit(request, id: int):
    part = Participant.objects.get(pk=id)
    return render(request, 'contacts/inscrit.html', context={'person': part, 'dioceses': DIOCESES})