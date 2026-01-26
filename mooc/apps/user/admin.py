from django.contrib import admin
from .models import User, Restriction


@admin.register(Restriction)
class RestrictionAdmin(admin.ModelAdmin):
    
    # ! N'APPARAIT DANS L'ADMIN QUE POUR LE STATUT SUPERUSER !
    # affichage des restrictions
    list_display = ['id', 'name', 'get_users', 'get_tutos']
    # list_display = ['id', 'name']
    ordering = ('id',)

    
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    
    # affichage des users
    list_display = ['id', 'username', 'get_groups', 'restrictions_list', 'email']
    ordering = ('id',)

    def restrictions_list(self, user):
        return ", ".join([r.name for r in user.get_restrictions])