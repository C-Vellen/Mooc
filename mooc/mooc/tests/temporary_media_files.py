# Fonctions permettant de créer un dossier temporaire (create_dir) au niveau de chaque appli, et d'y
# enregistrer un fichier temporaire (create_file) de type image ou texte, de façon à documenter 
# les champs ImageField et FileField des modèles en cours de test.
# Fonction de suppression du dossier temporaire et de son contenu (delete_dir)


import shutil
from PIL import Image
from pathlib import Path
from django.conf import settings

def create_file(app_name, file_name, args):
    """
    créé un fichier sur dossier temporaire app_name/tmp/
    entrée : nom du fichier (str), contenu (str)
    sortie : chemin PosixPath du fichier
    """
    tmp_file = create_dir(app_name) / file_name
    ext = file_name.split(".")[-1]
    if ext in ['jpg', 'jpeg', 'png', 'bitmap']:
        img = Image.new(*args)
        img.save(tmp_file)
    else:
        tmp_file.write_text(args)
    return tmp_file

def create_dir(app_name):
    """ définit un dossier temporaire tmp (le créé s'il n'existe pas)"""
    path = Path("/".join([settings.APPS_DIR, app_name, "tests"]))
    tmp_dir = path / "tmp"
    try:
        tmp_dir.mkdir()
    except FileExistsError:
        pass
    return tmp_dir

def delete_dir(app_name):
    """supprime le dossier temporaire tmp"""
    tmp_dir = create_dir(app_name)
    try:
        shutil.rmtree(tmp_dir)
    except FileNotFoundError:
        pass

