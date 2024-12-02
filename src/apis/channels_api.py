import json
from flask_restful import Resource
from apis import api_auth_utils
from flask import jsonify

from db_utils import channels_db_utils, messages_db_utils

class ChannelsEndpoint(Resource):
	def get(self):
		if api_auth_utils.is_valid_session() is False:
			return api_auth_utils.get_invalid_session_response()

		return channels_db_utils.get_channels()

class ChannelsIDEndpoint(Resource):
	def get(self, channel_id):
		if api_auth_utils.is_valid_session() is False:
			return api_auth_utils.get_invalid_session_response()

		channel = channels_db_utils.get_channel(channel_id)
		return channel

class ChannelMessagesEndpoint(Resource):
	def get(self, channel_id):
		if api_auth_utils.is_valid_session() is False:
			return api_auth_utils.get_invalid_session_response()

		messages = messages_db_utils.get_messages_in_channel(channel_id)
		return jsonify(messages)