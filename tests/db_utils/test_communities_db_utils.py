import unittest
import src.db_utils.communities_db_utils as communities_db_utils

class TestCommunitiesDBUtils(unittest.TestCase):
	def test_get_communities(self):
		communities = communities_db_utils.get_communities()
		self.assertEqual(len(communities), 2)

	def test_get_community(self):
		arrakis_community_id = 1
		arrakis_community_name = "Arrakis"
		community = communities_db_utils.get_community(arrakis_community_id)

		self.assertIsNotNone(community)
		self.assertEqual(community["id"], arrakis_community_id)
		self.assertEqual(community["name"], arrakis_community_name)