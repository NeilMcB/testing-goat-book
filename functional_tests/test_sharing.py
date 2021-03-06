from selenium import webdriver
from .base import FunctionalTest


def quit_if_possible(browser):
	try: browser.quit()
	except: pass


class SharingTest(FunctionalTest):

	def test_can_share_a_list_with_another_user(self):
		# Alice is a logged in user
		self.create_pre_authenticated_session('alice@example.com')
		alice_browser = self.browser
		self.addCleanup(lambda: quit_if_possible(alice_browser))

		# Bob is also hanging out on the site
		bob_browser = webdriver.Firefox()
		self.addCleanup(lambda: quit_if_possible(bob_browser))
		self.browser = bob_browser
		self.create_pre_authenticated_session('bob@example.com')

		# Alice goes to the homepage and starts a list
		self.browser = alice_browser
		self.browser.get(self.live_server_url)
		self.add_list_item('Get help')

		# She notices a "Share this list" option
		share_box = self.browser.find_element_by_css_selector(
			'input[name="share"]',
		)
		self.assertEqual(
			share_box.get_attribute('placeholder'),
			'your-friend@example.com',
		)

