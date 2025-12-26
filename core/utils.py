from pymongo import MongoClient
from django.conf import settings

# Global client
config = settings.MONGODB_CONFIG
client = MongoClient(
    host=config['host'],
    port=config['port'],
    serverSelectionTimeoutMS=config['timeout']
)
db = client[config['db_name']]
users_collection = db['users']
tasks_collection = db['tasks']
