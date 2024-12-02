import unittest
import tests.apis.api_test_utils as api_test_utils

class TestLoginAPI(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		api_test_utils.send_post_request(None, "manage/init")
	def test_login_endpoint_success(self):
		print("\n\nTEST 3.1) You can login successfully with the right userID and password")

		body = {"username": "Abbott", "password": "abbottpassword"}

		result_body = api_test_utils.send_post_request(
			self,
			"login",
			body,
			expected_code=200
		)
		print("  Made POST Request on /login")
		print("    body: ", body)
		print("  200 Response Recieved: ", result_body)
		print("  ✅ Succesfully Logged In")

		self.assertIsNotNone(result_body)

		self.assertIn("session_key", result_body)
		session_key = result_body["session_key"]
		self.assertIsNotNone(session_key)

		self.assertIn("message", result_body)
		self.assertEqual(result_body["message"], "Logged in successfully")

		headers = {
			"Authorization": session_key
		}

		print("\n  3.2) Hashing is performed as described")
		user_response = api_test_utils.send_get_request(
			self,
			"users/1",
			headers=headers
		)
		print("  Made GET Request on /users/1")
		print("    headers: ", headers)
		print("  200 Response Recieved: ", user_response)
		print("  ✅ Stored password is not same as plaintext password")

		self.assertNotEqual(user_response['password'], 'abbottpassword')

	def test_login_endpoint_failure(self):
		print("\n\nTEST 4) Incorrect passwords fail login")

		body={"username": "abbott", "password": "wrongpassword"}

		result_body = api_test_utils.send_post_request(
			self,
			"login",
			body,
			expected_code=401
		)
		print("  Made POST Request on /login")
		print("    body: ", body)
		print("  401 Response Recieved: ", result_body)
		print("  ❌ Request Failed Due To Invalid Password")

		self.assertEqual(result_body["message"], "Invalid username or password")

	def test_logout_endpoint_success(self):
		result_body = api_test_utils.send_post_request(
			self,
			"login",
			{"username": "Abbott", "password": "abbottpassword"},
			expected_code=200
		)

		session_key = result_body["session_key"]

		result_body = api_test_utils.send_post_request(
			self,
			"logout",
			headers={"Authorization": session_key},
			expected_code=200
		)

		self.assertEqual(result_body["message"], "Logged out successfully")

	def test_logout_endpoint_no_session_token(self):
		result_body = api_test_utils.send_post_request(
			self,
			"logout",
			expected_code=401
		)

		self.assertEqual(result_body["message"], "Invalid session token")

	def test_logout_endpoint_invalid_session_token(self):
		result_body = api_test_utils.send_post_request(
			self,
			"logout",
			headers={"Authorization": "invalid_token"},
			expected_code=401
		)

		self.assertEqual(result_body["message"], "Invalid session token")