import pytest
import os

from datetime import date
from django.core.files import File

from mooc.tests.temporary_media_files import create_file, delete_dir
from tuto.models import Category, Tutorial, Page, Content
from home.tests.context_tests import context_home
from tuto.tests.context_tests import context_tuto


@pytest.mark.django_db
class TestTutoModels:

    @pytest.mark.parametrize("i", range(2))
    def test_category_model(self, context_tuto, i):
        assert str(context_tuto['categories'][i]) == context_tuto['categories'][i].name

    @pytest.mark.parametrize("i", range(4))
    def test_tutorial_model(self, context_tuto, i):
        assert str(context_tuto['tutos'][i]) == context_tuto['tutos'][i].title

    @pytest.mark.parametrize("i", range(4))
    def test_page_model(self, context_tuto, i):
        assert str(context_tuto['pages'][i]) == context_tuto['pages'][i].page_title
        
    @pytest.mark.parametrize("i", range(4))
    def test_content_model(self, context_tuto, i):
        assert str(context_tuto['contents'][i]) == context_tuto['tutos'][i].title[:10] + "_" + context_tuto['pages'][i].page_title + "_" + str(context_tuto['contents'][i].position) + "_" + context_tuto['contents'][i].title

    @pytest.mark.parametrize("i", range(4))
    def test_content_has_ancre(self, context_tuto, i):
        assert context_tuto['contents'][i].ancre == f"#{context_tuto['contents'][i].id}"

    def test_auto_delete_file(self):
        """ test de la suppression des anciens fichiers MEDIA lors de la suppression ou mise à jour
        des articles et des contenus """
        
        # création répertoire temporaire et image de test
        img_name = 'img_test.jpg'
        img_content = ['RGB', (100, 100), 'rgb(255,100,30)']
        tmp_img = create_file("tuto", img_name, img_content)

        # création instances article et contenu
        cat = Category(name='cat')
        cat.save()
        with tmp_img.open(mode='rb') as f:
            tut = Tutorial(
                    category=cat, 
                    title='tutotest', 
                    created_at=date.today(),
                    miniature=File(f, name=img_name), 
                    resume="texte")
            tut.save() 
            pag = Page(
                    tuto=tut,
                    page_number=1,
                    page_title='pagetest',
                    description="texte")
            pag.save()
            cont = Content(
                    contenttype='PA',
                    page=pag,
                    position=1,
                    title='contenttest',
                    image=File(f, name=img_name)) 
            cont.save()

        # test instanciation modèles avec leurs images
        assert tut.miniature
        assert cont.image
        assert os.path.isfile(tut.miniature.path)
        assert os.path.isfile(cont.image.path)

        # test suppression ancienne image si mise à jour
        old_min_path = tut.miniature.path
        old_img_path = cont.image.path
        with tmp_img.open(mode='rb') as f:
            tut.miniature = File(f, name='new'+img_name)
            tut.save()
            cont.image = File(f, name='new'+img_name) 
            cont.save()
        assert os.path.isfile(tut.miniature.path)
        assert os.path.isfile(cont.image.path)
        assert not os.path.isfile(old_min_path)
        assert not os.path.isfile(old_img_path)

        # test suppression des images à la suppression des instances
        tut.delete()
        cont.delete()
        assert not os.path.isfile(tut.miniature.path)
        assert not os.path.isfile(cont.image.path)
        
        # nettoyage répertoire temporaire
        delete_dir("tuto")



