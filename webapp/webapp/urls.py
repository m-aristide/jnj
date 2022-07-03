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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from contacts.user import logout, connexion, login
from contacts.views import index, add_contact, modifier_participant, delete_contact, inscrits 
from contacts.views import inscrit, check_badge_produit, delete_photo, paiement_participant
from dortoires.views import sites, ajouter_site, supprimer_site, supprimer_dortoir
from encadreur.views import encadreurs, creer_code_encadreur, delete_code_encadreur
from organisateurs.views import organisateurs, organisateur, delete_organisateur

urlpatterns = [
    path('users/logout', logout, name='logout'),
    path('users/connexion', connexion, name='connexion'),
    path('users/login', login, name='login'),

    path('', index, name='index'),
    path('inscrits', inscrits, name='inscrits'),
    path('inscrits/add', add_contact, name='add-contact'),
    path('inscrits/update/<int:id>', modifier_participant, name='update-participant'),
    path('inscrits/check-badge-produit', check_badge_produit, name='check-badge-produit'),
    path('inscrits/<int:id>', inscrit, name='inscrit'),
    path('inscrits/paiement/<int:id>', paiement_participant, name='paiement-participant'),
    path('inscrits/delete/<int:id>', delete_contact, name='delete-participant'),
    path('inscrits/delete-photo', delete_photo, name='remove-photo'),

    # encadreurs
    path('encadreurs', encadreurs, name='encadreurs'),
    path('encadreurs/creer', creer_code_encadreur, name='creer-code-encadreur'),
    path('encadreurs/delete', delete_code_encadreur, name='delete-code-encadreur'),
    
    # sites urls
    path('sites', sites, name='sites'),
    path('sites/<int:id>', sites, name='site-edit'),
    path('sites/ajouter-site', ajouter_site, name='ajouter-site'),
    path('sites/supprimer-site', supprimer_site, name='supprimer-site'),
    path('sites/supprimer-dortoir', supprimer_dortoir, name='supprimer-dortoir'),
    path('admin/', admin.site.urls),

    # organisateurs
    path('organisateurs', organisateurs, name='organisateurs'),
    path('organisateur', organisateur, name='organisateur'),
    path('organisateurs/<int:id>', organisateur, name='organisateur_id'),
    path('organisateur/<int:id>', delete_organisateur, name='delete-organisateur')
]

# fichiers static
urlpatterns += staticfiles_urlpatterns()
