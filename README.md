# &#8205;&#127891; Projet de Mooc &#8205;&#127891; 

## &#128203; Généralités :
- python3.12 / django 5.2 
- base de donnée mysql ou postgresql
- auteur : Christophe Vellen

##  &#8205;&#127891; Démonstration : [ici](https://www.mooc.ecosketch.fr)

## &#129520; Fonctionnalités :
### Fonctionnalités accessibles à tous les utilisateurs :
- Présentation de la liste des tutoriels sous forme de liste :
    - sélection par catégorie
    - recherche de tutoriels contenant un mot ou une expression
- Lecture d'un tutoriel :
    - lecture par page du contenu
    - quiz : formulaires à compléter, affichage/masquage des bonnes réponses
    - passage à la page suivante si le quiz est terminé ou la page lue.
- Suivi de l'avancement des tutoriels sur son compte :
    - liste des tutoriels en cours ou terminés
    - % d'avancement
    - note obtenues aux quiz

### Fonctionnalités accessibles aux auteurs :
- Création et modification des tutoriels à travers l'interface spécifique :
    - insertion de contenus : 
        - titres, sous-titres, paragraphes, listes
        - image (taille ajustable), video
        - quiz : questions, propositions, correction
        - modification de l'ordre des contenus par glisser-déposer
    - visualisation du rendu en cours de rédaction
- Affectation du nouveau tutoriel :
        - par catégorie
        - par restriction d'utilisation pour les utilisateurs
- Modification du tutoriel avant validation pour publication
- Possibilité de créer une nouvelle version d'un tutoriel déjà publié.

### Fonctionnalités accessibles aux gestionnaires :
- Création et modification des catégories de tutoriels
- validation d'un tutoriel pour publication
- archivage d'un tutoriel
- dépublication d'un tutoriel
- suppression d'un tutoriel

### Fonctionnalités accessibles à travers l'administration :
- Pour les utilisateurs :
    - affectation par groupe (utilisateur, auteur, gestionnaire)
    - restriction d'accès pour un utilisateur


## &#129489;&#8205;&#127891; Les utilisateurs :

- #### cas 1 : user anonyme, non authentifié : 
    La session est temporaire. Le suivi de l'avancement est sauvegardé temporairement en session. Après une heure, ou à la déconnexion, la session expire et le suivi d'avancement est perdu.
   
- #### cas 2 : user authentifié :
    Le suivi de l'avancement est sauvegardé en base de données.
        
## &#129489;&#8205;&#129309;&#8205;&#129489;  Les groupes utilisateurs :

5 groupes :
- "guest" : user anonyme, droits de lecture des tutoriels, résultats quizz enregistrés temporairement en session (pas en bd)
- "utilisateur" : user authentifié, droits de lecture des tutoriels, résultats quizz enregistrés en session et en bd
- "auteur" : user "utilisateur" + droit de créer, modifier des tutoriels
- "gestionnaire": user "utilisateur" + droit de publier, archiver, supprimer des tutoriels
- "admin": user "utilisateur" + accès à l'administration du site (= peut affecter un user dans un groupe)

Group comprend "utilisateur", "auteur", gestionnaire", "admin".
"guest" est affecté par défaut aux users anonymes
"utilisateur" est affecté par défaut aux nouveaux users qui s'authentifient. 

## &#128736; Installation : 

- installer pyenv, poetry et python3 v3.12 :
```bash
    curl https://pyenv.run | bash
    curl -sSL https://install.python-poetry.org | python3
    pyenv local 3.12.10
```

- cloner le projet :
```bash
    git clone https://github.com/C-Vellen/Mooc.git
```
- créer une base de donnée Mysql ou Postgresql

- en développement, créer et paramétrer /mooc/mooc/settings/develop.py, ou bien définir des variables d'environnement :
    ```bash 
        SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxx'
        DEBUG = True
        ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
        CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:8000", "http://localhost:8000"]
        PROTOCOL = "http"
        SITE_ID = 1
        DATABASES = {
            'default':  {
                'ENGINE': 'django.db.backends.postgresql' ou 'django.db.backends.mysql,
                'NAME': 'xxxxxxxxxxxx',
                'USER': 'xxxxxxxxxxxx',
                'PASSWORD': 'xxxxxxxxxxxxx',
                'HOST': '127.0.0.1',
                'PORT': xxxx,
            }
        }
        
    ``` 
- en production, créer et paramétrer /mooc/mooc/settings/production.py ou bien définir des variables d'environnement,:
    ```bash 
        SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxx'
        DEBUG = False
        ALLOWED_HOSTS = ['www.xxxxx.xx', ... ]
        CSRF_TRUSTED_ORIGINS = ['https://www.xxxxx.xx', ... ]
        PROTOCOL = 'https'
        SITE_ID = 1
        DATABASES = {
            'default':  {
                'ENGINE': 'django.db.backends.postgresql' ou 'django.db.backends.mysql,
                'NAME': 'xxxxxxxxxxxx',
                'USER': 'xxxxxxxxxxxx',
                'PASSWORD': 'xxxxxxxxxxxxx',
                'HOST': '127.0.0.1',
                'PORT': xxxx,
            }
        }
        STATIC_ROOT = 'chemin vers fichiers statiques sur le serveur'
        MEDIA_ROOT =  'chemin vers fichiers media sur le serveur'
    ``` 

- installer les dépendances, définies dans le fichier **pyproject.toml** :
    ```bash
        poetry install
    ```

- activer l'environnement virtuel:
    sur console du serveur, à la racine du projet (dossier /Mooc/ ) :
    ```bash 
        source .venv/bin/activate
    ```
    - première migration de la base de donnée :
    ```bash
        ./mooc/manage.py migrate
    ```
    - création du superuser (administrateur):
    ```bash
        ./mooc/manage.py createsuperuser
    ```
    - création des groupes, catégories et pré-remplissage de la bd (valeurs par défaut):
    ```bash
        ./mooc/manage.py initgroups
    ```
    - initialisation tailwind :
    ```bash
        ./mooc/manage.py tailwind install
        ./mooc/manage.py tailwind build
    ```

    - collecte des fichiers statiques (en production) :
    ```bash
        ./mooc/manage.py collectstatic
    ```

    - lancer le serveur (voir ci-dessous), se connecter en tant qu'administrateur et aller sur l'administration django
        - modifier le user : entrer subId (random), nom, prénom, group (auteur, gestionnaire, admin)        
        - compléter les champs image et fichier des tables home/libelles et home/defaultcontent

## &#128640; Lancement du serveur de développement :
    ```bash
        ./mooc/manage.py runserver
        ./mooc/manage.py tailwind start
        npx mix watch
    ```


## &#8505;&#65039; Informations :

    dépendances : pyproject.toml
    models de la base de données : MOOC_models.drawio
    droits utilisateurs : MOOC_users.md
    remerciements : https://github.com/bevacqua/dragula


