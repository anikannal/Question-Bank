from rest_framework import serializers
from .models import User, Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'is_completed', 'owner']
        read_only_fields = ['owner'] # Owner is set automatically

class UserSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'is_active', 'tasks']
