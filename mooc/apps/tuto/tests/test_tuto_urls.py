import pytest
from django.urls import reverse, resolve

from home.tests.context_tests import context_home
from tuto.tests.context_tests import context_tuto


@pytest.mark.django_db
class TestTutoUrls:

    def test_listing(self):
        path = reverse('tuto:listing')
        assert path == '/tutoriels/'
        assert resolve(path).view_name == 'tuto:listing'

    @pytest.mark.parametrize("i", range(4))
    def test_read_tuto(self,context_tuto, i):
        path = reverse(
                'tuto:read_tuto', 
                kwargs={
                    'tuto_slug': context_tuto['tutos'][i].slug, 
                    'page': '1',
                    })
        assert path == f"/tutoriels/{context_tuto['tutos'][i].slug}/1/"
        assert resolve(path).view_name == 'tuto:read_tuto'

    @pytest.mark.parametrize("i", range(2))
    def test_listing_cat(self,context_tuto, i):
        path = reverse(
                'tuto:listing_cat', 
                kwargs={'cat_slug': context_tuto['categories'][i].slug
                    })
        assert path == f"/tutoriels/category/{context_tuto['categories'][i].slug}/"
        assert resolve(path).view_name == 'tuto:listing_cat'

    def test_listing_search(self):
        path = reverse('tuto:listing_search')
        assert path == '/tutoriels/search/'
        assert resolve(path).view_name == 'tuto:listing_search'




