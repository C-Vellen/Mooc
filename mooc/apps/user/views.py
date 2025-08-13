import re
from string import digits, ascii_letters
from random import choice, randint
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.core import management
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError

from user.OpenID import OpenId
from mooc.settings import DEBUG, GROUPNAMES
from home.models import Libelles
from .forms import ConnexionForm
from .models import User, Restriction


def deconnexion(request):
    print("============= LOGOUT ===============")
    logout(request)
    return redirect("home:index")


def connexion(request):
    """
    Vue permettant de se connecter
    """

    # suppression des sessions expirées :
    management.call_command("clearsessions")

    context = {lib.description: lib for lib in Libelles.objects.all()}
    context.update(
        {
            "titre_onglet": "connexion",
            "user_still_exists": False,
            "authentication_fail": False,
        }
    )

    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            # récupération des données du formulaire :
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            new = form.cleaned_data["new"]
            email = ""
            # cas 1 : création d'un nouvel utilisateur :
            if new:
                # si l'utilisateur existe déjà, retour au formulaire avec message d'erreur :
                if User.objects.filter(username=username).exists():
                    user = None
                    context.update({"user_still_exists": True})
                    context.update({"form": form})
                    return render(request, "user/connexion.html", context)

                # si le username n'est pas déjà pris, on peut créer un nouvel utilisateur :
                else:
                    # création prénom nom à partir du username :
                    split_username = re.split(r"[-_ ]", username, maxsplit=1)
                    first_name = split_username[0]
                    if len(split_username) == 1:
                        last_name = ""
                    else:
                        last_name = split_username[-1]
                    # création subId (identifiant unique du user)
                    doublon = True  # garantir l'unicité du subId
                    while doublon:
                        subId = "".join(
                            [choice(digits + ascii_letters) for i in range(5)]
                        )
                        doublon = subId in [u.subId for u in User.objects.all()]
                    # création du user :
                    user = User.objects.create_user(
                        username,
                        email,
                        password,
                        first_name=first_name,
                        last_name=last_name,
                        subId=subId,
                        # restriction=None,
                    )
                    user.groups.set([Group.objects.get(name="utilisateur")])
                    user.restriction.set([])
                    user.save()

                    print("....................................")
                    print(
                        "new user is created:", user, "| auth?:", user.is_authenticated
                    )
                    print("....................................")

            # cas 2 : authentification d'un utilisateur existant :
            else:
                try:
                    user = authenticate(username=username, password=password)
                    print("....................................")
                    print(
                        "user is authenticated:",
                        user,
                    )
                    print("....................................")

                except PermissionDenied:
                    # context.update({"password_not_valid": True})
                    context.update({"authentication_fail": True})

            if user == None:
                print("user: NONE")
                context.update({"authentication_fail": True})
            else:
                # Création / Mise à jour de la session :
                print("LOGIN >>>>>>>>>>>")
                login(request, user)
                userinfo = {
                    "subid": user.subId,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "group": [g.name for g in user.groups.all()],
                    "restriction": [r.name for r in user.restriction.all()],
                }
                request.session["user"] = userinfo
                # utilisateur authentifié : session expire après 1 jour
                request.session.set_expiry(24 * 3600)

    else:
        form = ConnexionForm()
    titre_onglet = "connexion"
    context.update({"form": form})
    return render(request, "user/connexion.html", context)


def is_author(user):
    return user.is_author


def is_gestionnaire(user):
    return user.is_gestionnaire


def nonautorise(request):
    raise PermissionDenied
