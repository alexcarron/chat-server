from flask_restful import Resource
from flask import request, jsonify
from apis import request_data_utils, api_auth_utils
import json

from db_utils import messages_db_utils

class MessagesEndpoint(Resource):
	def get(self):
		if api_auth_utils.is_valid_session() is False:
			return api_auth_utils.get_invalid_session_response()
		
		query_args = request_data_utils.get_query_args_dict()
		search_query = query_args.get('search_query')
		start_date = query_args.get('start_date')
		end_date = query_args.get('end_date')

		messages = messages_db_utils.search_messages(search_string=search_query, start_date=start_date, end_date=end_date)

		return jsonify(messages)

	def post(self):
		if api_auth_utils.is_valid_session() is False:
			return api_auth_utils.get_invalid_session_response()

		user_id = api_auth_utils.get_user_id_of_requester()
		query_args = request_data_utils.get_query_args_dict()
		msg_type = query_args.get('type')

		if (msg_type != 'direct'):
			return {'message': f'message type {msg_type} not supported'}, 400

		message = request_data_utils.get_json_body_property('message')
		reciever_user_id = request_data_utils.get_json_body_property('reciever_user_id')

		if message is None:
			return {'message': 'message must be provided in body'}, 400
		elif reciever_user_id is None:
			return {'message': 'reciever_user_id must be provided in body'}, 400

		message = messages_db_utils.send_direct_message(
			user_id, reciever_user_id, message
		)

		return jsonify(message)