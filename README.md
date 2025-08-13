# &#8205;&#127891; Projet de Mooc &#8205;&#127891; 

## &#128203; Généralités :
- python3.12 / django 5.2 
- pour base de donnée postgresql v17.2
- auteur : Christophe Vellen
  

## &#128273; Codes pour la version locale développement :
- login de l'administrateur :
```bash
    {username: moocadmin, password:0000}
```
- BD postgres v17.2:
```bash
    {
        owner : moocadmin,
        password :    0000,
        database : moocdb,
        port: 5434,
    }
```


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

- installer les dépendances, définies dans le fichier **pyproject.toml** :
```bash
    git clone https://github.com/C-Vellen/Mooc.git
```

- en production, créer et paramétrer /mooc/mooc/settings/production.py :
    ```bash 
        SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxx'
        DEBUG = False
        ALLOWED_HOSTS = ['www.xxxxx.xx', ... ]
        SITE_ID = 1
        DATABASES = {
            'default':  {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'xxxxxxxxxxxx',
                'USER': 'xxxxxxxxxxxx',
                'PASSWORD': 'xxxxxxxxxxxxx',
                'HOST': '127.0.0.1',
                'PORT': xxxx,
            }
        }
        STATIC_ROOT = 'chemin vers fichiers statiques sur le serveur'
        MEDIA_ROOT =  'chemin vers fichiers media sur le serveur'
        PROTOCOL = 'https'
    ``` 

- activer l'environnement virtuel:
    sur console du serveur, à la racine du projet (dossier /Mooc/ ) :
    ```bash 
        source .venv/bin/activate
    ```
    - migrations :
    ```bash
        ./mooc/manage.py migrate
    ```
    - adressage des fichiers statiques (en production) :
    ```bash
        ./mooc/manage.py collectstatic
    ```

    - création des groupes et pré-remplissage de la bd (valeurs par défaut):
    ```bash
        ./mooc/manage.py initgroups
    ```
     - création du superuser (administrateur):
    ```bash
        ./mooc/manage.py createsuperuser
    ```

## &#128640; Lancement du serveur de développement :
- option 1 : en ligne de commande
    ```bash
        ./mooc/manage.py runserver
        ./mooc/manage.py tailwind start
        npx mix watch
    ```
- option 2 : utiliser le raccourci défini dans .bashrc_Mooc
    ```bash
        startmooc
    ```


## &#8505;&#65039; Informations :

    dépendances : pyproject.toml
    models de la base de données : MOOC_models.drawio
    droits utilisateurs : MOOC_users.md
    remerciements : https://github.com/bevacqua/dragula


## &#129489;&#8205;&#127891; Les utilisateurs :

- #### user anonyme, non authentifié : 
    pas de user, session temporaire expire après 1 heure. 
    - objet user : aucun user enregistré
    - objet request (enregistré par le browser):
    ```bash 
        request.user = AnonymousUser
        request.session = {
            "user": {
                "subid": None,
                "username": None,
                "first_name": None,
                "last_name": None,
                "status": ["guest"],
                "restriction": None,
            },
            "session_key": session.session_key,
            "_session_expiry":3600,
        }
    ```

    - objet session : enregistrée en bd, supprimée :
        - si logout ou 
        - si expirée dès qu'on appelle la vue user:connexion (clearsession)
    ```bash
        session -> session_key, data_key, expire_date
    ```
- #### user authentifié :
    a rempli le formulaire de la vue de user:connexion, session temporaire de 1 jour.
    - objet user : objet user créé ou récupéré dans la bd
        
    - objet request (enregistré par le browser):
    ```bash 
        request.user = user
        request.session = {
            "user": {
                "subid": user.subId,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "status": ["utilisateur"],
                "restriction": None,
            },
            "session_key": session.session_key,
            "_session_expiry":86400,
        }
    ```

    - objet session : enregistrée en bd, supprimée :
        - si logout ou 
        - si expirée dès qu'on appelle la vue user:connexion (clearsession)
    ```bash
        session -> session_key, data_key, expire_date
    ```

## &#129489;&#8205;&#129309;&#8205;&#129489;  Les groupes utilisateurs :
5 groupes :
- "guest" : user anonyme, droits de lecture des tutos, résultats quizz enregistrés en session (pas en bd)
- "utilisateur" : user authentifié, droits de lecture des tutos, résultats quizz enregistrés en session et en bd
- "auteur" : user "utilisateur" + droit d'écrire des tutos
- "gestionnaire": user "utilisateur" + droit de publier, archiver, supprimer des tutos
- "admin": user "utilisateur" + accès à l'administration du site (= peut affecter un user dans un groupe)

En bd : Group comprend "utilisateur", "auteur", gestionnaire", "admin".
"guest" est affecté par défaut aux users anonymes
"utilisateur" est affecté par défaut aux nouveaux users qui s'authentifient.