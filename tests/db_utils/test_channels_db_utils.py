import unittest
import src.db_utils.channels_db_utils as channels_db_utils

class TestCommunitiesDBUtils(unittest.TestCase):
	def test_get_channels(self):
		communities = channels_db_utils.get_channels()
		self.assertEqual(len(communities), 4)

	def test_get_channel(self):
		worms_channel_id = 1
		arrakis_community_id = 1
		worms_channel_name = "Worms"

		channel = channels_db_utils.get_channel(worms_channel_id)

		self.assertIsNotNone(channel)
		self.assertEqual(channel["id"], worms_channel_id)
		self.assertEqual(channel["community_id"], arrakis_community_id)
		self.assertEqual(channel["name"], worms_channel_name)

	def test_get_channels_in_community(self):
		arrakis_community_id = 1

		channels = channels_db_utils.get_channels_in_community(arrakis_community_id)

		self.assertEqual(len(channels), 2)

		for channel in channels:
			self.assertEqual(channel["community_id"], arrakis_community_id)
