import pytest
import os
from datetime import date
from mixer.backend.django import mixer


# Textes pour remplir les instances de test tuto page et contenu :
lorem_short = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do \
        eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad \
        minim veniam, quis nostrud exercitation laboris ullamco laboris nisi ut aliquip \
        ex ea commodo consequat."
lorem_long = "Sed ut perspiciatis unde omnis iste natus error sit voluptatem \
        accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae \
        ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt \
        explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut \
        odit aut fugit, sed quia consequuntur magni dolores eos qui ratione \
        voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum \
        quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam \
        eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat \
        voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam \
        corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? \
        Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse \
        quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo \
        voluptas nulla pariatur?"


@pytest.fixture
def context_tuto(context_home):
#def context_tuto():

    categories = mixer.cycle(2).blend(
            'tuto.Category', 
            name=(f'category_{i}' for i in range(2)), 
            slug=(f'category-{i}' for i in range(2)), 
            )
    tutos = mixer.cycle(4).blend(
            'tuto.Tutorial', 
            category=(categories[i] for i in (0,0,1,0)), 
            title=mixer.sequence("Titre {0}"), 
            date_public=date.today(),
            publie=(b for b in (True, True, True, False)),
            slug= mixer.sequence("tuto-{0}"),
            resume=(resume for resume in (
                "pas la peine de chercher ici !",
                lorem_short,
                " ".join(reversed(lorem_short.split(" "))),
                "".join(reversed(lorem_short))
                ))
            )
    pages = mixer.cycle(4).blend(
            'tuto.Page',
            id=(i for i in range(996,1000)),
            tuto=(tutos[i] for i in range(4)),
            page_number=(i for i in range(4)),
            page_title="titre de la page",
            description=(texte for texte in (
                lorem_long,
                "texte",
                "texte",
                lorem_short)),
            )

    contents = mixer.cycle(4).blend(
            'tuto.Content',
            id=(i for i in range(996,1000)),
            page=(pages[i] for i in range(4)),
            contenttype='PA',
            title="titre",
            texte=(texte for texte in (
                lorem_long,
                "texte",
                "texte",
                lorem_short)),
            position=1,
            )

    context_home.update({
    #context_tuto = {
            'categories':categories,
            'tutos':tutos,
            'pages':pages,
            'contents':contents,
            })
            #}
    
    yield context_home
    #yield context_tuto

    # suppression des fichiers de tests de MEDIAROOT :
    for tuto in tutos:
        if tuto.miniature:
            os.remove(tuto.miniature.path)
    for content in contents:
        if content.image:
            os.remove(content.image.path)


