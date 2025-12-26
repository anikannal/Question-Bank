from pymongo import MongoClient
from django.conf import settings

# Global client
client = MongoClient('mongodb://localhost:27017/')
db = client['question_bank_db']
users_collection = db['users']
tasks_collection = db['tasks']
