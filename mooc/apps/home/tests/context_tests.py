import pytest
import os

from django.contrib.auth.models import User, AnonymousUser, Group
from django.test import Client
from mixer.backend.django import mixer


@pytest.fixture
def context_home():

    """
    libelle = mixer.blend(
            'home.Libelles',
            page=page,
            description='titre',
            contenu='Super site web !',
            )
    
    client_nolog = Client()
    client_log = Client()
    groupListNames = ["gestionnaire", "auteur", "adherent"]
    groupList = [Group.objects.create(name=gln) for gln in groupListNames]
    param = {
        'username':'ContextUser',
        'password':'context_pwd',
        }
    user = User.objects.create_user(**param)
    user.groups.set(groupList)
    client_log.login(**param)
    """
    yield {
            'libelle':" ",
            #'client_log':client_log,
            #'client_nolog':client_nolog,
            
            }
    
    # suppression des fichiers de tests de MEDIAROOT :
    """
    if libelle.image:
        os.remove(libelle.image.path)
    if libelle.fichier:
        os.remove(libelle.fichier.path)
    """
