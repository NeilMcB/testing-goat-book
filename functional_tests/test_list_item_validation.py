from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

	def test_cannot_add_empty_list_items(self):
		# Alice accidentaly tries to submit an empty list item, she
		# hits enter on an empty input box

		# The homepage refreshes and there is an error message saying
		# that list items cannot be blank

		# She tries again with some text for the item, which now works

		# Perversely, she tries to submit an empty item again

		# She recieves a similar error to before

		# And can correct it by filling in some text
		self.fail('Write me!')

