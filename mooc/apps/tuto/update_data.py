import re
from random import randint
from django.utils.text import slugify
from .models import modelClass
from .parse_post import parse_post, debugPrint, foreignKeyFields, manytomanyFields


# liste des champs ForeignKey par model, afin de transformer l'id provisoire de la foreign key en instance :
# foreignKeyFields = { model.__name__ .lower(): [
#    field.name for field in model._meta.get_fields() if field.__class__.__name__ in["ForeignKey", "OneToOneField"] #and field.name in modelClass.keys()
#    ] for model in modelClass.values() }


def uniqueSlug(newtuto):
    """construit le slug d'un tuto en garantissant son unicité : titre-xxxx-version"""
    rootSlug = slugify(newtuto.title)[:40]
    suffixSlug = f"-{newtuto.version}"
    slugList = [
        t.slug for t in modelClass["tutorial"].objects.all()
    ]
    doublon = True
    while doublon:
        newSlug = rootSlug + suffixSlug
        doublon = newSlug in slugList
        suffixSlug = f"-{randint(1000, 9999)}-{newtuto.version}"
    return newSlug


def create_data(request):
    """crée un nouveau tutoriel (objet Tutorial) à partir du request.POST et l'enregistre en BD"""
    res_post, res_files = parse_post(request.POST, request.FILES)

    # ------ IMPRESSIONS POUR DEBUGGER : -------------------------------------
    # debugPrint(res_post, res_files)
    # ------------------------------------------------------------------------

    # dictionnaire de la nouvelle instance, exceptée les mantomanyfields qui doivent être traitée après initialisation de l'instance
    newinst = {
        f: v
        for f, v in list(res_post["create"]["tutorial"].values())[0].items()
        if f not in manytomanyFields["tutorial"]
    }

    # cas d'un champ ForeignKey (category, tutobase), remplacement de l'id par l'instance de la clé :
    for f, val in newinst.items():
        if f in foreignKeyFields["tutorial"]:
            newinst.update({f: modelClass[f].objects.get(id=val)})

    # intialisation de l'instance (excepté les manytomanyfields)
    newtuto = modelClass["tutorial"](**newinst)

    # initialisation des slug et thumbnail :
    newtuto.slug = uniqueSlug(newtuto)
    newtuto.thumbnail = newtuto.title[:20]

    # initialisation des fichiers (image ou file) :
    try:
        uploaded_file = list(res_files["create"]["tutorial"].values())[0]["image"]
        setattr(newtuto, "image", uploaded_file)
    except (IndexError, KeyError):  # s'il n'y a pas d'image enregistrée
        pass

    # initialisation du tutobase (pour pouvoir gérer ultérieurement les versions) :
    tutobase = modelClass["tutobase"](name=newtuto.title)
    tutobase.save()
    newtuto.tutobase = tutobase

    # création de l'instance et enregistrement dans la bd (nécessaire avant d'initaliser les manytomanyfields)
    newtuto.save()

    # initialisation des manytomanyfields :
    try:
        restriction_list = list(res_post["create"]["tutorial"].values())[0][
            "restriction"
        ]
    except KeyError:
        restriction_list = list()
    newtuto.restriction.set(restriction_list)
    newtuto.author.set(
        [
            request.user,
        ]
    )
    newtuto.save()

    return newtuto


def update_data(request):
    """met à jour à partir de request.POST les champs des objets Tutorial, Page, Content, ListItem, Category, Question, Proposition"""

    # analyse de request.POST/.FILES : décomposition en dictionnaire exploitable p
    res_post, res_files = parse_post(request.POST, request.FILES)

    # impression des dictionnaire dans la console pour debugger
    # debugPrint(res_post, res_files)

    # UPDATE: sauvegarde des données modifiées :

    # update des instances (excepté les images/filefields)
    for mod, coll in res_post["update"].items():
        for i, inst in coll.items():

            instance = modelClass[mod].objects.filter(id=i)
            if instance.first():
                # update de l'instance (excepté manytomanyfields)

                if mod == "tutorial":
                    old_title = instance.first().title
                if mod == "category":
                    old_name = instance.first().name

                inst_without_manytomanyfields = {
                    f: v for f, v in inst.items() if f not in manytomanyFields[mod]
                }
                instance.update(**inst_without_manytomanyfields)

                # update du tutoriel pour changement de slug si le titre a changé, et pour le manytomanyfields "Tutorial.restriction"
                if mod == "tutorial":
                    if instance.first().title != old_title:
                        instance.update(slug=uniqueSlug(instance.first()))
                    try:
                        restriction_list = inst["restriction"]
                    except KeyError:
                        restriction_list = list()
                    instance.first().restriction.set(restriction_list)
                    instance.first().save()

                # update de la catégorie pour changement de slug si le nom a changé
                if mod == "category":
                    if instance.first().name != old_name:
                        instance.update(slug=slugify(instance.first().name))

    # update des instances pour les images/filefields
    for mod, coll in res_files["update"].items():
        for i, inst in coll.items():
            for field, uploaded_file in inst.items():
                try:
                    instance = modelClass[mod].objects.get(id=i)
                    setattr(instance, field, uploaded_file)
                    instance.save()
                except modelClass[mod].DoesNotExist:
                    pass

    # CREATE: création des données nouvelles :

    # correspondance id provisoire / id final pour attribution des clés étrangères :
    corres = {m: dict() for m in modelClass}

    for mod, coll in res_post["create"].items():
        for i, inst in coll.items():
            # mise à jour du dictionnaire inst pour remplacer les id provisoires des champs 'foreignKey'
            # par les vrais id des clés.
            newinst = inst.copy()
            for f, val in inst.items():
                if f in foreignKeyFields[mod]:  # cas d'un champ clé étrangère
                    if "new" in val:  # nouvelle clé étrangère (nouvelle page...)
                        newinst.update(
                            {
                                f: modelClass[f].objects.get(
                                    id=corres[f][val.replace("new-", "")]
                                )
                            }
                        )
                    else:  # clé étrangère existante :
                        newinst.update(
                            {f: modelClass[f].objects.get(id=val.replace("new-", ""))}
                        )
            newinstance = modelClass[mod](**newinst)
            try:
                for field, uploaded_file in res_files["create"][mod][i].items():
                    setattr(newinstance, field, uploaded_file)
            except KeyError:
                pass

            # création du slug pour le model 'Category'
            if mod == "category":
                newinstance.slug = slugify(newinstance.name)

            newinstance.save()
            corres[mod].update({i: newinstance.id})

    # DELETE: suppression des données :
    for m, v in res_post["delete"].items():
        for i in v.keys():
            try:
                modelClass[m].objects.filter(id=i).delete()
            except ValueError:
                # cas de suppression d'un content entrainant la suppression d'un sous-content qui vient d'être créé et n'a donc pas d'id dans le dictionnaire request.POST (ex : suppression d'une Question dont on vient de créer une Proposition non encore enregistrée)
                pass
