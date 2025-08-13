from .models import DefaultContent, Libelles

INIT_INSTANCES = {
    "DefaultContent": [
        {
            "description": "default_image",
            "explication": "charger dans le champ 'Image' une image par défaut qui sera affichée",
        },
        {
            "description": "default_video",
            "explication": "charger dans le champ 'Fichier' une video par défaut qui sera affichée",
        },
    ],
    "Libelles": [
        {
            "description":  "Favicon",
            "explication":  "charger dans le champ 'image' le favicon qui sera affiché dans l'onglet du navigateur",
        },
        {
            "description":  "Bandeau_logo",
            "explication":  "charger dans le champ 'image' le logo qui sera affiché en haut à gauche du bandeau",
            "contenu":      "Logo",
        },
        {
            "description":  "Accueil_titre",
            "explication":  "écrire dans le champ 'contenu' le texte de présentation de la page d'accueil",
            "contenu":      "Titre de la page d'accueil",
        },
        {
            "description":  "Accueil_description",
            "explication":  "écrire dans le champ 'contenu' le texte de présentation de la page d'accueil",
            "contenu":      "Texte de description de la page d'accueil",
        },
        {
            "description":  "Footer_description",
            "explication":  "écrire dans le champ 'contenu' le texte du footer",
            "contenu":      "Texte de description du footer",
        },
        {
            "description":  "Lien_yt",
            "explication":  "charger le logo YT dans le champ image (jpg, png) ou dans le champ fichier (svg) et le lien dans le champ lien",
            "contenu":      "Lien Youtube",
        },
        {
            "description":  "Lien_X",
            "explication":  "charger le logo X dans le champ image (jpg, png) ou dans le champ fichier (svg) et le lien dans le champ lien",
            "contenu":      "Lien X",
        },
    ]
}

def init_instances(command):
    command.stdout.write(
        command.style.SUCCESS("Initialisation image par défaut et libellé de la page d'accueil")
    )

    for fields in INIT_INSTANCES["DefaultContent"]:
        instance = DefaultContent.create(**fields)
    for fields in INIT_INSTANCES["Libelles"]:
        instance = Libelles.create(**fields)
    
