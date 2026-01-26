from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    subId = models.CharField(max_length=8)
    restriction = models.ManyToManyField('Restriction', related_name="user", blank=True)
    
    @property
    def is_author(self):
        return self.groups.filter(name="auteur").exists()

    @property
    def is_gestionnaire(self):
        return self.groups.filter(name="gestionnaire").exists()

    def __str__(self):
        return "{} {} [{}]".format(self.last_name, self.first_name, self.username)
    
    @property
    def get_restrictions(self):
        return self.restriction.all()

    def get_groups(self):
        return " , ".join(g.name for g in self.groups.all())

class Restriction(models.Model):
    """ classe qui permet de définir des groupes de User et des groupes de tutoriels dont la lecture est retreinte à ces User """
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Restriction d'accè"

    def __str__(self):
        return self.name
    
    def get_users(self):
        return ", ".join(u.username for u in self.user.all())
    
    def get_tutos(self):
        return ", ".join(t.title for t in self.tutorial.all())
