from django.http import HttpRequest
from django.test import TestCase
from django.utils.html import escape
from django.urls import resolve

from lists.views import homepage
from lists.models import Item, List

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
		new_list = List.objects.first()
		self.assertRedirects(response, f'/lists/{new_list.id}/')

	def test_only_saves_items_when_necessary(self):
		response = self.client.get('/')
		self.assertEqual(Item.objects.count(), 0)


class ListViewTest(TestCase):
	
	def test_uses_list_template(self):
		list_ = List.objects.create()
		response = self.client.get(f'/lists/{list_.id}/')
		self.assertTemplateUsed(response, 'list.html')

	def test_displays_only_items_for_that_list(self):
		correct_list = List.objects.create()
		other_list = List.objects.create()

		correct_list_first_item_text = 'hello from 1'
		correct_list_second_item_text = 'world from 2'
		Item.objects.create(text=correct_list_first_item_text, list=correct_list)
		Item.objects.create(text=correct_list_second_item_text, list=correct_list)
		
		other_list_first_item_text = 'blello from 1'
		other_list_second_item_text = 'blorld from 2'
		Item.objects.create(text=other_list_first_item_text, list=other_list)
		Item.objects.create(text=other_list_second_item_text, list=other_list)

		response = self.client.get(f'/lists/{correct_list.id}/')
		self.assertContains(response, correct_list_first_item_text)
		self.assertContains(response, correct_list_second_item_text)

	def test_passes_correct_list_to_template(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		response = self.client.get(f'/lists/{correct_list.id}/')
		self.assertEqual(response.context['list'], correct_list)

	def test_can_save_a_POST_request_to_an_existing_list(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		self.client.post(
			f'/lists/{correct_list.id}/',
			data={'item_text': 'A new item for an existing list'},
		)

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item for an existing list')
		self.assertEqual(new_item.list, correct_list)


	def test_POST_redirects_to_list_view(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		response = self.client.post(
			f'/lists/{correct_list.id}/',
			data={'item_text': 'A new item for an existing list'},
		)

		self.assertRedirects(response, f'/lists/{correct_list.id}/')

	def test_validation_errors_are_sent_back_to_homepage_template(self):
		response = self.client.post('/lists/new', data={'item_text': ''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'homepage.html')
		expected_error = escape('You can\'t have an empty list item')
		self.assertContains(response, expected_error)

	def test_invalid_list_items_arent_saved(self):
		self.client.post('/lists/new', data={'item_text': ''})
		self.assertEqual(List.objects.count(), 0)
		self.assertEqual(Item.objects.count(), 0)
	
	def test_validation_errors_end_up_on_lists_page(self):
		list_ = List.objects.create()
		response = self.client.post(f'/lists/{list_.id}/', data={'item_text': ''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'list.html')
		expected_error = escape('You can\'t have an empty list item')
		self.assertContains(response, expected_error)
