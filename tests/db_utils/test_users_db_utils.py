import unittest
import datetime
from src.db_utils import users_db_utils, chat_db_utils
import src.db_utils.swen344_db_utils as db_utils

class TestUsersDBUtils(unittest.TestCase):
	def setUp(self):
		chat_db_utils.rebuild_tables()

	def test_get_users(self):
		users = users_db_utils.get_users()
		self.assertEqual(len(users), 7)

	def test_get_user(self):
		user_id = 2
		num_user_columns = 6
		username = "Costello"
		email = "costello@example.com"
		last_username_change_time = None

		user = users_db_utils.get_user(user_id)

		self.assertIsNotNone(user)
		self.assertEqual(len(user), num_user_columns)
		self.assertEqual(user["id"], user_id)
		self.assertEqual(user["username"], username)
		self.assertEqual(user["email"], email)
		self.assertEqual(user["last_username_change_time"], last_username_change_time)

	def test_get_id_of_login_exists(self):
		abbott_username = "Abbott"
		abbott_hashed_password = "fa5514aeb04d6fe8d8e66fd1b96e1dfde90688e35e3cf810993d5dce98afb8b9c636bcc939bd81251297a52185606e8c9420c793d2f6a98f93f5ac711d9d3f64"

		user_id = users_db_utils.get_id_of_login(abbott_username, abbott_hashed_password)
		self.assertEqual(user_id, 1)

	def test_get_id_of_login_wrong_password(self):
		abbott_username = "Abbott"
		abbott_hashed_password = "fa5514aeb04d6fe8d8e66fd1b96e1dfde90688e35e3cf810993d5dce98afb8b9c636bcc939bd81251297a52185606e7c9420c793d2f6a98f93f5ac711d9d3f64"

		user_id = users_db_utils.get_id_of_login(abbott_username, abbott_hashed_password)
		self.assertIsNone(user_id)

	def test_get_id_of_login_wrong_username(self):
		abbott_username = "Costello"
		abbott_hashed_password = "fa5514aeb04d6fe8d8e66fd1b96e1dfde90688e35e3cf810993d5dce98afb8b9c636bcc939bd81251297a52185606e8c9420c793d2f6a98f93f5ac711d9d3f64"

		user_id = users_db_utils.get_id_of_login(abbott_username, abbott_hashed_password)
		self.assertIsNone(user_id)

	def test_get_id_of_login_nonexistant_username(self):
		abbott_username = "Abott"
		abbott_hashed_password = "fa5514aeb04d6fe8d8e66fd1b96e1dfde90688e35e3cf810993d5dce98afb8b9c636bcc939bd81251297a52185606e8c9420c793d2f6a98f93f5ac711d9d3f64"

		user_id = users_db_utils.get_id_of_login(abbott_username, abbott_hashed_password)
		self.assertIsNone(user_id)

	def test_start_user_session_true(self):
		abbott_id = 1
		session_key = "fa5514aeb04d6fe8d8e66fd1b96e1dfde90688e35e3cf810993d5dce98afb8b9c636bcc939bd81251297a52185606e8c9420c793d2f6a98f93f5ac711d9d3f64"

		is_session_started = users_db_utils.start_new_user_session(abbott_id, session_key)
		self.assertTrue(is_session_started)

		user_session_key = db_utils.exec_get_first_value(
			"""
			SELECT session_key FROM users
				WHERE id = %(user_id)s
			""",
			{'user_id': abbott_id}
		)
		self.assertEqual(user_session_key, session_key)

	def test_start_user_session_false(self):
		fake_user_id = -1
		session_key = "fa5514aeb04d6fe8d8e66fd1b96e1dfde90688e35e3cf810993d5dce98afb8b9c636bcc939bd81251297a52185606e8c9420c793d2f6a98f93f5ac711d9d3f64"

		is_session_started = users_db_utils.start_new_user_session(fake_user_id, session_key)
		self.assertFalse(is_session_started)

	def test_end_user_session_no_session(self):
		abbott_id = 1


		users_db_utils.end_user_session(abbott_id)
		ended_existing_session = users_db_utils.end_user_session(abbott_id)

		self.assertFalse(ended_existing_session)

		user_session_key = db_utils.exec_get_first_value(
			"""
			SELECT session_key FROM users
				WHERE id = %(user_id)s
			""",
			{'user_id': abbott_id}
		)
		self.assertIsNone(user_session_key)

	def test_end_user_session_with_session(self):
		abbott_id = 1
		session_key = "fa5514aeb04d6fe8d8e66fd1b96e1dfde90688e35e3cf810993d5dce98afb8b9c636bcc939bd81251297a52185606e8c9420c793d2f6a98f93f5ac711d9d3f64"

		users_db_utils.start_new_user_session(abbott_id, session_key)

		is_session_ended = users_db_utils.end_user_session(abbott_id)
		self.assertTrue(is_session_ended)

		user_session_key = db_utils.exec_get_first_value(
			"""
			SELECT session_key FROM users
				WHERE id = %(user_id)s
			""",
			{'user_id': abbott_id}
		)
		self.assertIsNone(user_session_key)

	def test_end_user_session_no_user(self):
		fake_user_id = -1
		session_key = "fa5514aeb04d6fe8d8e66fd1b96e1dfde90688e35e3cf810993d5dce98afb8b9c636bcc939bd81251297a52185606e8c9420c793d2f6a98f93f5ac711d9d3f64"

		users_db_utils.start_new_user_session(fake_user_id, session_key)

		is_session_ended = users_db_utils.end_user_session(fake_user_id)
		self.assertFalse(is_session_ended)
		self.assertFalse(is_session_ended)

	def test_get_user_id_of_session_key_after_started(self):
		abbott_id = 1
		session_key = "fa5514aeb04d6fe8d8e66fd1b96e1dfde90688e35e3cf810993d5dce98afb8b9c636bcc939bd81251297a52185606e8c9420c793d2f6a98f93f5ac711d9d3f64"

		users_db_utils.start_new_user_session(abbott_id, session_key)

		user_id = users_db_utils.get_user_id_of_session_key(session_key)
		self.assertEqual(user_id, abbott_id)

	def test_get_user_id_of_session_key_after_ended(self):
		abbott_id = 1
		session_key = "fa5514aeb04d6fe8d8e66fd1b96e1dfde90688e35e3cf810993d5dce98afb8b9c636bcc939bd81251297a52185606e8c9420c793d2f6a98f93f5ac711d9d3f64"

		users_db_utils.end_user_session(abbott_id)

		user_id = users_db_utils.get_user_id_of_session_key(session_key)
		self.assertIsNone(user_id)

	def test_get_user_id_of_session_key_after_replaced(self):
		abbott_id = 1
		old_session_key = "fa5514aeb04d6fe8d8e66fd1b96e1dfde90688e35e3cf810993d5dce98afb8b9c636bcc939bd81251297a52185606e8c9420c793d2f6a98f93f5ac711d9d3f64"

		users_db_utils.start_new_user_session(abbott_id, old_session_key)

		new_session_key = "ba5514aeb04d6fe8d8e66fd1b96e1dfde90688e35e3cf810993d5dce98afb8b9c636bcc939bd81251297a52185606e8c9420c793d2f6a98f93f5ac711d9d3f64"

		users_db_utils.start_new_user_session(abbott_id, new_session_key)

		old_session_user_id = users_db_utils.get_user_id_of_session_key(old_session_key)
		new_session_user_id = users_db_utils.get_user_id_of_session_key(new_session_key)

		self.assertIsNone(old_session_user_id)
		self.assertEqual(new_session_user_id, abbott_id)

	def test_add_user_bob_and_marvin(self):
		marvin = users_db_utils.add_user('DrMarvin', 'hashed_password',  'marvin@example.com')
		bob = users_db_utils.add_user('Bob', 'hashed_password', None)

		self.assertIsNotNone(marvin)
		self.assertIsNotNone(bob)
		self.assertNotEqual(marvin['id'], bob['id'])

		marvin = users_db_utils.get_user(marvin['id'])
		bob = users_db_utils.get_user(bob['id'])

		self.assertEqual(marvin['username'], 'DrMarvin')
		self.assertEqual(marvin['password'], 'hashed_password')
		self.assertEqual(marvin['email'], 'marvin@example.com')
		self.assertEqual(bob['username'], 'Bob')
		self.assertEqual(bob['password'], 'hashed_password')
		self.assertIsNone(bob['email'])

	def test_update_user(self):
		abbott_id = 1
		new_username = 'Joseph'
		new_email = 'joseph@example.com'
		new_password = 'new_hashed_password'

		updated_user = users_db_utils.update_user(abbott_id, username=new_username, email=new_email, hashed_password=new_password)

		self.assertIsNotNone(updated_user)
		self.assertEqual(updated_user['id'], abbott_id)
		self.assertEqual(updated_user['username'], new_username)
		self.assertEqual(updated_user['email'], new_email)
		self.assertEqual(updated_user['password'], new_password)

		joseph = users_db_utils.get_user(1)
		self.assertEqual(joseph['username'], new_username)
		self.assertEqual(joseph['email'], new_email)
		self.assertEqual(joseph['password'], new_password)

	def test_update_user_no_changes(self):
		abbott_id = 1
		abbott = users_db_utils.get_user(abbott_id)

		updated_user = users_db_utils.update_user(abbott_id)

		self.assertIsNotNone(updated_user)
		self.assertEqual(updated_user['id'], abbott_id)
		self.assertEqual(updated_user['username'], abbott['username'])
		self.assertEqual(updated_user['email'], abbott['email'])
		self.assertEqual(updated_user['password'], abbott['password'])
		self.assertIsNone(updated_user['last_username_change_time'])

	def test_update_user_duplicate_username(self):
		abbott_id = 1
		new_username = 'Costello'
		new_email = 'joseph@example.com'
		new_password = 'new_hashed_password'

		self.assertRaises(Exception, users_db_utils.update_user, abbott_id, username=new_username, email=new_email, hashed_password=new_password)

	def test_update_user_duplicate_email(self):
		abbott_id = 1
		new_username = 'Joseph'
		new_email = 'costello@example.com'
		new_password = 'new_hashed_password'

		self.assertRaises(Exception, users_db_utils.update_user, abbott_id, username=new_username, email=new_email, hashed_password=new_password)

	def test_update_user_fake_user(self):
		fake_user_id = -1
		new_username = 'Joseph'
		new_email = 'costello@example.com'
		new_password = 'new_hashed_password'

		updated_user = users_db_utils.update_user(fake_user_id, username=new_username, email=new_email, hashed_password=new_password)

		self.assertIsNone(updated_user)

	def test_update_user_last_change_time(self):
		todays_date = datetime.datetime.now().strftime('%Y-%m-%d')

		bob = users_db_utils.add_user('Bob', 'bobpassword', 'bob@example.com')

		updated_user = users_db_utils.update_user(bob['id'], username="BabySteps2Door")

		self.assertEqual(updated_user['username'], 'BabySteps2Door')
		self.assertIsNotNone(updated_user['last_username_change_time'])
		self.assertEqual(updated_user['last_username_change_time'].strftime('%Y-%m-%d'), todays_date)

	def test_update_user_cant_change_username(self):
		todays_date = datetime.datetime.now().strftime('%Y-%m-%d')
		bob = users_db_utils.add_user('Bob', 'bobpassword', 'bob@example.com')

		users_db_utils.update_user(bob['id'], username="BabySteps2Door")

		self.assertRaises(RuntimeError, users_db_utils.update_user, bob['id'], username="BabySteps2Elevator")

		updated_user = users_db_utils.get_user(bob['id'])
		self.assertEqual(updated_user['username'], 'BabySteps2Door')
		self.assertIsNotNone(updated_user['last_username_change_time'])
		self.assertEqual(updated_user['last_username_change_time'].strftime('%Y-%m-%d'), todays_date)

	def test_delete_user_exists(self):
		abbott_id = 1
		deleted_user = users_db_utils.delete_user(abbott_id)

		self.assertIsNotNone(deleted_user)
		self.assertEqual(deleted_user['id'], abbott_id)

		self.assertIsNone(users_db_utils.get_user(abbott_id))

		deleted_user = users_db_utils.delete_user(abbott_id)
		self.assertIsNone(deleted_user)

		chat_db_utils.rebuild_tables()

	def test_delete_user_does_not_exist(self):
		fake_user_id = -1
		deleted_user = users_db_utils.delete_user(fake_user_id)

		self.assertIsNone(deleted_user)