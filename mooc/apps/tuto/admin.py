from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType

from .models import Category, TutoBase, Tutorial, Page, Content, ListItem, Question, Proposition

# _______________________________________________________________
# classe mixin pour récupérer facilement les adresse url des instances
# et pour les afficher dans l'interface d'administration

class AdminURLMixin(object):
    def get_admin_url(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__)
        return reverse("admin:tuto_%s_change" % (
            content_type.model),
            args=(obj.id,))



# _______________________________________________________________
# classes des modèles à afficher en table dans les classes liées:
# Tutorial dans Category,...


class TutorialInline(admin.TabularInline, AdminURLMixin):
    # affiche sous une catégorie ou une TutoBase les tutos qui lui sont liés
    model = Tutorial
    # champs éditables à afficher
    
    fieldsets = [
            (None, {'fields': ['id', 'title', 'slug', 'author', 'version', 'updated_at', 'tutorial_link']})
            ]
    # champs non modifiables à afficher
    readonly_fields = ['id', 'version', 'created_at', 'tutorial_link']
    ordering = ('-created_at',)
    extra = 0
    
    # méthode pour pouvoir afficher le lien html des tutorials :
    def tutorial_link(self, tutorial):
        url = self.get_admin_url(tutorial)
        return mark_safe("<a href='{}'>{}</a>".format(url, tutorial.id))

    tutorial_link.short_description = "lien"

class PageInline(admin.TabularInline, AdminURLMixin):
    # affiche sous un tuto les contenus qui lui sont liés
    model = Page
    # champs éditables à afficher
    fieldsets = [
            (None, {'fields': ['tuto', ('id', 'page_number', 'page_title', 'page_link'),]})
            ]
    # champs non modifiables à afficher
    readonly_fields = ['id', 'page_link']
    ordering = ('page_number',)
    extra = 1
    
    # méthode pour pouvoir afficher le lien html des paragraphes :
    def page_link(self, page):
        url = self.get_admin_url(page)
        return mark_safe("<a href='{}'>{}</a>".format(url, page.id))

    page_link.short_description = "lien"



class ContentInline(admin.TabularInline, AdminURLMixin):
    # affiche sous un tuto les contenus qui lui sont liés
    model = Content
    # champs éditables à afficher
    fieldsets = [
            (None, {'fields': ['page', ('id', 'position', 'contenttype',), 'texte', 'image', 'video', 'percent_scale', 'content_link']})
            ]
    # champs non modifiables à afficher
    readonly_fields = ['id', 'content_link']
    ordering = ('position',)
    extra = 1
    
    # méthode pour pouvoir afficher le lien html des paragraphes :
    def content_link(self, content):
        url = self.get_admin_url(content)
        return mark_safe("<a href='{}'>{}</a>".format(url, content.id))

    content_link.short_description = "lien"

class ListItemInline(admin.TabularInline, AdminURLMixin):
    model = ListItem
    # champs éditables à afficher
    fieldsets = [
            (None, {'fields': ['content', ('id', 'position', 'texte', 'listitem_link'),]})
            ]
    # champs non modifiables à afficher
    readonly_fields = ['id', 'listitem_link']

    ordering = ("position", )

    def listitem_link(self, listitem):
        url = self.get_admin_url(listitem)
        return mark_safe("<a href='{}'>{}</a>".format(url, listitem.id))

    listitem_link.short_description = "lien"

class QuestionInline(admin.TabularInline, AdminURLMixin):
    model = Question
    # champs éditables à afficher
    fieldsets = [
            (None, {'fields': ['page', ('id', 'position', 'question', 'multiresponse', 'explication','question_link'),]})
            ]
    
    # champs non modifiables à afficher
    readonly_fields = ['id', 'question_link']
    # méthode pour pouvoir afficher le lien html des paragraphes :
    def question_link(self, question):
        url = self.get_admin_url(question)
        return mark_safe("<a href='{}'>{}</a>".format(url, question.id))

    question_link.short_description = "lien"


class PropositionInline(admin.TabularInline, AdminURLMixin):
    model = Proposition
    # champs éditables à afficher
    fieldsets = [
            (None, {'fields': ['question', ('id', 'position', 'proposition', 'good_answer','proposition_link'),]})
            ]
    # champs non modifiables à afficher
    readonly_fields = ['id', 'proposition_link']

    ordering = ("position", )

    def proposition_link(self, proposition):
        url = self.get_admin_url(proposition)
        return mark_safe("<a href='{}'>{}</a>".format(url, proposition.id))

    proposition_link.short_description = "lien"
    
# _______________________________________________________________
# classes pour afficher chaque modèle dans l'interface d'administration

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    
    # affichage des catégories
    list_display = ['name', 'slug', 'position']
    ordering = ('position',)
    
    # champs pré-remplis :
    prepopulated_fields = {'slug': ('name',),}
 
    # affichage de la table des tutos de la catégorie
    inlines = [TutorialInline,]

@admin.register(TutoBase)
class TutoBaseAdmin(admin.ModelAdmin):
    
    # affichage des catégories
    list_display = ['id', 'name', 'updated_at', 'get_last_version', 'get_last_published_or_archived_version']
    
    # champs pré-remplis :
    # champs à afficher
    fieldsets = [
            (None, {'fields': [
                ('name', 'updated_at', 'get_last_version', 'get_last_published_or_archived_version'),  
            ]})]
    readonly_fields = ['get_last_version', 'get_last_published_or_archived_version']
    # affichage de la table des tutos de la catégorie
    inlines = [TutorialInline,]


@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    
    # affichage de la liste des tutos
    list_display = ['id', 'title', 'category', 'updated_at', 'slug', 'tutobase', 'version', 'in_progress', 'submitted', 'rejected', 'published', 'archived', ] 
    ordering = ('-updated_at',)
    
    # champs pré-remplis :
    prepopulated_fields = {'slug': ('title',),}
 
    # affichage des tutos

    # définition d'une barre de recherche et de filtre sur les champs
    search_fields = ['title', 'resume']
    list_filter = ['category', 'created_at', 'published']

    # champs à afficher
    fieldsets = [
            (None, {'fields': [
                ('id', 'title', 'author',),
                 ('category', 'restriction', 'tutobase', 'version'), 
                ('thumbnail', 'slug',),
                ('in_progress', 'submitted', 'rejected', 'published', 'archived', ),
                ('created_at', 'updated_at'), 
                'image', 
                'resume', 
                ]})
            ]
    
    # déclarer les champs non modifiables pour pouvoir les afficher:
    readonly_fields = ['id', 'created_at']
    
    # affichage de la  table des pages des tutos:
    inlines = [PageInline,]


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    
    # affichage de la liste des pages
    list_display = ['id', 'tuto', 'page_title', 'page_number'] 
    ordering = ('page_number',)
    
    # champs à afficher
    fieldsets = [
            (None, {'fields': [('id', 'tuto', 'page_title', 'page_number'), ]})
            ]
    # déclarer les champs non modifiables pour pouvoir les afficher:
    readonly_fields = ['id']
    
     # affichage de la  table des pages des contenus:
    inlines = [ContentInline, QuestionInline]
 


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    
    # affichage de la liste des contenus
    list_display = ['id', 'contenttype', 'page', 'position'] 
    ordering = ('position',)
    
    # définition d'une barre de recherche et de filtre sur les champs
    search_fields = ['texte']
    list_filter = ['contenttype', 'page', 'position']

    # champs à afficher
    fieldsets = [
            (None, {'fields': [('id', 'contenttype', 'page', 'position'), 'texte', 'image', 'video', 'percent_scale']})
            ]
    # déclarer les champs non modifiables pour pouvoir les afficher:
    readonly_fields = ['id']
    
    # affichage de la  table des listitems :
    inlines = [ListItemInline,]
  
@admin.register(ListItem)
class ListItemAdmin(admin.ModelAdmin):
    
    # affichage de la liste des propositions
    list_display = ['id', 'content', 'position', 'texte',]
    
    # champs à afficher
    fieldsets = [
            (None, {'fields': [('id', 'content', 'position', 'texte',), ]})
            ]
    # déclarer les champs non modifiables pour pouvoir les afficher:
    readonly_fields = ['id']
    

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    
    # affichage de la liste des questions
    list_display = ['id', 'page', 'question', 'multiresponse', 'position', 'explication']
    
    # champs à afficher
    fieldsets = [
            (None, {'fields': [('id', 'page', 'question', 'multiresponse',), ('position', 'explication'), ]})
            ]
    
    # déclarer les champs non modifiables pour pouvoir les afficher:
    readonly_fields = ['id']
    
     # affichage de la  table des pages des propositions :
    inlines = [PropositionInline,]
  


@admin.register(Proposition)
class PropositionAdmin(admin.ModelAdmin):
    
    # affichage de la liste des propositions
    list_display = ['id', 'question', 'position', 'proposition', 'good_answer',]
    
    # champs à afficher
    fieldsets = [
            (None, {'fields': [('id', 'question', 'position', 'proposition', 'good_answer',), ]})
            ]
    # déclarer les champs non modifiables pour pouvoir les afficher:
    readonly_fields = ['id']
    
