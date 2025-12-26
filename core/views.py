from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import users_collection, tasks_collection
from bson import ObjectId

def serialize_doc(doc):
    doc['id'] = str(doc.pop('_id'))
    return doc

class UserList(APIView):
    def get(self, request):
        users = list(users_collection.find())
        return Response([serialize_doc(u) for u in users])

    def post(self, request):
        data = request.data
        if users_collection.find_one({"email": data.get("email")}):
             return Response({"detail": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Simple validation
        user = {
            "email": data.get("email"),
            "is_active": data.get("is_active", True)
        }
        result = users_collection.insert_one(user)
        user['_id'] = result.inserted_id
        return Response(serialize_doc(user), status=status.HTTP_201_CREATED)

class TaskList(APIView):
    def get(self, request):
        # Handle query params for Task 3 here if needed, or let candidate do it
        owner_id = request.query_params.get('owner_id')
        filter_query = {}
        if owner_id:
            filter_query['owner_id'] = owner_id
            
        tasks = list(tasks_collection.find(filter_query))
        serialized_tasks = []
        for t in tasks:
            # Join owner info manually if needed, or just return ID
            serialized_tasks.append(serialize_doc(t))
        return Response(serialized_tasks)

    def post(self, request):
        data = request.data
        task = {
            "title": data.get("title"),
            "description": data.get("description", ""),
            "is_completed": data.get("is_completed", False),
            "owner_id": data.get("owner_id"), # Storing as string or whatever passed
            # Task 1: Priority field placeholder
        }
        if data.get("priority"):
             task["priority"] = data.get("priority")

        result = tasks_collection.insert_one(task)
        task['_id'] = result.inserted_id
        return Response(serialize_doc(task), status=status.HTTP_201_CREATED)

class TaskDetail(APIView):
    def put(self, request, pk):
        data = request.data
        update_data = {
            "title": data.get("title"),
            "is_completed": data.get("is_completed"),
        }
        if "priority" in data:
             update_data["priority"] = data["priority"]
             
        # Remove None values
        update_data = {k: v for k, v in update_data.items() if v is not None}
        
        result = tasks_collection.update_one(
            {"_id": ObjectId(pk)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        updated_task = tasks_collection.find_one({"_id": ObjectId(pk)})
        return Response(serialize_doc(updated_task))
