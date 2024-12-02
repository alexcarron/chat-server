from flask_restful import Resource
from flask import jsonify
from auth_utils import hasher
from apis import request_data_utils, api_auth_utils
from db_utils import users_db_utils, messages_db_utils

class UsersEndpoint(Resource):
	def get(self):
		if api_auth_utils.is_valid_session() is False:
			return api_auth_utils.get_invalid_session_response()

		return jsonify(users_db_utils.get_users())

	def post(self):
		if api_auth_utils.is_valid_session() is False:
			return api_auth_utils.get_invalid_session_response()

		body = request_data_utils.get_json_body()
		username = body.get('username')
		password = body.get('password')
		email = body.get('email')

		if (username is None) or (password is None):
			return {'message': 'Missing username or password'}, 400

		hashed_password = hasher.hash_string(password)

		try:
			user = users_db_utils.add_user(username, hashed_password, email)
			return jsonify(user)
		except Exception:
			return {'message': 'Username or email already exists'}, 400

class UserIDEndpoint(Resource):
	def get(self, user_id):
		if api_auth_utils.is_valid_session() is False:
			return api_auth_utils.get_invalid_session_response()

		return jsonify(users_db_utils.get_user(user_id))

	def put(self, user_id):
		if api_auth_utils.is_valid_session() is False:
			return api_auth_utils.get_invalid_session_response()

		body = request_data_utils.get_json_body()
		username = body.get('username')
		password = body.get('password')
		email = body.get('email')

		hashed_password = None

		if password is not None:
			hashed_password = hasher.hash_string(password)

		try:
			updated_user = users_db_utils.update_user(
				user_id,
				username=username,
				hashed_password=hashed_password,
				email=email
			)

			if updated_user is None:
				return {'message': 'User not found'}, 404

			return jsonify(updated_user)
		except RuntimeError as runtime_error:
			return {'message': str(runtime_error)}, 400
		except Exception:
			return {'message': 'Username or email already exists'}, 400

	def delete(self, user_id):
		if api_auth_utils.is_valid_session() is False:
			return api_auth_utils.get_invalid_session_response()

		deleted_user = users_db_utils.delete_user(user_id)

		if deleted_user is not None:
			return jsonify(deleted_user)
		else:
			return {'message': 'User not found'}, 404

class UserMessagesEndpoint(Resource):
	def get(self, user_id):
		if api_auth_utils.is_valid_session() is False:
			return api_auth_utils.get_invalid_session_response()

		query_args = request_data_utils.get_query_args_dict()
		msg_type = query_args.get('type')
		max_messages = query_args.get('max_messages')

		try:
			if max_messages is not None:
				max_messages = int(max_messages)

			messages = messages_db_utils.get_messages_from_user(
				user_id,
				type=msg_type,
				max_messages=max_messages
			)
		except RuntimeError as runtime_error:
			return {'message': str(runtime_error)}, 400
		except TypeError:
			return {'message': 'max_messages must be an integer'}, 400
		except ValueError:
			return {'message': 'max_messages must be an integer'}, 400

		return jsonify(messages)