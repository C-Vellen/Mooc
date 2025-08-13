from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import Http404
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.utils.text import slugify

from pathlib import Path
from django.core.files import File

from itertools import chain
from operator import attrgetter
from home.context import usercontext
from user.views import is_author, is_gestionnaire
from user.models import Restriction
from progress.models import TutoProgress, PageProgress
from .models import CONTENTTYPE, Category, Tutorial, Page, clone

from .update_data import foreignKeyFields, create_data, update_data


# valeurs des boutons de redirection après création ou mise à jour tuto :
nextValue = {
    "cont": "Enregistrer et continuer les modifications",
    "visu": "Enregistrer et visualiser le tutoriel",
    "back": "Enregistrer et retourner à mon compte",
    "canc": "Annuler les modifications",
    "create": "Créer et ajouter des pages",
    "createback": "Créer et revenir au menu",
    "createcanc": "Annuler et revenir au menu",
}

# identification et statuts possible d'un tutoriel :
titre_auteur = "Vous êtes auteur de ce tutoriel (version V{}) "
titre_gestionnaire = " est auteur de ce tutoriel (version V{}) "
statut = {
    "progress": "non publié, en cours de rédaction",
    "submit": "non publié, soumis au gestionnaire pour publication",
    "publie": "publié, visible par tous",
    "denied": "non publié car rejeté par le gestionnaire",
}


def tutocontext(request):

    context = usercontext(request)
    # état de la progression du tuto pour user (ou création de tutoprogress s'il n'existe pas encore)
    tuto_list = (
        Tutorial.objects.filter(
            Q(published=True)
            # & (Q(restriction__in=request.user.restriction.all()) | Q(restriction=None))
        )
        .order_by("-updated_at")
        .distinct()
    )
    for tuto in tuto_list:
        tp, created = TutoProgress.objects.get_or_create(user=request.user, tuto=tuto)
        if created:
            tp.set_all_pageprogress()

    context.update(
        {
            "titre_tous": "Tous les tutoriels",
            "tutos": tuto_list,
            "tp_list": [],
            "categories": Category.objects.all().order_by("position"),
            "restrictions": Restriction.objects.all().order_by("name"),
            "tuto_form": False,
            "tuto_header": "read",
            "read": True,
        }
    )

    if request.user.is_authenticated:
        context.update(
            {
                "tp_list": request.user.tutoprogress.filter(
                    tuto__in=tuto_list
                ).order_by("-tuto__updated_at")
            }
        )
    else:
        context.update({"tp_list": []})

    return context


# @login_required
def listing(request):
    """liste des vignettes des tutos publies"""
    context = tutocontext(request)
    context.update(
        {
            "titre_onglet": "Les tutoriels",
            "titre_vide": "Aucun tutoriel",
        }
    )

    return render(request, "tuto/listing.html", context)


# @login_required
def listing_cat(request, cat_slug):
    """liste des vignettes des tutos publies d'une même catégorie"""
    context = tutocontext(request)
    category_select = get_object_or_404(Category, slug=cat_slug)
    tuto_select = context["tutos"].filter(category=category_select)  # à supprimer
    tp_list_select = context["tp_list"].filter(Q(tuto__category=category_select))
    context.update(
        {
            "titre_onglet": "tutos " + category_select.name,
            "category_select": category_select,
            "tp_list": tp_list_select,
            "titre_page": "",
            "titre_vide": f"Aucun tutoriel dans la catégorie {category_select.name}.",
        }
    )
    return render(request, "tuto/listing.html", context)


@login_required
@user_passes_test(lambda u: is_author or is_gestionnaire)
def listing_one(request, tuto_slug):
    """visualisation par l'auteur de la vignette d'un tuto en cours de création"""
    tuto = get_object_or_404(Tutorial, slug=tuto_slug)
    context = tutocontext(request)

    tp, created = TutoProgress.objects.get_or_create(user=request.user, tuto=tuto)
    if created:
        tp.set_all_pageprogress()

    if tuto in request.user.tutorial.all():
        context.update(
            {
                "utilisateur": "Auteur",
            }
        )
    elif request.user.is_gestionnaire:
        context.update(
            {
                "utilisateur": "Gestionnaire",
            }
        )

    context.update(
        {
            "titre_onglet": "Les tutoriels",
            "titre_page": "",
            "titre_vide": "Aucun tutoriel",
            "tp_list": [tp],
        }
    )

    return render(request, "tuto/listing.html", context)


# @login_required
def listing_search(request):
    """liste des vignettes des tutos publies suite à recherche"""
    query = request.GET.get("query")
    context = tutocontext(request)
    context.update(
        {
            "titre_onglet": "Le Mooc, recherche dans les tutoriels",
            "titre_vide": f'Désolé, aucun résultat pour la recherche "{query}".',
        }
    )
    tp_list = context["tp_list"]

    if not query:
        context.update(
            {
                "titre_page": "Tous les tutoriels :",
                "tutos": context["tutos"],  # à supprimer
                "tp_list": tp_list,
            }
        )
    else:
        tutos_found = (
            Tutorial.objects.filter(tutoprogress__in=tp_list)
            .filter(
                (Q(title__icontains=query) | Q(resume__icontains=query))
                | Q(page__content__texte__icontains=query)
            )
            .distinct()
        )
        context.update(
            {
                "titre_page": 'Résultat pour la recherche "{}" : {} tutoriel{}.'.format(
                    query, len(tutos_found), "s" * (len(tutos_found) > 1)
                ),
                "tp_list": tp_list.filter(tuto__in=tutos_found),
            }
        )

    return render(request, "tuto/listing.html", context)


# @login_required
def read_tuto(request, tuto_slug, page):
    """
    affichage de la page d'un tutoriel
    """
    # informations sur le tuto et la page à afficher :
    page_number = int(page)
    tuto = get_object_or_404(Tutorial, slug=tuto_slug)

    # le tuto ne peut être affiché que si :
    #       1- il est publie et (l'user fait partie de la liste de restriction d'accès, ou le tuto n'a aucune restriction)
    # ou :  2- son auteur fait la requête
    # ou :  3- un gestionnaire fait la requête

    if (
        tuto
        in Tutorial.objects.filter(
            (
                Q(published=True)
                & (
                    Q(restriction__in=request.user.restriction.all())
                    | Q(restriction=None)
                )
            )
            | (Q(author=request.user))
        )
    ) or (request.user.is_gestionnaire):
        current_page = get_object_or_404(Page, tuto=tuto, page_number=page_number)
    else:
        raise Http404

    # état de la progression du tuto pour user (ou création de tutoprogress s'il n'existe pas encore)
    tp, created = TutoProgress.objects.get_or_create(user=request.user, tuto=tuto)
    if created:
        tp.set_all_pageprogress()
    current_pageprogress = PageProgress.objects.get(
        user=request.user, page=current_page
    )

    if request.method == "POST":
        if current_page.get_all_questions:
            # cas du quiz
            if "redo" in request.POST.keys():
                # demande de recommencer le quiz
                current_pageprogress.finished = False
                current_pageprogress.correction = False
                current_pageprogress.quiztry += 1

            else:
                # validation du quiz
                # enregistrement des réponses :
                PageProgress.register_responses(current_pageprogress, request.POST)
                current_pageprogress.finished = True
                current_pageprogress.correction = False

            current_pageprogress.save()

        else:
            # si pas de quiz :
            # validation page lue :
            current_pageprogress.finished ^= True
            current_pageprogress.save()

    PageProgress.set_all_propositionprogress(
        current_pageprogress, clear="redo" in request.POST.keys()
    )

    context = tutocontext(request)
    if tuto in request.user.tutorial.all():
        context.update(
            {
                "utilisateur": "auteur",
                "titre_page": "Vous êtes " + tuto.get_tuto_status,
            }
        )
    elif is_gestionnaire(request.user):
        context.update(
            {
                "utilisateur": "gestionnaire",
                "titre_page": "<nom de l'auteur>" + " est " + tuto.get_tuto_status,
            }
        )
    else:
        context.update(
            {
                "utilisateur": "adhérent",
            }
        )

    context.update(
        {
            "titre_onglet": tuto.thumbnail,
            "tuto": tuto,
            "current_page": current_page,
            "tp": tp,
            "current_pageprogress": current_pageprogress,
        }
    )

    return render(request, "tuto/read_tuto.html", context)


@login_required
@user_passes_test(is_author)
def create_tuto(request):

    context = tutocontext(request)
    context.update(
        {
            "titre_onglet": "Nouveau tutoriel",
            "username": request.user.username,
            "categories": Category.objects.all().order_by("position"),
            "tuto_restrictions": Restriction.objects.none(),
            "create": nextValue["create"],
            "createback": nextValue["createback"],
            "createcanc": nextValue["createcanc"],
            "tuto_form": True,
            "tuto_header": "create",
        }
    )

    if request.method == "POST":

        if request.POST["next"] == "createcanc":
            return redirect("progress:auteur")

        newtuto = create_data(request)

        if request.POST["next"] == "createback":
            return redirect("progress:auteur")
        elif request.POST["next"] == "create":
            return redirect("tuto:update_tuto", newtuto.slug)

    return render(request, "tuto/create_tuto.html", context)


@login_required
@user_passes_test(is_author)
def update_tuto(request, tuto_slug):

    tuto = get_object_or_404(Tutorial, slug=tuto_slug)
    if request.user not in tuto.author.all():
        return redirect("user:nonautorise")

    context = tutocontext(request)
    context.update(
        {
            "titre_onglet": tuto.thumbnail,
            "tuto": tuto,
            "categories": Category.objects.all(),
            "tuto_restrictions": tuto.restriction.all(),
            "CONTENTTYPES": CONTENTTYPE,
            "cont": nextValue["cont"],
            "visu": nextValue["visu"],
            "back": nextValue["back"],
            "canc": nextValue["canc"],
            "tuto_form": True,
            "tuto_header": "update",
        }
    )

    if request.method == "POST":

        tuto.tutobase.updated_at = timezone.now()
        tuto.tutobase.save()
        tuto.updated_at = timezone.now()
        tuto.in_progress = True
        tuto.submitted = False
        tuto.rejected = False
        tuto.save()

        update_data(request)
        tuto = get_object_or_404(Tutorial, id=tuto.id)

        # redirections vers la page de visualisation ou retour au compte auteur ou continuation sur la page update
        if request.POST["next"] == "visu":
            return redirect("tuto:listing_one", tuto.slug)
        elif request.POST["next"] == "back":
            return redirect("progress:auteur")
        elif request.POST["next"] == "cont":
            return redirect("tuto:update_tuto", tuto.slug)

    return render(request, "tuto/update_tuto.html", context)


login_required


@user_passes_test(lambda u: is_author or is_gestionnaire)
def delete_tuto(request, tuto_slug):
    tuto = get_object_or_404(Tutorial, slug=tuto_slug)
    if request.user in tuto.author.all():
        tuto.delete()
        return redirect("progress:auteur")
    elif request.user.is_gestionnaire:
        tuto.delete()
        return redirect("progress:gestionnaire")
    else:
        return redirect("user:nonautorise")


login_required


@user_passes_test(is_author)
def submit_tuto(request, tuto_slug):
    """soumission d'un tuto au gestionnaire pour
    publication (ou rejet)"""
    tuto = get_object_or_404(Tutorial, slug=tuto_slug)
    if request.user not in tuto.author.all():
        return redirect("user:nonautorise")
    else:
        tuto.in_progress = False
        tuto.submitted = True
        tuto.save()
        return redirect("progress:auteur")


login_required


@user_passes_test(is_gestionnaire)
def reject_tuto(request, tuto_slug):
    tuto = get_object_or_404(Tutorial, slug=tuto_slug)
    tuto.in_progress = False
    tuto.submitted = False
    tuto.rejected = True
    tuto.published = False
    tuto.save()
    return redirect("progress:gestionnaire")


login_required


@user_passes_test(is_gestionnaire)
def publish_tuto(request, tuto_slug):
    """première publication d'un nouveau tuto
    ou republication d'un tuto archivé"""
    tuto = get_object_or_404(Tutorial, slug=tuto_slug)
    tuto.in_progress = False
    tuto.submitted = False
    tuto.rejected = False
    tuto.published = True
    tuto.save()
    # les tutos de version inférieure sont archivés :
    for t in tuto.tutobase.tutorial.filter(version__lt=tuto.version):
        t.archived = True
        t.save()
    return redirect("progress:gestionnaire")


login_required


@user_passes_test(is_gestionnaire)
def archive_tuto(request, tuto_slug):
    """archivage d'un tuto publié"""
    tuto = get_object_or_404(Tutorial, slug=tuto_slug)
    tuto.archived = True
    tuto.save()
    return redirect("progress:gestionnaire")


login_required


@user_passes_test(is_gestionnaire)
def dearchive_tuto(request, tuto_slug):
    """déarchivage d'un tuto publié : possible uniquement s'il n'y a
    pas de version plus récente publiée ou archivée"""
    tuto = get_object_or_404(Tutorial, slug=tuto_slug)
    for t in tuto.tutobase.tutorial.filter(version__gt=tuto.version):
        if t.published or t.archived:
            return redirect("progress:gestionnaire")
    tuto.archived = False
    tuto.save()
    return redirect("progress:gestionnaire")


login_required


@user_passes_test(is_gestionnaire)
def depublish_tuto(request, tuto_slug):
    tuto = get_object_or_404(Tutorial, slug=tuto_slug)
    if tuto.archived:
        tuto.published = False
        tuto.save()
    return redirect("progress:gestionnaire")


login_required


@user_passes_test(is_author)
def duplicate_tuto(request, tuto_slug):
    """duplication d'un tuto, ainsi que toute l'arborescence des related objects,
    conformément à ce qui est défini dans les class models avec les propriété
    get_all_related_objects et méthode set_related_field"""

    tuto = get_object_or_404(Tutorial, slug=tuto_slug)
    tuto = clone(tuto)  # fonction définie dans tuto.models.py

    # incrément de la version et modification du slug (qui doit rester unique)
    new_version = tuto.tutobase.get_last_version + 1
    tuto.version = new_version
    tuto.slug = slugify(tuto.title) + "-" + str(new_version)

    # statut du tuto dupliqué : en cours de rédaction
    tuto.in_progress = True
    tuto.submitted = False
    tuto.rejected = False
    tuto.published = False
    tuto.archived = False

    tuto.save()
    tuto.author.set(
        [
            request.user,
        ]
    )

    return redirect("progress:auteur")
