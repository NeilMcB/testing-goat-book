from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

	def test_can_start_a_list_for_one_user(self):
		# Gussie has heard about a cool new app, she goes to look at the homepage.
		self.browser.get(self.live_server_url)

		# She notices the page title and header mention to-do lists.
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		# She is invited to enter a to-do item straight away.
		inputbox = self.get_item_input_box()
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item',
		)		

		# She types "Buy peacock feathers" into a text box.
		inputbox.send_keys('Buy peacock feathers')

		# When she hits enter, the page updates and now the lists "1: Buy peacock featuers"
		# as an item in a to-do list.
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')

		# There is still a text box inviting her to add another item, she enters "Use
		# peacock feathers to make a fly".
		inputbox = self.get_item_input_box()
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item',
		)		
		
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)

		# The page updates again and now shows both items on her list.
		self.wait_for_row_in_list_table('1: Buy peacock feathers')
		self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

	
	def test_multiple_users_can_start_litsts_at_different_urls(self):
		# Alice starts a new to-do list
		self.browser.get(self.live_server_url)
		inputbox = self.get_item_input_box()
		inputbox.send_keys('Buy peacock feathers')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')

		# She notices her list has a unique URL
		alice_list_url = self.browser.current_url
		self.assertRegex(alice_list_url, '/lists/.+')


		# Now a new user, Bob, accesses the site in a different session
		self.browser.quit()
		self.browser = webdriver.Firefox()
		self.browser.get(self.live_server_url)

		# Bob should see no sign of Edith's list
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text)

		# Bob starts a new list by entering an item
		inputbox = self.get_item_input_box()
		inputbox.send_keys('Smoke some weed bro')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Smoke some weed bro')

		# Bob gets his own unique url
		bob_list_url = self.browser.current_url
		self.assertRegex(bob_list_url, '/lists/.+')
		self.assertNotEqual(bob_list_url, alice_list_url)

		# There is still not trace of Alice's list
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('make a fly', page_text)
		self.assertIn('weed bro', page_text)

