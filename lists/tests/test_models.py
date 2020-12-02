from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve

from lists.views import homepage
from lists.models import Item, List

class ItemModelTest(TestCase):

	def test_default_text(self):
		item = Item()
		self.assertEqual(item.text, '')

	def test_item_is_related_to_list(self):
		list_ = List.objects.create()
		item = Item(list=list_)
		item.save()
		self.assertIn(item, list_.item_set.all())	

	def test_cannot_save_empty_list_items(self):
		list_ = List.objects.create()
		item = Item(list=list_, text='')
		with self.assertRaises(ValidationError):
			item.save()
			# Force database to perform validation
			item.full_clean()

	def test_duplicate_items_in_same_list_are_invalid(self):
		list_ = List.objects.create()
		Item.objects.create(text='foo', list=list_)
		with self.assertRaises(ValidationError):
			item = Item(text='foo', list=list_)
			item.full_clean()

	def test_duplicate_items_in_different_lists_are_valid(self):
		list1 = List.objects.create()
		list2 = List.objects.create()
		
		Item.objects.create(text='foo', list=list1)
		item = Item(text='foo', list=list2)
		item.full_clean()  # Shouldn't raise an error

	def test_list_ordering(self):
		# Uniqueness constraint in Item can cause issues with query ordering
		list_ = List.objects.create()
		item1 = Item.objects.create(text='1', list=list_)
		item2 = Item.objects.create(text='2', list=list_)
		item3 = Item.objects.create(text='3', list=list_)
		self.assertEqual(
			list(Item.objects.all()),
			[item1, item2, item3],
		)
	
	def test_string_representation(self):
		item = Item(text='some text')
		self.assertEqual(str(item), 'some text')


class ListModelTestCase(TestCase):
	
	def test_get_absolute_url(self):
		list_ = List.objects.create()
		self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')
