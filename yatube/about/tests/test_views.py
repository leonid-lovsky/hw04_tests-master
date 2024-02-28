from django.test import TestCase, Client
from django.urls import reverse


class AboutViewsTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_author_page(self):
        response = self.guest_client.get(reverse('about:author'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about/author.html')

    def test_about_tech_page(self):
        response = self.guest_client.get(reverse('about:tech'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about/tech.html')
