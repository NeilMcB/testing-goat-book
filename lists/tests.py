from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve

from .views import homepage


class HomepageTest(TestCase):

	def test_root_url_resolves_to_homepage_view(self):
		found = resolve('/')
		self.assertEqual(found.func, homepage)


	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = homepage(request)
		html = response.content.decode('utf8')

		self.assertTrue(html.startswith('<html>'))
		self.assertIn('<title>To-Do lists</title>', html)
		self.assertTrue(html.endswith('</html>'))

