from . import swen344_db_utils as db_utils

def get_channels():
	"""
	Retrieves all channels from the database.

	Assumptions:
		The caller has administrative privileges.

	Returns:
		list: A list of channels. Each channel being a dictionary mapping channel column names to their corresponding data.
	"""
	channels = db_utils.exec_get_all_rows("SELECT * FROM channels")
	return channels

def get_channel(channel_id):
	"""
	Retrieves a channel from the database by ID.

	Args:
		channel_id (int): The ID of the channel to retrieve.

	Returns:
		tuple: The retrieved channel. A channel being a dictionary mapping channel column names to their corresponding data.
	"""
	return db_utils.exec_get_first_row(
		"SELECT * FROM channels WHERE id = %(channel_id)s",
		{'channel_id': channel_id}
	)

def get_channels_in_community(community_id):
	"""
	Retrieves all channels in the specified community.

	Args:
		community_id (int): The ID of the community to retrieve channels from.

	Returns:
		list: A list of channels in the specified community. Each channel being a dictionary mapping channel column names to their corresponding data.
	"""
	return db_utils.exec_get_all_rows(
		"SELECT * FROM channels WHERE community_id = %(community_id)s",
		{'community_id': community_id}
	)