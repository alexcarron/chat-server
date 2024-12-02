import unittest
import src.auth_utils.hasher as hasher

class TestHasher(unittest.TestCase):
	def test_hash_string(self):
		unhashed_string = "unhashed string"
		# From https://sha512.online/
		expected_hash = "c2768a1e910a1476cd214aef96917595d0ada676a892cbe3c294fe7e14a331da2f74ae05c61f7ed8f6467b260e3afd5906b321e163eba216bccaba0208d56335"
		hashed_string = hasher.hash_string(unhashed_string)

		self.assertEqual(hashed_string, expected_hash)

	def test_hash_string_empty(self):
		unhashed_string = ""
		# From https://sha512.online/
		expected_hash = "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e"
		hashed_string = hasher.hash_string(unhashed_string)

		self.assertEqual(hashed_string, expected_hash)

	def test_hash_string_password(self):
		unhashed_string = "abbottpassword"
		# From https://sha512.online/
		expected_hash = "fa5514aeb04d6fe8d8e66fd1b96e1dfde90688e35e3cf810993d5dce98afb8b9c636bcc939bd81251297a52185606e8c9420c793d2f6a98f93f5ac711d9d3f64"
		hashed_string = hasher.hash_string(unhashed_string)

		self.assertEqual(hashed_string, expected_hash)

	def test_hash_string_number(self):
		unhashed_string = 982

		self.assertRaises(AttributeError, hasher.hash_string, unhashed_string)

	def test_matches_hashed_value_true(self):
		expected_string_value = "password"
		expected_hash_value = hasher.hash_string(expected_string_value)
		input_string = "password"

		does_match = hasher.matches_hashed_value(input_string, expected_hash_value)

		self.assertTrue(does_match)

	def test_matches_hashed_value_false(self):

		expected_string_value = "password"
		expected_hash_value = hasher.hash_string(expected_string_value)
		input_string = "password2"

		does_match = hasher.matches_hashed_value(input_string, expected_hash_value)

		self.assertFalse(does_match)