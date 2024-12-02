import unittest
import tests.apis.api_test_utils as api_test_utils

class TestChannelsAPI(unittest.TestCase):
	def test_channels_endpoint(self):
		channels_response = api_test_utils.send_get_request(self, "channels",
		headers={
			"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
		},)

		self.assertIsNotNone(channels_response)
		self.assertEqual(len(channels_response), 4)

	def test_channels_id_endpoint(self):
		worms_channel_id = 1
		arrakis_community_id = 1
		worms_channel_name = "Worms"

		channel_response = api_test_utils.send_get_request(self,
			f"channels/{worms_channel_id}",
			headers={
				"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
			}
		)

		self.assertIsNotNone(channel_response)
		self.assertEqual(channel_response["id"], worms_channel_id)
		self.assertEqual(channel_response["community_id"], arrakis_community_id)
		self.assertEqual(channel_response["name"], worms_channel_name)

	def test_channel_messages_endpoint(self):
		random_channel_id = 2
		expected_num_messages = 2

		messages_response = api_test_utils.send_get_request(self,
			f"channels/{random_channel_id}/messages",
			headers={
				"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
			}
		)

		self.assertIsNotNone(messages_response)
		self.assertEqual(len(messages_response), expected_num_messages)
		for message in messages_response:
			self.assertEqual(message["channel_id"], random_channel_id)

	def test_channel_messages_endpoint_bad_channel(self):
		bad_channel_id = 9999
		expected_num_messages = 0

		messages_response = api_test_utils.send_get_request(self,
			f"channels/{bad_channel_id}/messages",
			headers={
				"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
			}
		)

		self.assertIsNotNone(messages_response)
		self.assertEqual(len(messages_response), expected_num_messages)