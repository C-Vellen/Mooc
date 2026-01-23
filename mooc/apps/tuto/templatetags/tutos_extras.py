from datetime import datetime
from django import template
from django.http import Http404
from mooc.settings import MEDIA_URL
from home.models import default_image_url, default_video_url
# from home.models import Libelles, DefaultContent
# from user.models import Restriction
# from tuto.models import Page, Content, Question, Proposition

register = template.Library()


@register.filter
def break_line(content):
    return content.replace("\n", "<br/>")


@register.filter
def multiresponse(question):
    if question.multiresponse:
        return "multiresponse"
    return "uniqueresponse"


# mise en forme des scores et notations :
@register.filter
def ordinal(n):
    if n == 1:
        return "1ère"
    return f"{n}ème"


@register.filter
def question_notation(qp):
    return "{} point".format(qp.question_score)


@register.filter
def tuto_progression(tutoprogress):
    try:
        return "{:.0f} %".format(
            100
            * tutoprogress.get_page_finished
            / tutoprogress.tuto.get_pages_total_number
        )
    except (ZeroDivisionError, AttributeError):
        return "-"


@register.filter
def page_notation(pageprogress):
    if pageprogress.page_max_score > 0:
        page_score = "-"
        if pageprogress.finished:
            page_score = pageprogress.page_score
        return "{} / {}".format(page_score, pageprogress.page_max_score)
    else:
        return "-"


@register.filter
def tuto_notation(tutoprogress):
    if tutoprogress.tuto_max_score_done > 0:
        return "{} / {}".format(
            tutoprogress.tuto_score, tutoprogress.tuto_max_score_done
        )
    else:
        return "-"


# récupération des images :
@register.filter
def find_img(content):
    """recherche de l'image associée au contenu dans la BD, et de l'image par défaut si pas d'image"""
    try:
        return content.image.url
    except (AttributeError, ValueError):
        return MEDIA_URL + default_image_url()


# récupération des fichiers :
@register.filter
def find_file(content):
    """recherche du fichier associée au contenu dans la BD"""
    try:
        return content.fichier.url
    except (AttributeError, ValueError):
        return ""


# récupération des videos :
@register.filter
def find_video(content):
    """recherche du fichier associée au contenu dans la BD"""
    try:
        return content.video.url
    except (AttributeError, ValueError):
        return MEDIA_URL + default_video_url()


# définition des <input name=" ... "> pour les champs de l'objet tuto

@register.filter
def input_image(tuto, tuto_header):
    return "{}-tutorial-{}-image".format(tuto_header, get_id(tuto))


@register.filter
def input_category(tuto, tuto_header):
    return "{}-tutorial-{}-category".format(tuto_header, get_id(tuto))


@register.filter
def input_restriction(tuto, tuto_header):
    return "{}-tutorial-{}-restriction".format(tuto_header, get_id(tuto))


@register.filter
def input_title(tuto, tuto_header):
    return "{}-tutorial-{}-title".format(tuto_header, get_id(tuto))


@register.filter
def input_resume(tuto, tuto_header):
    return "{}-tutorial-{}-resume".format(tuto_header, get_id(tuto))


def get_id(tuto):
    try:
        return tuto.id
    except AttributeError:
        # si nouveau tuto (pas d'id):
        return "xx"


@register.filter
def tuto_author(tuto, user):
    try:
        return tuto.get_author_names
    except AttributeError:
        return "Auteur: {} {}".format(user.first_name, user.last_name)


@register.filter
def tuto_date(tuto):
    try:
        return "Publié le {}".format(tuto.updated_at.strftime("%d/%m/%y"))
    except AttributeError:
        return "Publié le {}".format(datetime.today().strftime("%d/%m/%y"))


@register.filter
def call_to_read(tp, tuto_header):
    """Libellé du bouton d'action de l'en-tête tuto"""
    try:
        return tp.call_to_read
    except AttributeError:
        if tuto_header == "read":
            return "Démarrer"
        else:
            return ""


@register.filter
def groups_list(user):
    """liste des restrictions appliquées au user"""
    if user.groups.count() > 1:
        return f"Groupes : {user.get_groups()}"
    elif user.groups.count() == 1:
        return f"Groupe : {user.get_groups()}"
    else:
        return ""


@register.filter
def initiales(user):
    """renvoie les initiales de user"""
    if user.is_anonymous:
        return "👤"
    else:
        try:
            first = user.first_name[0].upper()
        except IndexError:
            first = ""
        try:
            last = user.last_name[0].upper()
        except IndexError:
            last = ""
        return first + last
