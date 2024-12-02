from flask_restful import Resource
from apis import api_auth_utils
from db_utils import communities_db_utils, channels_db_utils

class CommunitiesEndpoint(Resource):
	def get(self):
		return communities_db_utils.get_communities()

class CommunitiesIDEndpoint(Resource):
	def get(self, community_id):
		community = communities_db_utils.get_community(community_id)
		return community

class CommunityChannelsEndpoint(Resource):
	def get(self, community_id):
		if api_auth_utils.is_valid_session() is False:
			return api_auth_utils.get_invalid_session_response()

		channels = channels_db_utils.get_channels_in_community(community_id)
		return channels
