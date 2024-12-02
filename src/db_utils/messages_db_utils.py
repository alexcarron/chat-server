

from . import swen344_db_utils as db_utils

def search_messages(search_string=None, start_date=None, end_date=None):
	"""
	Retrieves all messages that contain the specified search string in the specified date range.

	Assumptions:
		The caller has administrative privileges or is a member of all communities

	Args:
		search_string (str, optional): The string to search for in the messages text. Defaults to None.
		start_date (str, optional): The earliest date to include in the results. Defaults to None.
		end_date (str, optional): The latest date to include in the results. Defaults to None.

	Returns:
		list: A list of messages that contain the specified search string in the specified date range. Each message being a dictionary mapping message column names to their corresponding data.
	"""
	# Default condition to accept all messages
	where_condition = "TRUE"
	args_dict = {}

	if search_string is not None:
		where_condition = "to_tsvector(messages.message) @@ to_tsquery(%(search_string)s)"

		search_tokens = search_string.split()
		search_string = " & ".join(search_tokens)
		args_dict["search_string"] = search_string

	if start_date is not None and end_date is not None:
		where_condition += " AND (messages.time_sent BETWEEN %(start_date)s AND %(end_date)s)"
		args_dict["start_date"] = start_date
		args_dict["end_date"] = end_date
	elif start_date is not None:
		where_condition += " AND (messages.time_sent >= %(start_date)s)"
		args_dict["start_date"] = start_date
	elif end_date is not None:
		where_condition += " AND (messages.time_sent <= %(end_date)s)"
		args_dict["end_date"] = end_date

	return db_utils.exec_get_all_rows(
		f"""
		SELECT messages.* FROM messages
			WHERE {where_condition}
		""",
		args_dict
	)

def get_messages_in_channel(channel_id):
	"""
	Retrieves all messages in the specified channel.

	Assumptions:
		The caller has administrative privileges or is a member of the sppecified channel

	Args:
		channel_id (int): The ID of the channel to retrieve messages from

	Returns:
		list: A list of messages in the specified channel. Each message being a dictionary mapping message column names to their corresponding data.
	"""
	return db_utils.exec_get_all_rows(
		"""
		SELECT messages.*, channel_msgs.channel_id FROM messages
				LEFT JOIN channel_messages channel_msgs ON messages.id = channel_msgs.id
				INNER JOIN channels ON
					channel_msgs.channel_id = channels.id AND
					channels.id = %(channel_id)s
		""",
		{"channel_id": channel_id}
	)

def get_messages_from_user(user_id, type=None, max_messages=None):
	"""
	Retrieves the given type of messages sent by the specified user

	Assumptions:
		The caller has administrative privileges or is the specified user

	Args:
		user_id (int): The ID of the user to retrieve messages from
		type (str, optional): The type of messages to retrieve. Defaults to None.
		max_messages (int, optional): The maximum number of messages to retrieve. Defaults to None.

	Returns:
		list: A list of messages sent by the specified user. Each message being a dictionary mapping message column names to their corresponding data.
	"""
	if type is not None and type not in ["direct", "channel", "all"]:
		raise RuntimeError("type must be either 'direct', 'channel', or 'all'")

	query_args = {
		"user_id": user_id
	}

	limit_clause = ""
	if max_messages is not None:
		if max_messages < 0:
			raise RuntimeError("max_messages must be greater than or equal to 0")

		query_args["max_messages"] = max_messages
		limit_clause = "LIMIT %(max_messages)s"

	direct_messages_query = f"""
		SELECT messages.*, direct_messages.receiver_user_id FROM messages
			INNER JOIN direct_messages ON messages.id = direct_messages.id
			WHERE messages.sender_user_id = %(user_id)s
			{limit_clause}
	"""

	channel_messages_query = f"""
		SELECT messages.*, channel_messages.channel_id FROM messages
			INNER JOIN channel_messages ON messages.id = channel_messages.id
			WHERE messages.sender_user_id = %(user_id)s
			{limit_clause}
	"""

	messages = []

	if type == "direct":
		messages = db_utils.exec_get_all_rows(
			direct_messages_query,
			query_args
		)
	elif type == "channel":
		messages = db_utils.exec_get_all_rows(
			channel_messages_query,
			query_args
		)
	else:
		messages = db_utils.exec_get_all_rows(
			f"""
				({direct_messages_query})
				UNION ALL
				({channel_messages_query})
				{limit_clause}
			""",
			query_args
		)

	return messages

def send_direct_message(sender_user_id, receiver_user_id, message):
	"""
	Sends a message from the specified sender to the specified receiver

	Assumptions:
		The caller has administrative privileges or is the specified sender

	Args:
		sender_user_id (int): The ID of the user who sent the message
		receiver_user_id (int): The ID of the user who receives the message
		message (str): The message to send

	Raises:
		Exception: If the specified sender or receiver does not exist

	Returns:
		dict: The sent message. A message being a dictionary mapping message column names to their corresponding data.
	"""
	message = db_utils.exec_commit_return_row(
		"""
			INSERT INTO messages (sender_user_id, message) VALUES
				(%(sender_user_id)s, %(message)s)
				RETURNING *
		""",
		{
			"sender_user_id": sender_user_id,
			"message": message
		}
	)

	direct_message = db_utils.exec_get_first_row(
		"""
			INSERT INTO direct_messages (id, receiver_user_id) VALUES
				(%(message_id)s, %(receiver_user_id)s)
			RETURNING *
		""",
		{
			"message_id": message["id"],
			"receiver_user_id": receiver_user_id
		}
	)

	message["receiver_user_id"] = direct_message["receiver_user_id"]

	return message