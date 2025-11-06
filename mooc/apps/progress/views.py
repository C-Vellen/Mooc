from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from progress.context import progresscontext
from home.context import homecontext
from user.views import is_author, is_gestionnaire
from tuto.models import TutoBase, Tutorial, Category
from tuto.update_data import update_data
from .session import TutoSession
from .models import TutoProgress


def compte(request):
    """page du compte"""
    context = progresscontext(request)
    if request.user.is_authenticated:
        context.update(
            {
                "author_link": request.user.is_author,
                "gestionnaire_link": request.user.is_gestionnaire,
                "titre_compte": f"Compte personnel de {request.user.first_name} {request.user.last_name}",
                "connexion_link": False,
            }
        )
    elif request.user.is_anonymous:
        tp_list = [TutoSession(tp) for tp in request.session["progress"]]
        context.update(
            {
                "author_link": False,
                "gestionnaire_link": False,
                "titre_compte": "Compte invité",
                "connexion_link": True,
            }
        )

    context.update(
        {
            "titre_onglet": "Mon compte",
            "tuto_form": False,
            "tuto_header": "progress",
        }
    )
    return render(request, "progress/compte.html", context)


@login_required
@user_passes_test(is_author)
def auteur(request):
    """page du compte 'auteur' permettant de voir/modifier/créer un tuto"""
    context = homecontext(request)
    context.update(
        {
            "titre_onglet": "Mon compte Auteur",
            "tutobases": [
                tb for tb in TutoBase.objects.all() if tb.has_author(request.user)
            ],
            "tuto_form": False,
            "tuto_header": "admin",
            "author_link": False,
            "gestionnaire_link": request.user.is_gestionnaire,
        }
    )
    return render(request, "progress/tuto_admin_auteur.html", context)


@login_required
@user_passes_test(is_gestionnaire)
def gestionnaire(request):
    """
    page du compte 'gestionnaire' permettant de :
    - créer/modifier/supprimer une catégorie
    - voir/valider/publier/rejeter/archiver/supprimer un tuto
    """
    context = homecontext(request)
    context.update(
        {
            "titre_onglet": "Mon compte Gestionnaire",
            "categories": Category.objects.all().order_by("position"),
            "tutobases": TutoBase.objects.all(),
            "tuto_form": False,
            "tuto_header": "admin",
            "author_link": request.user.is_author,
            "gestionnaire_link": False,
        }
    )

    # création, modif ou suppression d'une catégorie:
    if request.method == "POST":
        res_post = request.POST
        update_data(request)
        return redirect("progress:gestionnaire")

    return render(request, "progress/tuto_admin_gestionnaire.html", context)
