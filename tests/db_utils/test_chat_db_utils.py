import unittest
import src.db_utils.chat_db_utils as chat_db_utils

class TestChatDBUtils(unittest.TestCase):
	def test_rebuild_tables(self):
		"""Rebuild the tables"""
		chat_db_utils.rebuild_tables()
		self.assertTrue(chat_db_utils.do_all_tables_exist())

	def test_rebuild_tables_is_idempotent(self):
		"""Drop and rebuild the tables twice"""
		chat_db_utils.rebuild_tables()
		chat_db_utils.rebuild_tables()
		self.assertTrue(chat_db_utils.do_all_tables_exist())

	def test_do_all_tables_exist(self):
		"""Check if all the tables exist"""
		chat_db_utils.delete_all_tables()
		self.assertFalse(chat_db_utils.do_all_tables_exist())

		chat_db_utils.rebuild_tables()
		self.assertTrue(chat_db_utils.do_all_tables_exist())