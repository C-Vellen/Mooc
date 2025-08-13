import os
from pathlib import Path
from datetime import date
from itertools import chain
from operator import attrgetter

from django.core.files import File
from django.db import models
from django.db.models import Q
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.utils import timezone
from mooc.media_file_cleaning import auto_delete_file_on_delete, auto_delete_file_on_change
from user.models import User

CONTENTTYPE = (
        ('TI', 'Titre'),
        ('ST', 'Sous-titre'),
        ('PA', 'Paragraphe'),
        ('IM', 'Image'),
        ('VI', 'Video'),
        ('LI', 'Liste'),
    )


class Tutorial(models.Model):

    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="tutorial")
    author = models.ManyToManyField(User, related_name="tutorial")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, blank=True)
    image = models.ImageField(upload_to="tuto/images/", blank=True)
    resume = models.TextField(max_length=2000)
    restriction = models.ManyToManyField('user.Restriction', related_name="tutorial", blank=True)


    # date de création, renseignée automatiquement, non modifable
    # n'apparait pas sur le site, uniquement dans l'administration
    created_at = models.DateField(auto_now_add=True, verbose_name='date de création')
    
    # date de mise à jour. Peut être modifiée dans l'interface d'administration.
    updated_at = models.DateTimeField(default=timezone.now, verbose_name='date de mise à jour')

   # booleens pour décrire les états d'un tutoriel : 
    in_progress = models.BooleanField(default=True)
    submitted = models.BooleanField(default=False) 
    rejected = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    # base et version du tuto :
    tutobase = models.ForeignKey("TutoBase", on_delete=models.CASCADE, related_name="tutorial")
    version = models.IntegerField(default=0)

    # titre qui apparaitra dans la balise title (dans l'onglet du navigateur) :
    thumbnail = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = "tutoriel"
        ordering = ['created_at']
        permissions = (
                ("publie_tuto", "rendre un tutoriel public"),
                )

    @property
    def get_pages_total_number(self):
        """ nombre total de pages du tuto"""
        return len(self.get_all_pages)

    @property
    def get_all_pages(self):
        """ liste de toutes les pages du tuto, triées selon leur numéro """
        return Page.objects.filter(tuto=self).order_by('page_number')
    
    @property
    def get_all_related_objects(self):
        """ liste de tous les objets qui ont une relation et que l'on souhaite dupliquer """
        return Page.objects.filter(tuto=self)
        
    @property
    def get_all_contents(self):
        """ liste de tous les contenus du tuto"""
        return Content.objects.filter(page__tuto=self)

    @property
    def get_all_questions(self):
        """ liste de toutes les questions du tuto"""
        return Question.objects.filter(page__tuto=self)
  
    @property
    def get_all_propositions(self):
        """ liste de toutes les propositions du tuto"""
        return Proposition.objects.filter(question__page__tuto=self)
  
    @property
    def get_questions_number(self):
        """ Nombre total de questions dans un tuto (dénominateur de la note)"""
        #return sum([p.get_questions_number for p in self.get_all_pages])
        return len(self.get_all_questions)

    @property
    def get_tuto_status(self):
        # identification et statuts possible d'un tutoriel :
        titre = 'V{} '.format(self.version)        
        status = {
            'non publiée':  not self.published,
            'en cours':     self.in_progress,
            'soumise':      self.submitted,
            'rejetée':      self.rejected,
            'publiée':      self.published,
            'archivée':     self.archived,
        }
        return titre + ' '.join([com*boo for com, boo in status.items()])
    
    @property
    def is_last_version(self):
        """Le tuto est la dernière version, ce qui autorise à créer une nouvelle
        version à partir de ce tuto (permet d'éviter de créer des versions parallèles)"""

        return self.tutobase.get_last_version == self.version
    
    @property
    def is_last_published_or_archived_version(self):
        """Le tuto est la dernière version publiée ou archivée de la tutobase, ce qui autorise à créer une nouvelle
        version à partir de ce tuto (permet d'éviter de créer des versions parallèles)"""

        return self.tutobase.get_last_published_or_archived_version == self.version
    
    @property
    def get_author_names(self):
        """Texte de présentation du ou des auteurs """
        authorlist = [ "{} {}".format(t.first_name, t.last_name) for t in self.author.all() ]
        if len(authorlist) == 1 :
            return "Auteur : " + authorlist[0]
        elif len(authorlist) >= 2:
            return "Auteurs : " + ", ".join(authorlist[:-1]) + " et " + authorlist[-1]
    
    @property
    def get_restrictions(self):
        return self.restriction.all()

    def __str__(self):
        return self.title

    def get_file(self):
        """ liste des fichiers media, pour gérer leur mise à jour et suppression """
        return [self.image] 


class TutoBase(models.Model):
    """ classe de tutos permettant d'y rattacher les différentes versions d'un tuto"""
    name = models.CharField(max_length=200, default="TutoBase")
    
    # date de mise à jour. Peut être modifiée dans l'interface d'administration.
    updated_at = models.DateTimeField(default=timezone.now, verbose_name='date de mise à jour')


    @property
    def get_all_tutos(self):
        return Tutorial.objects.filter(tutobase=self).order_by('-version')

    @property
    def get_last_version(self):
        return max([0]+[tuto.version for tuto in self.tutorial.all()])
    
    @property
    def get_last_published_or_archived_version(self):
        return max([-1]+[tuto.version for tuto in self.tutorial.filter(Q(published=True) | Q(archived=True))])
    
    @property
    def get_creation_date(self):
        return max([tuto.created_at for tuto in self.tutorial])

    def has_author(self, user):
        return self.tutorial.filter(author__in=[user])
    

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-updated_at']
     
    

class Page(models.Model):
    """ une page d'un contenu : contient des content et à la fin peu contenir 0 ou 1 quiz """

    tuto = models.ForeignKey('Tutorial', on_delete=models.CASCADE)
    page_number = models.IntegerField(verbose_name="Page")
    page_title = models.CharField(max_length=200, verbose_name="Titre")
    
    class Meta:
        verbose_name = "page"
        ordering = ['page_number']
    
    @property
    def get_all_contents(self):
        """
        liste des contenus de page, triés selon leur position
        en excluant les contents de type 'image' dont le champ image est vide 
        pour éviter l'erreur d'exécution du html : ValueError: The 'image' attribute has no file associated with it
        """
        # return Content.objects.filter(page=self).exclude(contenttype='IM', image='').order_by('position')
        return Content.objects.filter(page=self).order_by('position')

    @property
    def get_all_questions(self):
        """ liste des questions de la page, triées selon leur position """
        return Question.objects.filter(page=self).order_by('position')

    @property
    def get_all_related_objects(self):
        """ liste de tous les objets qui ont une relation et que l'on souhaite dupliquer """
        return list(chain(
            Content.objects.filter(page=self),
            Question.objects.filter(page=self)
        ))

    def set_related_field(self, index):
        """ modifie la valeur de la clé étrangère (utile pour duplication)"""
        try:
            related_object = Tutorial.objects.get(id=index)
            self.tuto = related_object
            self.save()
        except Tutorial.DoesNotExist:
            self.delete()

    @property
    def get_questions_number(self):
        """ nombre de questions du quiz """
        return len(self.get_all_questions)

    def __str__(self):
        return self.page_title

class Content(models.Model):
    """ un contenu : sommaire, titre, sous-titre, paragraphe, image ...  """
    page = models.ForeignKey('Page', on_delete=models.CASCADE)
    contenttype = models.CharField(max_length=20, choices=CONTENTTYPE)
    texte = models.TextField(blank=True)
    image = models.ImageField(upload_to="tuto/images/", blank=True)
    video = models.FileField(upload_to="tuto/videos/", blank=True)
    percent_scale = models.IntegerField(default=100)
    position = models.IntegerField()

    class meta:
        verbose_name = "contenu"
    
    @property
    def get_all_related_objects(self):
        """ liste de tous les objets qui ont une relation et que l'on souhaite dupliquer """
        return list(chain(
            ListItem.objects.filter(content=self),
        ))
        
    @property    
    def get_all_listitems(self):
        """ liste des items, triés selon leur position """
        return ListItem.objects.filter(content=self).order_by('position')
    
    @property
    def readable_contenttype(self):
        return self.get_contenttype_display() 
    
    @property
    def short_text(self):
        if self.contenttype == 'LI':
            return "[{}]: - {}".format(self.get_contenttype_display(), self.get_all_listitems[0].texte)
        else:
            return "[{}]: {}".format(self.get_contenttype_display(), self.texte)
        
    def set_related_field(self, index):
        """ modifie la valeur de la clé étrangère (utile pour duplication)"""
        try:
            related_object = Page.objects.get(id=index)
            self.page = related_object
            self.save()
        except Page.DoesNotExist:
            self.delete()
    
    @property
    def ancre(self):
        """
        définition d'une ancre à inclure dans le fichier html
        pour un accès depuis le sommaire
        par exemple : <a href='{% url content.ancre %}'>Lien</a>
        """
        return '#'+str(self.id)

    def __str__(self):
        return self.page.tuto.title[:10]+ "_" + str(self.page) +  "_" + str(self.position) + "_" + self.texte[:10]

    def get_file(self):
        """ liste des fichiers media, pour gérer leur mise à jour et suppression """
        return [self.image, self.video]

class ListItem(models.Model):
    """items associés à un contenu de type list"""
    
    content = models.ForeignKey('Content', on_delete=models.CASCADE)   
    texte = models.TextField(blank=True)
    position = models.IntegerField()

    class Meta:
        verbose_name = "listitem"

    @property
    def get_all_related_objects(self):
        """ liste de tous les objets qui ont une relation et que l'on souhaite dupliquer """
        return []
    
    def set_related_field(self, index):
        """ modifie la valeur de la clé étrangère (utile pour duplication)"""
        try:
            related_object = Content.objects.get(id=index)
            self.content = related_object
            self.save()
        except Content.DoesNotExist:
            self.delete()

    def __str__(self):
        return "ListItem" + str(self.position)


class Category(models.Model):
    """ catégorie du tuto """
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, null=True, blank=True)
    position = models.IntegerField(default=0)

    class Meta:
        verbose_name = "categorie"

    def has_notuto(self):
        return not self.tutorial.all()
    
    @classmethod
    def max_position(cls):
        return max([0]+[cat.position for cat in cls.objects.all()])

    def __str__(self):
        return self.name

class Question(models.Model):
    """ Question d'un quiz """
    page = models.ForeignKey('Page', on_delete=models.CASCADE)
    question = models.TextField()
    # boolean = true si plusieurs réponses possibles
    multiresponse = models.BooleanField(default=False)
    # position du contenu dans la page :
    position = models.IntegerField()
    # explication affichée avec la correction :
    explication = models.TextField()

    class Meta:
        verbose_name = "question"

    @property
    def get_all_propositions(self):
        """ liste des propositions de la quetion, triées selon leur position """
        return Proposition.objects.filter(question=self).order_by('position')
    
    @property
    def get_all_related_objects(self):
        """ liste de tous les objets qui ont une relation et que l'on souhaite dupliquer """
        return Proposition.objects.filter(question=self)
    
    def set_related_field(self, index):
        """ modifie la valeur de la clé étrangère (utile pour duplication)"""
        try:
            related_object = Page.objects.get(id=index)
            self.page = related_object
            self.save()
        except Page.DoesNotExist:
            self.delete()

    def __str__(self):
        return self.question[0:30]

class Proposition(models.Model):
    """ Une proposition rattachée à une question """
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    position = models.IntegerField()
    proposition = models.TextField()
    good_answer = models.BooleanField(default=False)

    class Meta:
        verbose_name = "proposition"

    @property
    def get_all_related_objects(self):
        """ liste de tous les objets qui ont une relation et que l'on souhaite dupliquer """
        return []

    def set_related_field(self, index):
        """ modifie la valeur de la clé étrangère (utile pour duplication)"""
        try:
            related_object = Question.objects.get(id=index)
            self.question = related_object
            self.save()
        except Question.DoesNotExist:
            self.delete()

    def __str__(self):
        return "propostion"+ str(self.position)


# Suppression des fichiers MEDIAROOT inutiles lors de leur mise à jour ou suppression
@receiver(post_delete, sender=Tutorial)
@receiver(post_delete, sender=Content)
def auto_delete_images_on_delete(sender, instance, **kwargs):
    auto_delete_file_on_delete(sender, instance) 

@receiver(pre_save, sender=Tutorial)
@receiver(pre_save, sender=Content)
def auto_delete_image_on_change(sender, instance, **kwargs):
    auto_delete_file_on_change(sender, instance) 

# Suppression du Tutobase à la suppression du dernier tutoriel s'y référant :
@receiver(post_delete, sender=Tutorial)
def auto_delete_tutobase(sender, instance, **kwargs):
    tutobase = instance.tutobase
    if len(tutobase.get_all_tutos) == 0:
        tutobase.delete()

# variables globales :
modelClass = {
        'tutobase': TutoBase,
        'tutorial': Tutorial,
        'tuto': Tutorial,
        'category': Category,
        'page': Page,
        'content': Content, 
        'listitem': ListItem,
        'question': Question,
        'proposition': Proposition,
        }

def clone(instance):
    """ clone un objet tuto avec toute l'arborescente des related objects définie par la propriété get_all_related_objects et la méthode set_related_field + duplique les fichiers assciés des champs ImageField et FileField"""

    # enregistrement des instances en relation 
    related_objects = instance.get_all_related_objects
    # création nouvelle instance
    instance.id = None

    # enregistrement des images et fichiers de l'instance :
    filefield_buffer = { f.name:f.value_from_object(instance) for f in instance._meta.fields if f.__class__.__name__ in ("ImageField", "FileField") and f.value_from_object(instance) }
    
    # copie des fichiers dans la nouvelle instance (ce qui copie automatiquement les fichiers dans MEDIA)
    for field, file in filefield_buffer.items():
        path = Path(file.path)
        with path.open(mode="rb") as f:
            setattr(instance, field, File(f, name=path.name))
            instance.save()

    # sauvegarde de la nouvelle instance
    instance.save()

    # copie des instances en relation (processus récursif) :
    for inst in related_objects:
        inst = clone(inst)
        inst = inst.set_related_field(instance.id)

    return instance
