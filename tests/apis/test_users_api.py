import unittest
import datetime
import tests.apis.api_test_utils as api_test_utils

class TestUsersAPI(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		api_test_utils.send_post_request(None, "manage/init")

	def test_users_endpoint_get(self):
		users_response = api_test_utils.send_get_request(self, "users",
			headers={
				"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
			},)

		self.assertIsNotNone(users_response)
		self.assertEqual(len(users_response), 7)

	def test_users_endpoint_post(self):
		print("\n\nTEST 1) You can add a new user with a password and any other user information")

		headers = {
			"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
		}
		body = {
			"username": "TestUser",
			"email": "testuser@bu.edu",
			"password": "testpassword"
		}

		user_response = api_test_utils.send_post_request(
			self,
			"users",
			headers=headers,
			body=body
		)
		print("  Made POST Request on /users")
		print("    headers: ", headers)
		print("    body: ", body)
		print("  200 Response Recieved: ", user_response)
		print("  ✅ Created TestUser User")

		self.assertIsNotNone(user_response)
		self.assertIsNotNone(user_response['id'])
		self.assertEqual(user_response['username'], "TestUser")
		self.assertEqual(user_response['email'], "testuser@bu.edu")
		self.assertNotEqual(user_response['password'], "testpassword")

	def test_users_endpoint_post_no_email(self):
		user_response = api_test_utils.send_post_request(
			self,
			"users",
			headers={
				"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
			},
			body={
				"username": "TestUser2",
				"password": "testpassword"
			}
		)

		self.assertIsNotNone(user_response)
		self.assertIsNotNone(user_response['id'])
		self.assertEqual(user_response['username'], "TestUser2")
		self.assertIsNone(user_response['email'])
		self.assertNotEqual(user_response['password'], "testpassword")

	def test_users_endpoint_post_no_username(self):
		user_response = api_test_utils.send_post_request(
			self,
			"users",
			body={
				"password": "testpassword"
			},
			headers={
				"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
			},
			expected_code=400
		)

		self.assertEqual(user_response['message'], "Missing username or password")

	def test_users_endpoint_post_no_password(self):
		user_response = api_test_utils.send_post_request(
			self,
			"users",
			body={
				"username": "TestUser"
			},
			headers={
				"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
			},
			expected_code=400
		)

		self.assertEqual(user_response['message'], "Missing username or password")

	def test_users_endpoint_post_duplicate_username(self):
		print("\n\nTEST 2) If a user already exists, the add user fails")

		headers = {
			"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
		}
		body = {
			"username": "Abbott",
			"email": "different@email.edu",
			"password": "differentpassword"
		}

		user_response = api_test_utils.send_post_request(
			self,
			"users",
			body=body,
			headers=headers,
			expected_code=400
		)
		print("  Made POST Request on /users")
		print("    headers: ", headers)
		print("    body: ", body)
		print("  400 Response Recieved: ", user_response)
		print("  ❌ Request Failed Due To Username Already Existing")

		self.assertEqual(user_response['message'], "Username or email already exists")

	def test_users_endpoint_post_duplicate_email(self):
		user_response = api_test_utils.send_post_request(
			self,
			"users",
			body={
				"username": "NewUserName",
				"password": "password",
				"email": "abbott@example.com"
			},
			headers={
				"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
			},
			expected_code=400
		)

		self.assertEqual(user_response['message'], "Username or email already exists")

	def test_users_id_endpoint_get(self):
		user_id = 2
		username = "Costello"
		email = "costello@example.com"
		last_username_change_time = None

		user_response = api_test_utils.send_get_request(self,
			f"users/{user_id}",
			headers={
				"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
			},
		)

		self.assertIsNotNone(user_response)

		costello = user_response

		self.assertEqual(costello["id"], user_id)
		self.assertEqual(costello["username"], username)
		self.assertEqual(costello["email"], email)
		self.assertEqual(costello["last_username_change_time"], last_username_change_time)

	def test_users_id_endpoint_put_no_body(self):
		api_test_utils.send_post_request(self, "manage/init")

		abbott_id = 1

		abbott = api_test_utils.send_put_request(self,
			f"users/{abbott_id}",
			headers={
				"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
			},
		)

		self.assertIsNotNone(abbott)
		self.assertEqual(abbott["id"], 1)
		self.assertEqual(abbott["username"], 'Abbott')
		self.assertEqual(abbott["email"], 'abbott@example.com')
		self.assertIsNone(abbott["last_username_change_time"])

	def test_users_id_endpoint_put(self):
		print("\n\nTEST 5) You can edit a users information")

		abbott_id = 1
		new_username = 'Joseph'
		new_email = 'joseph@example.com'
		new_password = 'new_password'

		body = {
			"username": new_username,
			"email": new_email,
			"password": new_password
		}

		headers = {
			"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
		}

		abbott = api_test_utils.send_put_request(
			self,
			f"users/{abbott_id}",
			body=body,
			headers=headers,
		)
		print("  Made PUT Request on /users/1")
		print("    headers:", headers)
		print("    body:", body)
		print("  200 Response Recieved: ", abbott)
		print("  ✅ Updated User of id 1")

		last_username_change_time = datetime.datetime.strptime(
			abbott["last_username_change_time"],
			'%a, %d %b %Y %H:%M:%S GMT'
		)

		self.assertIsNotNone(abbott)
		self.assertEqual(abbott["id"], 1)
		self.assertEqual(abbott["username"], new_username)
		self.assertEqual(abbott["email"], new_email)
		self.assertNotEqual(abbott["password"], new_password)
		self.assertIsNotNone(abbott["last_username_change_time"])
		self.assertEqual(
			last_username_change_time.strftime('%Y-%m-%d'),
			datetime.datetime.now().strftime('%Y-%m-%d')
		)
		print("  User succesfully updated with new information")

		api_test_utils.send_post_request(self, "manage/init")

	def test_users_id_endpoint_put_user_not_found(self):
		print("\n\nTEST 6) If you try to edit a non-existent user, the API fails")

		fake_user_id = 999
		new_username = 'Joseph'
		new_email = 'joseph@example.com'
		new_password = 'new_password'

		headers = {
			"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
		}

		body = {
			"username": new_username,
			"email": new_email,
			"password": new_password
		}

		response = api_test_utils.send_put_request(
			self,
			f"users/{fake_user_id}",
			headers=headers,
			body=body,
			expected_code=404
		)
		print("  Made PUT Request on /users/999")
		print("    headers:", headers)
		print("    body:", body)
		print("  404 Response Recieved: ", response)
		print("  ❌ Request Failed Due To User Not Being Found")


		self.assertEqual(response["message"], "User not found")

	def test_users_id_endpoint_put_changed_recently(self):
		abbott_id = 1
		new_username = 'Joseph'
		new_username2 = 'Joey'

		api_test_utils.send_put_request(
			self,
			f"users/{abbott_id}",
			headers={
				"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
			},
			body={
				"username": new_username,
			},
		)

		response = api_test_utils.send_put_request(
			self,
			f"users/{abbott_id}",
			headers={
				"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
			},
			body={
				"username": new_username2,
			},
			expected_code=400
		)

		self.assertEqual(response["message"], "Cannot change username because user has changed username in last 6 months")

		api_test_utils.send_post_request(self, "manage/init")

	def test_users_id_endpoint_put_username_exists(self):
		api_test_utils.send_post_request(self, "manage/init")

		abbott_id = 1

		response = api_test_utils.send_put_request(
			self,
			f"users/{abbott_id}",
			headers={
				"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
			},
			body={
				"username": 'Costello',
			},
			expected_code=400
		)


		self.assertEqual(response["message"], "Username or email already exists")

	def test_users_id_endpoint_put_email_exists(self):
		abbott_id = 1

		response = api_test_utils.send_put_request(
			self,
			f"users/{abbott_id}",
			headers={
				"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
			},
			body={
				"email": 'costello@example.com',
			},
			expected_code=400
		)

		self.assertEqual(response["message"], "Username or email already exists")

	def test_users_id_endpoint_delete_existing_user(self):
		print("\n\nTEST 7.1) You can delete a user")

		abbott_id = 1

		headers = {
			"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
		}

		abbott_user = api_test_utils.send_delete_request(
			self,
			f"users/{abbott_id}",
			headers={
				"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
			},
		)
		print("  Made DELETE Request on /users/1")
		print("    headers:", headers)
		print("  200 Response Recieved: ", abbott_user)
		print("  ✅ Deleted User of ID 1")

		self.assertIsNotNone(abbott_user)
		self.assertEqual(abbott_user["id"], 1)
		print("  User succesfully deleted")

		print("\n  7.2) Again, if the user doesn’t exist, the API fails")

		response = api_test_utils.send_delete_request(
			self,
			f"users/{abbott_id}",
			headers=headers,
			expected_code=404
		)
		print("  Made DELETE Request on /users/1")
		print("    headers:", headers)
		print("  404 Response Recieved: ", response)
		print("  ❌ Request Failed Due To User Not Being Found")

		self.assertEqual(response["message"], "User not found")

		api_test_utils.send_post_request(self, "manage/init")

	def test_users_id_endpoint_delete_no_auth(self):
		print("\n\nTEST 8) If you try to remove a user (who exists), and don’t have the correct authentication session key, the API fails")

		abbott_id = 1

		response = api_test_utils.send_delete_request(
			self,
			f"users/{abbott_id}",
			expected_code=401
		)
		print("  Made DELETE Request on /users/1")
		print("    headers:", "None")
		print("  401 Response Recieved: ", response)
		print("  ❌ Request Failed Due To Invalid Session Token")


		self.assertEqual(response["message"], "Invalid session token")

	def test_users_id_endpoint_delete_non_existing_user(self):
		fake_user_id = 999

		response = api_test_utils.send_delete_request(
			self,
			f"users/{fake_user_id}",
			headers={
				"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
			},
			expected_code=404
		)

		self.assertEqual(response["message"], "User not found")

	def test_users_messages_endpoint(self):
		abbott_id = 1
		headers = {
			"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
		}

		response = api_test_utils.send_get_request(
			self,
			f"users/{abbott_id}/messages",
			headers=headers,
		)

		self.assertIsNotNone(response)
		self.assertEqual(len(response), 5)

	def test_users_messages_endpoint_direct(self):
		print("\n\nTEST 9) You can list DMs")

		abbott_id = 1
		msg_type = "direct"
		headers = {
			"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
		}

		response = api_test_utils.send_get_request(
			self,
			f"users/{abbott_id}/messages?type={msg_type}",
			headers=headers,
		)
		print("  Made GET Request on " + f"users/{abbott_id}/messages?type={msg_type}")
		print("    headers:", headers)
		print("  200 Response Recieved: ", response)
		print("  ✅ Sucesfully Recieved Direct Messages From User of ID 1")

		self.assertIsNotNone(response)
		self.assertEqual(len(response), 4)

	def test_users_messages_endpoint_direct_max_messages(self):
		print("\n\nTEST 10) You can list DMs, and specify a maximum number to return")

		abbott_id = 1
		msg_type = "direct"
		max_messages = 2

		headers = {
			"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
		}

		response = api_test_utils.send_get_request(
			self,
			f"users/{abbott_id}/messages?type={msg_type}&max_messages={max_messages}",
			headers=headers,
		)
		print("  Made GET Request on " + f"users/{abbott_id}/messages?type={msg_type}&max_messages={max_messages}")
		print("    headers:", headers)
		print("  200 Response Recieved: ", response)
		print("  ✅ Sucesfully Recieved Two or Less Direct Messages From User of ID 1")

		self.assertIsNotNone(response)
		self.assertEqual(len(response), max_messages)

	def test_users_messages_endpoint_invalid_type(self):
		abbott_id = 1
		msg_type = "invalid"
		max_messages = 2

		response = api_test_utils.send_get_request(
			self,
			f"users/{abbott_id}/messages?type={msg_type}&max_messages={max_messages}",
			headers={
				"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
			},
			expected_code=400
		)

		self.assertIsNotNone(response)
		self.assertEqual(response['message'], "type must be either 'direct', 'channel', or 'all'")

	def test_users_messages_endpoint_negative_max_messages(self):
		abbott_id = 1
		msg_type = "direct"
		max_messages = -1

		response = api_test_utils.send_get_request(
			self,
			f"users/{abbott_id}/messages?type={msg_type}&max_messages={max_messages}",
			headers={
				"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
			},
			expected_code=400
		)

		self.assertIsNotNone(response)
		self.assertEqual(response['message'], "max_messages must be greater than or equal to 0")

	def test_users_messages_endpoint_invalid_max_messages(self):
		abbott_id = 1
		msg_type = "direct"
		max_messages = "invalid"

		response = api_test_utils.send_get_request(
			self,
			f"users/{abbott_id}/messages?type={msg_type}&max_messages={max_messages}",
			headers={
				"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
			},
			expected_code=400
		)

		self.assertIsNotNone(response)
		self.assertEqual(response['message'], "max_messages must be an integer")