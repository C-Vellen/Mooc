from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from user.models import Restriction
from progress.models import TutoProgress, PageProgress
from progress.session import TutoSession
from progress.context import progresscontext
from .models import CONTENTTYPE, Category, Tutorial, Page, clone

from .update_data import create_data, update_data, uniqueSlug
from .permission import permission_check


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


def listing(request):
    """liste des vignettes des tutos publies"""
    context = progresscontext(request)
    context.update(
        {
            "titre_onglet": "Les tutoriels",
            "titre_vide": "Aucun tutoriel",
        }
    )

    return render(request, "tuto/listing.html", context)


def listing_cat(request, cat_slug):
    """liste des vignettes des tutos publies d'une même catégorie"""
    context = progresscontext(request)
    category_select = get_object_or_404(Category, slug=cat_slug)
    if request.user.is_authenticated:
        tp_list_select = context["tp_list"].filter(Q(tuto__category=category_select))
    else:
        tp_list_select = [
            tp for tp in context["tp_list"] if tp.tuto.category == category_select
        ]
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


def listing_one(request, tuto_slug):
    """visualisation de la vignette d'un tuto"""
    
    tuto = get_object_or_404(Tutorial, slug=tuto_slug)
    context = progresscontext(request, display_tuto=True)

    if tuto not in context["tutos"]:
        raise Http404

    tp, created = TutoProgress.objects.get_or_create(user=request.user, tuto=tuto)
    if created:
        tp.set_all_pageprogress()

    context.update(
        {
            "titre_onglet": "Les tutoriels",
            "titre_page": "",
            "titre_vide": "Aucun tutoriel",
            "tp_list": [tp],
            "tuto": tuto,
            "tuto_header": "read",
            "role": request.session.get("role", "auteur"),
        }
    )

    return render(request, "tuto/listing.html", context)


def listing_search(request):
    """liste des vignettes des tutos publies suite à recherche"""
    query = request.GET.get("query")
    context = progresscontext(request)
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
                "tp_list": tp_list,
            }
        )
    else:
        if request.user.is_authenticated:
            queryset = Tutorial.objects.filter(tutoprogress__in=tp_list)
        elif request.user.is_anonymous:
            queryset = Tutorial.objects.filter(id__in=[tp.id for tp in tp_list])

        tutos_found = queryset.filter(
            (Q(title__icontains=query) | Q(resume__icontains=query))
            | Q(page__content__texte__icontains=query)
        ).distinct()

        if request.user.is_authenticated:
            tp_list_found = tp_list.filter(tuto__in=tutos_found)
        elif request.user.is_anonymous:
            tp_list_found = [tp for tp in tp_list if tp.tuto in tutos_found]

        context.update(
            {
                "titre_page": 'Résultat pour la recherche "{}" : {} tutoriel{}.'.format(
                    query, len(tutos_found), "s" * (len(tutos_found) > 1)
                ),
                "tp_list": tp_list_found,
            }
        )

    return render(request, "tuto/listing.html", context)


def read_tuto(request, tuto_slug, page):
    """
    affichage de la page d'un tutoriel
    """

    page_number = int(page)
    tuto = get_object_or_404(Tutorial, slug=tuto_slug)

    # MISE A JOUR DU CONTEXT
    context = progresscontext(request, display_tuto=True)

    # CHARGEMENT DE LA PAGE A AFFICHER
    if tuto in context["tutos"]:
        current_page = get_object_or_404(Page, tuto=tuto, page_number=page_number)
    else:
        raise Http404

    # CHARGEMENT DE LA PROGRESSION DE USER (TutoProgess si user.is_auth, TutoSession si user.is_anonym)
    # état de la progression du tuto pour user (ou création de tutoprogress s'il n'existe pas encore)
    if request.user.is_authenticated:
        tutoprogress, created = TutoProgress.objects.get_or_create(
            user=request.user, tuto=tuto
        )
        if created:
            tutoprogress.set_all_pageprogress()
        current_pageprogress, created = PageProgress.objects.get_or_create(
            user=request.user, page=current_page
        )
    elif request.user.is_anonymous:

        tutoprogress = TutoSession(
            next(tp for tp in request.session["progress"] if tp["id"] == tuto.id)
        )
        current_pageprogress = next(
            pp for pp in tutoprogress.get_all_pageprogress if pp.id == current_page.id
        )

    # SI POST (RETOUR FORMULAIRE QUIZ OU PAGE LUE)
    if request.method == "POST":
        if current_page.get_all_questions:
            # cas du quiz
            if "redo" in request.POST.keys():
                # demande de recommencer le quiz
                current_pageprogress.finished = False
                current_pageprogress.quiztry += 1
            else:
                # validation du quiz et enregistrement des réponses :
                if request.user.is_authenticated:
                    PageProgress.register_responses(current_pageprogress, request.POST)
                current_pageprogress.finished = True
        else:
            # si pas de quiz, validation page lue :
            current_pageprogress.finished ^= True

        # enregistrement des réponses du quiz :
        if request.user.is_authenticated:
            current_pageprogress.save()
        elif request.user.is_anonymous:
            current_pageprogress.update(request.POST, request.session["progress"])
            request.session["progress"] = current_pageprogress.save(
                request.session["progress"]
            )
            tutoprogress.update(request.session["progress"])
            request.session["progress"] = tutoprogress.save(request.session["progress"])

    if request.user.is_authenticated:
        PageProgress.set_all_propositionprogress(
            current_pageprogress, clear="redo" in request.POST.keys()
        )
        

    context.update(
        {
            "titre_onglet": tuto.thumbnail,
            "tp": tutoprogress,
            "tuto": tuto,
            "current_page": current_page,
            "current_pageprogress": current_pageprogress,
            "role": request.session.get("role"),
        }
    )

    return render(request, "tuto/read_tuto.html", context)


@login_required
# @user_passes_test(is_author)
@permission_check
def create_tuto(request, context):
    """ création d'un tuto """
    
    role = request.session.get("role", "auteur")
    if request.method == "POST":

        if request.POST["next"] == "createcanc":
            return redirect("progress:auteur")

        newtuto = create_data(request)

        if request.POST["next"] == "createback":
            return redirect("progress:admin", role)
        elif request.POST["next"] == "create":
            return redirect("tuto:update_tuto", newtuto.slug)

    return render(request, "tuto/create_tuto.html", context)


@login_required
@permission_check
def update_tuto(request, tuto_slug, context):
    """ modification d'un tuto """

    role = request.session.get("role", "auteur")
    tuto = Tutorial.objects.get(slug=tuto_slug)
    
    if request.method == "POST":

        tuto.tutobase.updated_at = timezone.now()
        tuto.tutobase.save()
        tuto.updated_at = timezone.now()
        if not tuto.submitted:
            tuto.in_progress=True
            tuto.rejected = False  
        tuto.save()

        update_data(request)
        tuto = get_object_or_404(Tutorial, id=tuto.id) #????

        # redirections vers la page de visualisation ou retour au compte auteur ou continuation sur la page update
        if request.POST["next"] == "visu":
            return redirect("tuto:listing_one", tuto.slug)
        elif request.POST["next"] == "back":
            return redirect("progress:admin", role)
        elif request.POST["next"] == "cont":
            return redirect("tuto:update_tuto", tuto.slug)

    return render(request, "tuto/update_tuto.html", context)


@login_required
@permission_check
def delete_tuto(request, tuto_slug):
    """ suppression d'un tuto """
    
    role = request.session.get("role", "auteur")
    tuto = Tutorial.objects.get(slug=tuto_slug)   
    tuto.delete()
    return redirect("progress:admin", role)


@login_required
@permission_check
def submit_tuto(request, tuto_slug):
    """soumission d'un tuto au gestionnaire pour publication (ou rejet)"""

    role = request.session.get("role", "auteur")
    tuto = Tutorial.objects.get(slug=tuto_slug)
    tuto.in_progress = False
    tuto.submitted = True
    tuto.save()
    return redirect("progress:admin", role)


@login_required
@permission_check
def reject_tuto(request, tuto_slug):
    """rejet du tuto par le gestionnaire après soumission"""

    role = request.session.get("role", "auteur")
    tuto = Tutorial.objects.get(slug=tuto_slug)
    tuto.in_progress = False
    tuto.submitted = False
    tuto.rejected = True
    tuto.published = False
    tuto.save()
    return redirect("progress:admin", role)


@login_required
@permission_check
def publish_tuto(request, tuto_slug):
    """première publication d'un nouveau tuto ou republication d'un tuto archivé"""

    role = request.session.get("role", "auteur")    
    tuto = Tutorial.objects.get(slug=tuto_slug)
    tuto.in_progress = False
    tuto.submitted = False
    tuto.rejected = False
    tuto.published = True
    tuto.save()
    # les tutos de version inférieure sont archivés :
    for t in tuto.tutobase.tutorial.filter(version__lt=tuto.version):
        t.archived = True
        t.save()
    return redirect("progress:admin", role)


@login_required
@permission_check
def archive_tuto(request, tuto_slug):
    """archivage d'un tuto publié"""

    role = request.session.get("role", "auteur")
    tuto = Tutorial.objects.get(slug=tuto_slug)
    tuto.archived = True
    tuto.save()
    return redirect("progress:admin", role)
    

@login_required
@permission_check
def dearchive_tuto(request, tuto_slug):
    """déarchivage d'un tuto publié """

    role = request.session.get("role", "auteur")
    tuto = Tutorial.objects.get(slug=tuto_slug)
    tuto.archived = False
    tuto.save()
    return redirect("progress:admin", role)



@login_required
@permission_check
def depublish_tuto(request, tuto_slug):
    """ retrait de la publication """

    role = request.session.get("role", "auteur")
    tuto = Tutorial.objects.get(slug=tuto_slug)

    if tuto.archived:
        tuto.published = False
        tuto.save()
    return redirect("progress:admin", role)


@login_required
@permission_check
def duplicate_tuto(request, tuto_slug):
    """duplication d'un tuto, ainsi que toute l'arborescence des related objects,conformément à ce qui est défini dans les class models avec les propriétés get_all_related_objects et méthode set_related_field"""

    role = request.session.get("role", "auteur")
    tuto = Tutorial.objects.get(slug=tuto_slug)

    tuto = clone(tuto)  # fonction définie dans tuto.models.py

    # incrément de la version et modification du slug (qui doit rester unique)
    new_version = tuto.tutobase.get_last_version + 1
    tuto.version = new_version
    # tuto.slug = slugify(tuto.title) + "-" + str(new_version)
    tuto.slug = uniqueSlug(tuto)

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
    return redirect("progress:admin", role)
