from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from mooc.settings import GROUPNAMES
from home.init_instances import init_instances
from tuto.models import Category


class Command(BaseCommand):
    help = "Création des groupes de bases"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Initialisation des groupes :"))

        for g in GROUPNAMES:
            group, created = Group.objects.get_or_create(name=g)
            if created:
                groupstatus = "groupe vient d'être créé"
            else:
                groupstatus = "groupe déjà existant"

            self.stdout.write("   Group {} : ok - {}".format(g, groupstatus))

            if g == "admin":
                group.permissions.set(Permission.objects.all())

        self.stdout.write(self.style.SUCCESS("Initialisation des catégories :"))

        if Category.objects.all().exists():
            self.stdout.write("   Catégories existantes")
        else:
            category, created = Category.objects.get_or_create(name="Categorie_1")
            category.slug = "categorie_1"
            category.save()
            self.stdout.write("   Catégorie_1 : créée")

        init_instances(self)
