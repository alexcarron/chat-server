import unittest
from src.db_utils import messages_db_utils, chat_db_utils

class TestMessagesDBUtils(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		chat_db_utils.rebuild_tables()

	def test_search_messages_no_results(self):
		search_string = "giraffe"

		messages_found = messages_db_utils.search_messages(search_string)

		self.assertEqual(len(messages_found), 0)

	def test_search_messages_reply(self):
		search_string = "reply"

		messages_found = messages_db_utils.search_messages(search_string)

		self.assertEqual(len(messages_found), 2)

		self.assertEqual(messages_found[0]["message"], "please reply")
		self.assertEqual(messages_found[1]["message"], "i replied already!")

	def test_search_messages_reply_please(self):
		search_string = "reply please"

		messages_found = messages_db_utils.search_messages(search_string)

		self.assertEqual(len(messages_found), 1)

		self.assertEqual(messages_found[0]["message"], "please reply")

	def test_search_messages_no_query(self):
		messages_found = messages_db_utils.search_messages()

		self.assertEqual(len(messages_found), 17)

	def test_search_messages_start_date(self):
		start_date = "2022-01-01"

		messages_found = messages_db_utils.search_messages(start_date=start_date)

		self.assertEqual(len(messages_found), 8)

	def test_search_messages_end_date(self):
		end_date = "2022-01-01"

		messages_found = messages_db_utils.search_messages(end_date=end_date)

		self.assertEqual(len(messages_found), 9)

	def test_search_messages_start_and_end_date(self):
		start_date = "2024-12-08"
		end_date = "2024-12-10"

		messages_found = messages_db_utils.search_messages(start_date=start_date, end_date=end_date)

		self.assertEqual(len(messages_found), 4)

	def test_search_messages_query_start_and_end_date(self):
		search_string = "Hello"
		start_date = "2024-12-08"
		end_date = "2024-12-10"

		messages_found = messages_db_utils.search_messages(search_string, start_date, end_date)

		self.assertEqual(len(messages_found), 1)

	def test_get_messages_in_channel(self):
		random_channel_id = 2
		expected_num_messages = 2

		messages = messages_db_utils.get_messages_in_channel(random_channel_id)

		self.assertEqual(len(messages), expected_num_messages)

		for message in messages:
			self.assertEqual(message["channel_id"], random_channel_id)

	def test_get_messages_from_user(self):
		abbott_id = 1
		expected_num_messages = 5

		messages = messages_db_utils.get_messages_from_user(abbott_id)

		self.assertEqual(len(messages), expected_num_messages)

		for message in messages:
			self.assertIn("id", message)
			self.assertEqual(message["sender_user_id"], abbott_id)
			self.assertIn("message", message)
			self.assertIn("time_sent", message)
			self.assertIn("is_read", message)
			self.assertTrue(
				("channel_id" in message) or
				("receiver_user_id" in message)
			)

	def test_get_messages_from_user_invalid_user(self):
		fake_id = -1

		messages = messages_db_utils.get_messages_from_user(fake_id)

		self.assertEqual(len(messages), 0)

	def test_get_messages_from_user_invalid_type(self):
		abbott_id = 1
		msg_type = "invalid"

		self.assertRaises(RuntimeError, messages_db_utils.get_messages_from_user, abbott_id, type=msg_type)

	def test_get_messages_from_user_negative_max_messages(self):
		abbott_id = 1
		max_messages = -1

		self.assertRaises(RuntimeError, messages_db_utils.get_messages_from_user, abbott_id, max_messages=max_messages)

	def test_get_messages_from_user_channel(self):
		abbott_id = 1
		expected_num_messages = 1

		messages = messages_db_utils.get_messages_from_user(abbott_id, type="channel")

		self.assertEqual(len(messages), expected_num_messages)

		for message in messages:
			self.assertIn("id", message)
			self.assertEqual(message["sender_user_id"], abbott_id)
			self.assertIn("message", message)
			self.assertIn("time_sent", message)
			self.assertIn("is_read", message)
			self.assertIn("channel_id", message)

	def test_get_messages_from_user_max_messages(self):
		abbott_id = 1
		max_messages = 1

		messages = messages_db_utils.get_messages_from_user(abbott_id, max_messages=max_messages)

		self.assertEqual(len(messages), max_messages)

		for message in messages:
			self.assertIn("id", message)
			self.assertEqual(message["sender_user_id"], abbott_id)
			self.assertIn("message", message)
			self.assertIn("time_sent", message)
			self.assertIn("is_read", message)
			self.assertTrue(
				("channel_id" in message) or
				("receiver_user_id" in message)
			)

	def test_get_messages_from_user_direct_max_messages(self):
		abbott_id = 1
		max_messages = 1


		messages = messages_db_utils.get_messages_from_user(abbott_id, type="direct", max_messages=max_messages)

		self.assertEqual(len(messages), max_messages)

		for message in messages:
			self.assertIn("id", message)
			self.assertEqual(message["sender_user_id"], abbott_id)
			self.assertIn("message", message)
			self.assertIn("time_sent", message)
			self.assertIn("is_read", message)
			self.assertIn("receiver_user_id", message)

	def test_send_direct_message(self):
		abbott_id = 1
		receiver_id = 2
		message = "Hello"

		direct_message = messages_db_utils.send_direct_message(abbott_id, receiver_id, message)

		self.assertEqual(direct_message["sender_user_id"], abbott_id)
		self.assertEqual(direct_message["receiver_user_id"], receiver_id)
		self.assertEqual(direct_message["message"], message)

		chat_db_utils.rebuild_tables()

	def test_send_direct_message_invalid_sender(self):
		fake_id = -1
		receiver_id = 2
		message = "Hello"

		self.assertRaises(Exception, messages_db_utils.send_direct_message, fake_id, receiver_id, message)

	def test_send_direct_message_invalid_reciever(self):
		sender_id = 1
		receiver_id = -1
		message = "Hello"

		self.assertRaises(Exception, messages_db_utils.send_direct_message, sender_id, receiver_id, message)