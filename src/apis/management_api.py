from flask_restful import Resource

from db_utils  import chat_db_utils
from db_utils import swen344_db_utils as db_utils

class InitEndpoint(Resource):
	def post(self):
		chat_db_utils.rebuild_tables()

class VersionEndpoint(Resource):
	def get(self):
		return (db_utils.exec_get_first_row('SELECT VERSION()'))