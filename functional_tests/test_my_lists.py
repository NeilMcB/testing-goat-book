from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session
User = get_user_model()


class MyListTest(FunctionalTest):
	
	def create_pre_authenticated_session(self, email):
		if self.staging_server:
			session_key = create_session_on_server(self.staging_server, email)
		else:
			session_key = create_pre_authenticated_session(email)
		
		# We need to visit the site to get a cookie
		self.browser.get(f'{self.live_server_url}/404_made_up_url/')
		self.browser.add_cookie(dict(
			name=settings.SESSION_COOKIE_NAME,
			value=session_key,
			path='/',
		))
	
	def test_logged_in_users_are_saved_as_my_lists(self):
		# Alice is a logged-in user
		self.create_pre_authenticated_session('alice@example.com')

		# She goes to the homepage to start a list
		self.browser.get(self.live_server_url)
		self.add_list_item('Reticulate splines')
		self.add_list_item('Immanetize eschatron')
		first_list_url = self.browser.current_url

		# She notices a "My lists" link
		self.browser.find_element_by_link_text('My lists').click()

		# She sees that her first list is in there, named after its first item
		self.wait_for(
			lambda: self.browser.find_element_by_link_text('Reticulate splines')
		)
		self.browser.find_element_by_link_text('Reticulate splines').click()
		self.wait_for(
			lambda: self.assertEqual(self.browser.current_url, first_list_url)
		)

		# She decides to start another list just to check it's also added
		self.browser.get(self.live_server_url)
		self.add_list_item('Immunize cows')
		second_list_url = self.browser.current_url

		# She checks this also appears under her "My lists"
		self.browser.find_element_by_link_text('My lists').click()
		self.wait_for(
			lambda: self.browser.find_element_by_link_text('Immunize cows')
		)
		self.browser.find_element_by_link_text('Immunize cows').click()
		self.wait_for(
			lambda: self.assertEqual(self.browser.current_url, second_list_url)
		)
	
		# Then she logs out
		self.browser.find_element_by_link_text('Log out').click()
		self.wait_for(lambda: self.assertEqual(
			self.browser.find_elements_by_link_text('My lists'),
			[],		
		))	
