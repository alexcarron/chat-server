import unittest
import tests.apis.api_test_utils as api_test_utils

class TestCommunitiesAPI(unittest.TestCase):
	def test_communities_endpoint(self):
		communities_response = api_test_utils.send_get_request(self, "communities")

		self.assertIsNotNone(communities_response)
		self.assertEqual(len(communities_response), 2)

	def test_communities_id_endpoint(self):
		arrakis_community_id = 1
		arrakis_community_name = "Arrakis"

		community_response = api_test_utils.send_get_request(self,
			f"communities/{arrakis_community_id}",
			headers={
				"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
			},
		)

		self.assertIsNotNone(community_response)
		self.assertEqual(community_response["id"], arrakis_community_id)
		self.assertEqual(community_response["name"], arrakis_community_name)

	def test_community_channels_endpoint(self):
		arrakis_community_id = 1

		channels_response = api_test_utils.send_get_request(self,
			f"communities/{arrakis_community_id}/channels",
			headers={
				"Authorization": "ca1ac3ec69751daa3ec0cbc18c6b26196569bd17560aba6b472c0f6031c02070c19a30f1f4f68e7770e80d947f36998c0353a3c8ce74a32ebd3c1c1ac32558f3"
			},
		)

		self.assertIsNotNone(channels_response)
		self.assertEqual(len(channels_response), 2)