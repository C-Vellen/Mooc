from django.db.models import Q

from pathlib import Path

from home.context import homecontext
from user.models import Restriction
from progress.models import TutoProgress
from progress.session import progress_init, TutoSession
from tuto.models import Category, Tutorial


def tuto_authorized_list(request, display_tuto) -> list:
    """LISTE DES TUTOS AUTORISES :
        - dans les listes de tutos (si display_tuto=False)
        - à l'affichage (si display_tuto=True)
    le tuto ne peut être affiché que si :
          1- il est publie et (l'user fait partie de la liste de restriction d'accès, ou le tuto n'a aucune restriction)
    ou :  2- son auteur fait la requête
    ou :  3- un gestionnaire fait la requête
    """
    if request.user.is_anonymous:
        tuto_authorized_list = (
            Tutorial.objects.filter(Q(published=True) & Q(restriction=None))
            .order_by("-updated_at")
            .distinct()
        )

    elif request.user.is_authenticated:
        tuto_authorized_list = (
            Tutorial.objects.filter(
                Q(published=True)
                & (
                    Q(restriction__in=request.user.restriction.all())
                    | Q(restriction=None)
                )
            )
            .order_by("-updated_at")
            .distinct()
        )
        if display_tuto and request.user.is_gestionnaire:
            tuto_authorized_list = Tutorial.objects.all()
        elif display_tuto and request.user.is_author:
            tuto_authorized_list = tuto_authorized_list.union(
                Tutorial.objects.filter(author=request.user)
            )
    return tuto_authorized_list


def progresscontext(request, display_tuto=False):

    context = homecontext(request)
    # état de la progression du tuto pour user (ou création de tutoprogress s'il n'existe pas encore)

    tuto_list = tuto_authorized_list(request, display_tuto=display_tuto)

    if request.user.is_authenticated:
        for tuto in tuto_list:
            tp, created = TutoProgress.objects.get_or_create(
                user=request.user, tuto=tuto
            )
            if created:
                tp.set_all_pageprogress()

        context.update(
            {
                "tp_list": request.user.tutoprogress.filter(
                    tuto__in=tuto_list
                ).order_by("-tuto__updated_at")
            }
        )

    elif request.user.is_anonymous:
        try:
            progress = request.session["progress"]
        except KeyError:
            request.session["progress"] = progress_init(tuto_list)
            progress = request.session["progress"]

        context.update({"tp_list": [TutoSession(tp) for tp in progress]})

    context.update(
        {
            "titre_tous": "Tous les tutoriels",
            "tutos": tuto_list,
            "categories": Category.objects.all().order_by("position"),
            "restrictions": Restriction.objects.all().order_by("name"),
            "tuto_form": False,
            "tuto_header": "read",
            "read": True,
        }
    )

    return context
