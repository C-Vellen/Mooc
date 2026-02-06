from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from progress.context import progresscontext
from tuto.permission import permission_check
from .session import TutoSession



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
@permission_check
def admin(request, role, context):
    """page du compte adlinistration des tutoriels permettant de les créer/modifier/publier/archiver/supprimer"""
    return render(request, "progress/tuto_admin.html", context)


