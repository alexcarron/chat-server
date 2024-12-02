from . import swen344_db_utils as db_utils
import datetime

def get_user(user_id):
	"""
	Retrieves a user from the database by ID.

	Assumptions:
		The caller has administrative privileges.

	Args:
		user_id (int): The ID of the user to retrieve.

	Returns:
		dict: The retrieved user. A user being a dictionary mapping user column names to their corresponding data.
	"""
	return db_utils.exec_get_first_row(
		"SELECT * FROM users WHERE id = %(user_id)s",
		{"user_id": user_id}
	)

def get_users():
	"""
	Retrieves all users from the database.

	Assumptions:
		The caller has administrative privileges.

	Returns:
		list: A list of users. Each user being a dictionary mapping user column names to their corresponding data.
	"""
	return db_utils.exec_get_all_rows("SELECT * FROM users")

def add_user(username, hashed_password, email=None):
	"""
	Adds a new user to the database.

	Args:
		username (str): The username of the new user.
		hashed_password (str): The hashed password of the new user.
		email (str, optional): The email of the new user. Defaults to `None`.

	Raises:
		Exception: If the username or email already exists in the database.

	Returns:
		dict: The created user. A user being a dictionary mapping user column names to their corresponding data.
	"""
	created_user = None

	if email is None:
		created_user = db_utils.exec_commit_return_row(
			"""
				INSERT INTO users(username, password)
					VALUES(%(username)s, %(password)s)
					RETURNING *
			""",
			{'username': username, 'password': hashed_password}
		)
	else:
		created_user = db_utils.exec_commit_return_row(
			"""
				INSERT INTO users(username, password, email)
					VALUES(%(username)s, %(password)s, %(email)s)
					RETURNING *
			""",
			{'username': username, 'password': hashed_password, 'email': email}
		)

	return created_user

def update_user(user_id, username=None, hashed_password=None, email=None):
	"""
	Updates a user in the database.

	Args:
		user_id (int): The ID of the user to update.
		username (str, optional): The new username. Defaults to `None`.
		password (str, optional): The new password. Defaults to `None`.
		email (str, optional): The new email. Defaults to `None`.

	Raises:
		Exception: If the username or email already exists in the database.
		RuntimeError: If the user has changed their username in the last 6 months.

	Returns:
		dict: The updated user. A user being a dictionary mapping user column names to their corresponding data. If the user does not exist, `None` is returned.
	"""
	timestamp = get_now_timestamp()
	can_change_username = can_user_change_username(user_id, timestamp)

	if not can_change_username and username is not None:
		raise RuntimeError('Cannot change username because user has changed username in last 6 months')

	updated_user = db_utils.exec_commit_return_row(
		"""
			UPDATE users
				SET
					username = COALESCE(%(username)s, username),
					password = COALESCE(%(password)s, password),
					email = COALESCE(%(email)s, email)
				WHERE
					id = %(user_id)s
				RETURNING *
		""",
		{
			'user_id': user_id,
			'username': username,
			'password': hashed_password,
			'email': email
		}
	)

	if username is not None:
		updated_user = db_utils.exec_commit_return_row(
			"""
				UPDATE users
					SET last_username_change_time = %(timestamp)s
					WHERE id = %(user_id)s
					RETURNING *
			""",
			{
				'user_id': user_id,
				'timestamp': timestamp
			}
		)

	return updated_user

def delete_user(user_id):
	"""
	Deletes a user from the database.

	Assumptions:
		The caller has administrative privileges.

	Args:
		user_id (int): The ID of the user to delete.

	Returns:
		dict: The deleted user. A user being a dictionary mapping user column names to their corresponding data. If the user does not exist, `None` is returned.
	"""
	deleted_user = db_utils.exec_commit_return_row(
		"""
			DELETE FROM users
				WHERE id = %(user_id)s
				RETURNING *
		""",
		{'user_id': user_id}
	)

	return deleted_user


def get_now_timestamp():
	"""
	Retrieves the current timestamp in the format 'YYYY-MM-DD HH:MM:SS'.

	Returns:
		str: The current timestamp in the format 'YYYY-MM-DD HH:MM:SS'.
	"""
	return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def can_user_change_username(user_id, timestamp=None):
	"""
	Checks if a user can change their username.

	Args:
		user_id (int): The ID of the user to check.
		timestamp (str, optional): The time the username change was made in the format 'YYYY-MM-DD HH:MM:SS'. Defaults to None.

	Returns:
		bool: True if the user can change their username, False otherwise.
	"""
	if (timestamp is None):
		timestamp = get_now_timestamp()

	time_changing_username = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

	last_username_change_time = db_utils.exec_get_first_value(
		"""
			SELECT last_username_change_time FROM users
				WHERE id = %(user_id)s
		""",
		{"user_id": user_id}
	)

	if (last_username_change_time is None):
		return True

	six_months_after_last_change = last_username_change_time + datetime.timedelta(days=180)

	if (time_changing_username > six_months_after_last_change):
		return True

	return False

def get_id_of_login(username, hashed_password):
	"""
	Retrieves the ID of the user with the specified username and hashed password.

	Args:
		username (str): The username to check.
		hashed_password (str): The hashed password to check.

	Returns:
		int: The ID of the user with the specified username and hashed password, or `None` if no such user exists.
	"""
	user_id = db_utils.exec_get_first_value(
		"""
		SELECT id FROM users
			WHERE
				username = %(username)s AND
				password = %(password)s
		""",
		{"username": username, "password": hashed_password}
	)

	return user_id

def start_new_user_session(user_id, session_key):
	"""
	Starts the user session by setting the session key in the database.

	Args:
		user_id (int): The ID of the user to start the session for.
		session_key (str): The session key to set.

	Return:
		bool: `True` if the session was started successfully, `False` otherwise.
	"""
	user_updated = db_utils.exec_commit_return_row(
		"""
		UPDATE users
			SET session_key = %(session_key)s
			WHERE id = %(user_id)s
			RETURNING *
		""",
		{'user_id': user_id, 'session_key': session_key}
	)

	return user_updated is not None

def end_user_session(user_id):
	"""
	Ends the user session by removing their sessoin key

	Args:
		user_id (int): The ID of the user whose session is to be ended.

	Returns:
		bool: `True` if the user had a session key and the session was ended successfully, `False` otherwise.
	"""
	user_updated = db_utils.exec_commit_return_row(
		"""
		UPDATE users
			SET session_key = NULL
			WHERE
				id = %(user_id)s AND
				session_key IS NOT NULL
			RETURNING *
		""",
		{'user_id': user_id}
	)

	return user_updated is not None

def get_user_id_of_session_key(session_key):
	"""
	Retrieves the ID of the user with the specified session key if the session key is valid.

	Args:
		session_key (str): The session key associated with the user.

	Returns:
		int: The ID of the user with the specified session key, or `None` if the session key is invalid.
	"""
	user_id_with_session_key = db_utils.exec_get_first_value(
		"""
		SELECT id FROM users
			WHERE
				session_key = %(session_key)s
		""",
		{'session_key': session_key}
	)

	return user_id_with_session_key