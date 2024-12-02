from . import swen344_db_utils as db_utils

def get_communities():
	"""
	Retrieves all communities from the database.

	Assumptions:
		The caller has administrative privileges.

	Returns:
		list: A list of communities. Each community being a dictionary mapping community column names to their corresponding data.
	"""
	communities = db_utils.exec_get_all_rows('SELECT * FROM communities')
	return communities

def get_community(community_id):
	"""
	Retrieves a community from the database by ID.

	Args:
		community_id (int): The ID of the community to retrieve.

	Returns:
		tuple: The retrieved community. A community being a dictionary mapping community column names to their corresponding data.
	"""
	return db_utils.exec_get_first_row(
		"SELECT * FROM communities WHERE id = %(community_id)s",
		{'community_id': community_id}
	)