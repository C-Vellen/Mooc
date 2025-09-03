from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from home.context import usercontext
from user.views import is_author, is_gestionnaire
from tuto.models import TutoBase, Tutorial, Category
from tuto.update_data import update_data
from .models import TutoProgress


def compte(request):
    context = usercontext(request)
    context.update(
        {
            "titre_onglet": "Mon compte",
            "tuto_form": False,
            "tuto_header": "progress",
        }
    )
    if request.user.is_authenticated:
        print("---> user is authenticated")
        context.update(
            {
                "tp_list": request.user.tutoprogress.all(),
                "author_link": request.user.is_author,
                "gestionnaire_link": request.user.is_gestionnaire,
                "connexion_link": False,
            }
        )
    else:
        print("---> user is NOT authenticated")
        tuto_list = (
            Tutorial.objects.filter(published=True).order_by("-updated_at").distinct()
        )
        context.update(
            {
                "tp_list": [{"tuto": tuto} for tuto in tuto_list],
                "author_link": False,
                "gestionnaire_link": False,
                "connexion_link": True,
            }
        )

    return render(request, "progress/compte.html", context)

    # return redirect("user:connexion")


@login_required
@user_passes_test(is_author)
def auteur(request):
    """page du compte 'auteur' permettant de voir/modifier/créer un tuto"""
    context = usercontext(request)
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
    context = usercontext(request)
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
