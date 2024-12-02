import unittest
import src.auth_utils.session_key_utils as session_key_utils

class TestSessionKeyUtils(unittest.TestCase):
	def test_generate_session_key(self):
		session_key = session_key_utils.generate_session_key()
		expected_length = session_key_utils.KEY_LENGTH

		self.assertIsInstance(session_key, str)
		self.assertEqual(len(session_key), expected_length)

	def test_generate_session_key_1000(self):
		expected_length = session_key_utils.KEY_LENGTH
		session_keys = set()  # Use a set to track unique keys

		for _ in range(1000):
			session_key = session_key_utils.generate_session_key()

			self.assertEqual(len(session_key), expected_length)
			self.assertNotIn(session_key, session_keys)

			session_keys.add(session_key)

		self.assertEqual(len(session_keys), 1000)
