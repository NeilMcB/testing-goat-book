from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve

from .views import homepage


class HomepageTest(TestCase):

	def test_home_page_returns_correct_html(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'homepage.html')
