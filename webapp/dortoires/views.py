from django.shortcuts import redirect, render

from dortoires.models import Site, Dortoire

# Create your views here.
def sites(request, id = None):
    sites = Site.objects.all()

    for site in sites:
        site.dortoirs = [it for it in  Dortoire.objects.filter(site__pk = site.pk).values()]

    # edition d'un site
    site_edit = None
    if id :
        site_edit = [item for item in sites if item.pk == id][0]

    # gestion alerte
    alerte = request.session.get('alerte', None)
    if alerte :
        del request.session['alerte']

    return render(request, 'sites.html', context={'sites': sites, 'alerte': alerte, 'site_edit': site_edit})


def ajouter_site(request) :
    
    site = Site(
        pk = (request.POST.get('id') if request.POST.get('id') != '' else None),
        designation = request.POST.get('designation'),
        description = request.POST.get('description')
    )

    # enregistrement du site
    site.save()

    capacites_names = []
    codes_names = []
    ## construction des dortoirs
    for entry in request.POST.keys(): 
        if 'capacite_' in entry :
            capacites_names.append(entry)
        elif 'code_' in entry :
            codes_names.append(entry)
    
    if len(capacites_names) != 0 :
        capacites_names.sort()
        codes_names.sort()
        dortoirs = []
        for i in range(0, len(capacites_names)):
            # get id 
            index = capacites_names[i].split('_').pop()
            dortoir_existant = request.POST.get('dortoir.id_' + index, None)
            # création ou mise à jour du dortoir
            if dortoir_existant :
                # mise à jour
                dortoir = Dortoire.objects.get(pk = int(dortoir_existant))
                if dortoir.occupation > int(request.POST.get(capacites_names[i])) :
                    request.session['alerte'] = {'success': False, 'message': f'La capacité du dortoir "{request.POST.get(codes_names[i])}" est inférieure à l\'occupation actuelle'}
                    return redirect('sites')
                else:
                    dortoir.capacite = request.POST.get(capacites_names[i])
                    dortoir.code = request.POST.get(codes_names[i])
            else:
                # création
                dortoir = Dortoire(
                    capacite = request.POST.get(capacites_names[i]),
                    code = request.POST.get(codes_names[i]),
                    site = site
                )
            dortoir.save()

    request.session['alerte'] = {'success': True, 'message': 'Site créé'}
    return redirect('sites')

def supprimer_site(request):
    id = int(request.POST.get('id'))
    dortoirs = Dortoire.objects.filter(site__pk = id, occupation__gte = 0)
    if len(dortoirs) > 0 :
        request.session['alerte'] = {'success': False, 'message': 'Impossible de supprimer le site. Ce site contient des dortoirs occupés !'}
        return redirect('sites')
    else:
        site = Site.objects.get(pk = id)
        site.delete()
        request.session['alerte'] = {'success': True, 'message': 'Site supprimé'}
        return redirect('sites')

def supprimer_dortoir(request):
    id = int(request.POST.get('id'))
    dortoir = Dortoire.objects.get(pk = id)
    if dortoir.occupation:
        request.session['alerte'] = {'success': False, 'message': 'Impossible de supprimer ce dortoir car occupé !'}
    else:
        dortoir.delete()
        request.session['alerte'] = {'success': True, 'message': 'Dortoir supprimé'}
    
    return redirect('sites/'+request.POST.get('id_site'))
