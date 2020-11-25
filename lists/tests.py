from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve

from .views import homepage
from .models import Item

class HomepageTest(TestCase):

	def test_homepage_returns_correct_html(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'homepage.html')

	def test_can_save_a_POST_request(self):
		response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

	def test_redirects_after_POST_request(self):
		response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
		self.assertRedirects(response, '/lists/the-only-list-in-the-world/')

	def test_only_saves_items_when_necessary(self):
		response = self.client.get('/')
		self.assertEqual(Item.objects.count(), 0)


class ListViewTest(TestCase):
	
	def test_uses_list_template(self):
		response = self.client.get('/lists/the-only-list-in-the-world/')
		self.assertTemplateUsed(response, 'list.html')

	def test_displays_all_created_items(self):
		first_item_text = 'hello from 1'
		second_item_text = 'world from 2'

		Item.objects.create(text=first_item_text)
		Item.objects.create(text=second_item_text)

		response = self.client.get('/lists/the-only-list-in-the-world/')

		self.assertContains(response, first_item_text)
		self.assertContains(response, second_item_text)


class ItemModelTest(TestCase):
	
	def test_saving_and_retrieving_items(self):
		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.save()

		second_item = Item()
		second_item.text = 'Item the second'
		second_item.save()

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		self.assertEqual(first_saved_item.text, 'The first (ever) list item')
		second_saved_item = saved_items[1]
		self.assertEqual(second_saved_item.text, 'Item the second')
		
