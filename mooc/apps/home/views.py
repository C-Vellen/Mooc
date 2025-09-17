from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tuto.views import tutocontext
from .context import usercontext


# @login_required
def index(request):
    context = tutocontext(request)
    context.update(
        {
            "titre_onglet": "Le Mooc",
            "titre_vide": "Aucun tutoriel",
        }
    )

    try:
        from mooc.variables_environnement import env, djangoSettings

        env()
        djangoSettings()
    except ModuleNotFoundError:
        pass

    # test de modification de session :
    if request.user.is_authenticated:
        print(">>>>>>>>>>>> Authentifié ! <<<<<<<<<<<<<<")
    else:
        print(">>>>>>>>>>>> Non Authentifié ! <<<<<<<<<<<<<<")
        try:
            request.session["count"] += 1
        except KeyError:
            request.session["count"] = 0

    return render(request, "home/index.html", context)
