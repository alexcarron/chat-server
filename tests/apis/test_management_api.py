import unittest
import tests.apis.api_test_utils as api_test_utils

class TestManagementApi(unittest.TestCase):
	def test_management_init_endpoint(self):
		api_test_utils.send_post_request(self, "manage/init")

	def test_management_Version_endpoint(self):
		version = api_test_utils.send_get_request(self,
			f"manage/version"
		)
		self.assertTrue(version["version"].startswith("PostgreSQL"))