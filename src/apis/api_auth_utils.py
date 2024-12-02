from flask_restful import request
from db_utils import users_db_utils


def get_session_token_in_header():
	"""
	Retrieves the session token passed in the Authorization header of the request.

	Returns:
		str: The session token passed in the Authorization header, or `None` if no session token was passed.
	"""
	session_token = request.headers.get('Authorization')
	return session_token

def is_valid_session():
	"""
	Checks if the session token passed in the Authorization header is valid.

	Returns:
		bool: `True` if the session token is valid, `False` otherwise.
	"""
	session_token = get_session_token_in_header()
	user_id = users_db_utils.get_user_id_of_session_key(session_token)
	return user_id is not None

def get_user_id_of_requester():
	"""
	Retrieves the user ID of the user making the request based on the user associated with the session token passed in the Authorization header.

	Returns:
		int: The ID of the user, or `None` if the user is not authenticated.
	"""
	session_token = get_session_token_in_header()
	user_id = users_db_utils.get_user_id_of_session_key(session_token)
	return user_id

def get_invalid_session_response():
	"""
	Returns an invalid session response.

	Returns:
		tuple: A tuple containing the invalid session response and the status code.
	"""
	return {"message": "Invalid session token"}, 401