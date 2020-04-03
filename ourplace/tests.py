from django.test import TestCase, Client 
from django.urls import resolve, reverse
from ourplace.models import UserProfile,Canvas,CanvasAccess
from django.contrib.auth.models import User
import os
import re


class CanvasMethodTests(TestCase):
    def setUp(self):
        #do at start
        u=User.objects.create_user('test', 'test@test.com', 'test')
        Canvas.objects.create(title='test default', owner=u)
        Canvas.objects.create(title='test specified views', owner=u, views=20)
        u2=User.objects.create_user('test2', 'test2@test.com', 'test2')
        Canvas.objects.create(title='test access', owner=u2, visibility='C')

        #add a client
        self.client=Client()
    def tearDown(self):
        #do at end 
        if os.path.exists(str(Canvas.objects.get(title='test default').thumbnail.path)):
            os.remove(str(Canvas.objects.get(title='test default').thumbnail.path))
        if os.path.exists(str(Canvas.objects.get(title='test specified views').thumbnail.path)):
            os.remove(str(Canvas.objects.get(title='test specified views').thumbnail.path))
        if os.path.exists(str(Canvas.objects.get(title='test access').thumbnail.path)):
            os.remove(str(Canvas.objects.get(title='test access').thumbnail.path))


    def test_ensure_canvas_views(self):
        self.assertEqual((Canvas.objects.get(title='test default').views >= 0), True) # check default value is positive
        self.assertEqual((Canvas.objects.get(title='test specified views').views ==20), True) # checks a canvas' views were what was set previously (in this case 20)

    def test_ensure_owner_is_added_to_canvas_access(self):
        # check owner and canvas is added to the canvas access table when a new canvas is created
        u=User.objects.get(username='test')
        self.assertEqual(CanvasAccess.objects.filter(canvas=Canvas.objects.get(title='test default'), user=u).exists(), True)

    def test_ensure_canvas_creation_creates_thumbnail(self):
        # check that a thumbnail is created when a canvas is created
        self.assertEqual(os.path.isfile(str(Canvas.objects.get(title='test default').thumbnail.path)), True)

    def test_ensure_canvas_creation_creates_correct_slug(self):
        # check that the canvas slug is created when the canvas created and that it's the slugifed version of the title
        self.assertEqual(('test-default' == Canvas.objects.get(title='test default').slug), True)


    def test_correct_pages_viewable_while_not_logged_in(self):
        viewable_pages=['/', '/sitemap.xml', '/about/', '/faq/', '/search/', '/place/test-default/']
        for i in viewable_pages:
            # Get request 
            response = self.client.get(i)
            # check response is 200 ok
            self.assertEqual(response.status_code, 200)
    def test_correct_pages_not_viewable_while_not_logged_in(self):
        non_viewable_pages=['/account/', '/place/test-default/edit/', '/place/test-default/access/','/place/']
        for i in non_viewable_pages:
            # Get request 
            response = self.client.get(i)
            # check response is 302 for redirection
            self.assertEqual(response.status_code, 302)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('ourplace:account'))
        self.assertRedirects(response, '/accounts/login/?next=/account/')




# class IndexViewTests(TestCase):
#     def test_index_view_with_no_categories(self):
#         """
#         If no categories exist, the appropriate message should be displayed.
#         """
#         response = self.client.get(reverse('rango:index'))
        
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'There are no categories present.')
#         self.assertQuerysetEqual(response.context['categories'], [])

