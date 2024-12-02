from flask_restful import Resource
from db_utils import users_db_utils
from auth_utils import hasher, session_key_utils
from apis import api_auth_utils, request_data_utils

class LoginEndpoint(Resource):
	def post(self):
		username = request_data_utils.get_json_body_property('username')
		password = request_data_utils.get_json_body_property('password')
		hashed_password = hasher.hash_string(password)

		user_id = users_db_utils.get_id_of_login(username, hashed_password)

		if user_id is None:
			return {"message": "Invalid username or password"}, 401

		session_key = session_key_utils.generate_session_key()
		users_db_utils.start_new_user_session(user_id, session_key)

		return {"session_key": session_key, "message": "Logged in successfully"}, 200


class LogoutEndpoint(Resource):
	def post(self):
		if api_auth_utils.is_valid_session() is False:
			return api_auth_utils.get_invalid_session_response()

		user_id = api_auth_utils.get_user_id_of_requester()

		users_db_utils.end_user_session(user_id)

		return {"message": "Logged out successfully"}, 200