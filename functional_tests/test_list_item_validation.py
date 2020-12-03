from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):
	
	def get_error_element(self):
		return self.browser.find_element_by_css_selector('.has-error')
	
	def test_cannot_add_empty_list_items(self):
		# Alice accidentaly tries to submit an empty list item, she
		# hits enter on an empty input box
		self.browser.get(self.live_server_url)
		self.get_item_input_box().send_keys(Keys.ENTER)			


		# The browser intercepts the request and does not load the list
		# page
		self.wait_for(lambda: self.browser.find_element_by_css_selector(
			'#id_text:invalid'
		))

		# She tries again with some text for the item, which now works
		self.get_item_input_box().send_keys('Buy milk')
		self.wait_for(lambda: self.browser.find_element_by_css_selector(
			'#id_text:valid'
		))
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')

		# Perversely, she tries to submit an empty item again
		self.get_item_input_box().send_keys(Keys.ENTER)

		# She recieves a similar error to before
		self.wait_for(lambda: self.browser.find_element_by_css_selector(
			'#id_text:invalid'
		))
		
		# And can correct it by filling in some text
		self.get_item_input_box().send_keys('Make tea')
		self.wait_for(lambda: self.browser.find_element_by_css_selector(
			'#id_text:valid'
		))
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')
		self.wait_for_row_in_list_table('2: Make tea')

	def test_cannot_add_duplicate_items(self):
		# Alice goes to the homepage and starts a new list
		self.browser.get(self.live_server_url)
		self.get_item_input_box().send_keys('Buy wellies')
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy wellies')

		# She accidentally tries to enter a suplicate item
		self.get_item_input_box().send_keys('Buy wellies')
		self.get_item_input_box().send_keys(Keys.ENTER)
	
		# She sees a helpful error message
		self.wait_for(lambda: self.assertEqual(
			self.get_error_element().text,
			'You\'ve already got this item in your list',
		))

	def test_error_messages_are_cleared_on_input(self):
		# Alice starts a list and causes a validation error
		self.browser.get(self.live_server_url)
		self.get_item_input_box().send_keys('Banter too thick')
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Banter too thick')
		self.get_item_input_box().send_keys('Banter too thick')
		self.get_item_input_box().send_keys(Keys.ENTER)
		
		self.wait_for(lambda: self.assertTrue(
			self.get_error_element().is_displayed()
		))

		# She starts typing in the input box to clear the error
		self.get_item_input_box().send_keys('a')

		# She is buzzing when the error disappears
		self.wait_for(lambda: self.assertFalse(
			self.get_error_element().is_displayed()
		))

	def test_error_messages_are_cleared_on_click(self):
		# Alice starts a list and causes a validation error
		self.browser.get(self.live_server_url)
		self.get_item_input_box().send_keys('Banter too thick')
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Banter too thick')
		self.get_item_input_box().send_keys('Banter too thick')
		self.get_item_input_box().send_keys(Keys.ENTER)
		
		self.wait_for(lambda: self.assertTrue(
			self.get_error_element().is_displayed()
		))

		# She clicks on the input box to clear the error
		self.get_item_input_box().click()

		# She is buzzing when the error disappears
		self.wait_for(lambda: self.assertFalse(
			self.get_error_element().is_displayed()
		))
