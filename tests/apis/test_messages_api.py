import unittest
import datetime
import tests.apis.api_test_utils as api_test_utils

class TestMessagesAPI(unittest.TestCase):
	def test_messages_endpoint_search_query(self):
		search_string = "reply please"

		messages_response = api_test_utils.send_get_request(self,
			f"messages?search_query={search_string}",
			headers={
				"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
			},
		)

		self.assertIsNotNone(messages_response)
		self.assertEqual(len(messages_response), 1)
		self.assertEqual(messages_response[0]["message"], "please reply")

	def test_messages_endpoint_no_query(self):
		messages_response = api_test_utils.send_get_request(self,
			f"messages",
			headers={
				"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
			},
		)

		self.assertIsNotNone(messages_response)
		self.assertGreater(len(messages_response), 0)

	def test_messages_endpoint_start_date(self):
		start_date_str = "2022-01-01"

		messages_response = api_test_utils.send_get_request(self,
			f"messages?start_date={start_date_str}",
			headers={
				"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
			},
		)

		self.assertIsNotNone(messages_response)

		for messsage in messages_response:
			time_sent_str = messsage["time_sent"]

			time_sent = datetime.datetime.strptime(time_sent_str, "%a, %d %b %Y %H:%M:%S GMT")
			start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")

			self.assertGreaterEqual(time_sent, start_date)

	def test_messages_endpoint_end_date(self):
		end_date_str = "2022-01-01"

		messages_response = api_test_utils.send_get_request(self,
			f"messages?end_date={end_date_str}",
			headers={
				"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
			},
		)

		self.assertIsNotNone(messages_response)

		for messsage in messages_response:
			time_sent_str = messsage["time_sent"]

			time_sent = datetime.datetime.strptime(time_sent_str, "%a, %d %b %Y %H:%M:%S GMT")
			end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")

			self.assertLessEqual(time_sent, end_date)

	def test_messages_endpoint_start_and_end_date(self):
		start_date_str = "2024-12-08"
		end_date_str = "2024-12-10"

		messages_response = api_test_utils.send_get_request(self,
			f"messages?start_date={start_date_str}&end_date={end_date_str}",
			headers={
				"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
			},
		)

		self.assertIsNotNone(messages_response)

		for messsage in messages_response:
			time_sent_str = messsage["time_sent"]

			time_sent = datetime.datetime.strptime(time_sent_str, "%a, %d %b %Y %H:%M:%S GMT")
			start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
			end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")

			self.assertGreaterEqual(time_sent, start_date)
			self.assertLessEqual(time_sent, end_date)

	def test_messages_endpoint_search_query_start_and_end_date(self):
		search_string = "Hello"
		start_date = "2024-12-08"
		end_date = "2024-12-10"

		messages_response = api_test_utils.send_get_request(self,
			f"messages?search_query={search_string}&start_date={start_date}&end_date={end_date}",
			headers={
				"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
			},
		)

		self.assertIsNotNone(messages_response)
		self.assertEqual(len(messages_response), 1)

	def test_messages_endpoint_post_direct(self):
		print("\n\nTEST 11) You can add a new DM")

		paul_id = 7
		reciever_user_id = 2
		message = "Hello"

		headers={
			"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
		}
		body={
			"reciever_user_id": reciever_user_id,
			"message": message
		}

		messages_response = api_test_utils.send_post_request(
			self,
			"messages?type=direct",
			headers=headers,
			body=body,
		)
		print("  Made POST Request on messages?type=direct")
		print("    headers:", headers)
		print("    body:", body)
		print("  200 Response Recieved: ", messages_response)
		print("  ✅ Direct Message Sent")

		self.assertIsNotNone(messages_response)
		self.assertEqual(messages_response["sender_user_id"], paul_id)
		self.assertEqual(messages_response["receiver_user_id"], reciever_user_id)
		self.assertEqual(messages_response["message"], message)

	def test_messages_endpoint_post_direct_no_auth(self):
		reciever_user_id = 2
		message = "Hello"

		response = api_test_utils.send_post_request(
			self,
			"messages?type=direct",
			body={
				"reciever_user_id": reciever_user_id,
				"message": message
			},
			expected_code=401
		)

		self.assertIsNotNone(response)
		self.assertEqual(response["message"], "Invalid session token")

	def test_messages_endpoint_post(self):
		reciever_user_id = 2
		message = "Hello"

		response = api_test_utils.send_post_request(
			self,
			"messages",
			headers={
				"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
			},
			body={
				"reciever_user_id": reciever_user_id,
				"message": message
			},
			expected_code=400
		)

		self.assertIsNotNone(response)
		self.assertEqual(response["message"], "message type None not supported")

	def test_messages_endpoint_post_no_message(self):
		reciever_user_id = 2

		response = api_test_utils.send_post_request(
			self,
			"messages?type=direct",
			headers={
				"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
			},
			body={
				"reciever_user_id": reciever_user_id,
			},
			expected_code=400
		)

		self.assertIsNotNone(response)
		self.assertEqual(response["message"], "message must be provided in body")

	def test_messages_endpoint_post_no_reciever(self):
		message = "Hello"

		response = api_test_utils.send_post_request(
			self,
			"messages?type=direct",
			headers={
				"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
			},
			body={
				"message": message,
			},
			expected_code=400
		)

		self.assertIsNotNone(response)
		self.assertEqual(response["message"], "reciever_user_id must be provided in body")