from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrive_it_later(self):
		# Gussie has heard about a cool new app, she goes to look at the homepage.
		browser.get('http://localhost:8000')

		# She notices the page title and header mention to-do lists.
		self.assertIn('To-Do', browser.title)
		self.fail('Finish the test!')

		# She is invited to enter a to-do item straight away.

		# She types "Buy peacock featuers" into a text box.

		# When she hits enter, the page updates and now the lists "1: Buy peacock featuers"
		# as an item in a to-do list.

		# There is still a text box inviting her to add another item, she enters "Use
		# peacock feathers to make a fly".

		# The page updates again and now shows both items on her list.

		# Edith wonders if the site will remember her list, then she sees the site has
		# generated a unique URL for her - there is some explanatory text to that effect.

		# She visits that URL - her to-do list is still there.


if __name__ == '__main__':
	unittest.main()

