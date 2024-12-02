from . import swen344_db_utils as db_utils


def delete_all_tables():
	"""Delete all the tables in the database."""
	db_utils.exec_sql_file('chat_schema_cleanup.sql')

def rebuild_tables():
	"""Delete and rebuild all the tables in the database."""
	delete_all_tables()
	db_utils.exec_sql_file('chat_schema_setup.sql')
	db_utils.exec_sql_file('insert_test_data.sql')

def do_all_tables_exist():
	"""
	Checks if all the tables in the database exist.

	Returns:
		bool: `True` if all the tables exist, `False` otherwise.
	"""
	try:
		suspensions = db_utils.exec_get_all_rows('SELECT * FROM suspensions')
		direct_messages = db_utils.exec_get_all_rows('SELECT * FROM direct_messages')
		channel_messages = db_utils.exec_get_all_rows('SELECT * FROM channel_messages')
		messages = db_utils.exec_get_all_rows('SELECT * FROM messages')
		users = db_utils.exec_get_all_rows('SELECT * FROM users')
		channels = db_utils.exec_get_all_rows('SELECT * FROM channels')
		communities = db_utils.exec_get_all_rows('SELECT * FROM communities')
	except Exception:
		return False

	return (
		len(suspensions) > 0 and
		len(direct_messages) > 0 and
		len(channel_messages) > 0 and
		len(communities) > 0 and
		len(channels) > 0 and
		len(messages) > 0 and
		len(users) > 0
	)