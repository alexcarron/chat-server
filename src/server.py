from flask import Flask
from flask_restful import Api
from apis import management_api, users_api, communities_api, channels_api, messages_api, login_api
from db_utils import chat_db_utils

flask_app = Flask(__name__)
main_api = Api(flask_app)

main_api.add_resource(management_api.InitEndpoint, "/manage/init")
main_api.add_resource(management_api.VersionEndpoint, "/manage/version")

main_api.add_resource(users_api.UsersEndpoint, "/users")
main_api.add_resource(users_api.UserIDEndpoint, "/users/<int:user_id>")
main_api.add_resource(users_api.UserMessagesEndpoint, "/users/<int:user_id>/messages")

main_api.add_resource(communities_api.CommunitiesEndpoint, "/communities")
main_api.add_resource(communities_api.CommunitiesIDEndpoint, "/communities/<int:community_id>")
main_api.add_resource(communities_api.CommunityChannelsEndpoint, "/communities/<int:community_id>/channels")

main_api.add_resource(channels_api.ChannelsEndpoint, "/channels")
main_api.add_resource(channels_api.ChannelsIDEndpoint, "/channels/<int:channel_id>")
main_api.add_resource(channels_api.ChannelMessagesEndpoint, "/channels/<int:channel_id>/messages")

main_api.add_resource(messages_api.MessagesEndpoint, "/messages")

main_api.add_resource(login_api.LoginEndpoint, "/login")
main_api.add_resource(login_api.LogoutEndpoint, "/logout")

if __name__ == "__main__":
	chat_db_utils.rebuild_tables()
	flask_app.run(debug=True)