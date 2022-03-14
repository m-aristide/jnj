"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from contacts.views import index, add_contact, modifier_participant, delete_contact, inscrits, inscrit, check_badge_produit
from dortoires.views import sites, ajouter_site, supprimer_site, supprimer_dortoir
from contacts.views_encadreurs import encadreurs, creer_code_encadreur, delete_code_encadreur

urlpatterns = [
    path('', index, name='index'),
    path('add', add_contact, name='add-contact'),
    path('update', modifier_participant, name='update-participant'),
    path('check-badge-produit', check_badge_produit, name='check-badge-produit'),
    path('inscrits/', inscrits, name='inscrits'),
    path('inscrits/<int:id>', inscrit, name='inscrit'),
    path('delete/<int:id>', delete_contact, name='delete-contact'),

    # encadreurs
    path('encadreurs', encadreurs, name='encadreurs'),
    path('encadreurs/creer', creer_code_encadreur, name='creer-code-encadreur'),
    path('encadreurs/delete', delete_code_encadreur, name='delete-code-encadreur'),
    
    # sites urls
    path('sites', sites, name='sites'),
    path('sites/<int:id>', sites, name='site-edit'),
    path('ajouter-site', ajouter_site, name='ajouter-site'),
    path('supprimer-site', supprimer_site, name='supprimer-site'),
    path('supprimer-dortoir', supprimer_dortoir, name='supprimer-dortoir'),
    path('admin/', admin.site.urls),
]
