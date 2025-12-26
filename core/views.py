from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Task
from .serializers import UserSerializer, TaskSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'])
    def tasks(self, request, pk=None):
        user = self.get_object()
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        # We override create to ensure tasks are created via the user endpoint or handle it here if owner_id is passed
        # However, the previous API laid out creating task for user.
        # Let's support creating task directly if owner_id is in body, otherwise rely on nested.
        # actually, standard DRF way is fine if owner is required.
        # But 'owner' field is read_only in serializer, so it must be passed via save().
        
        owner_id = request.data.get('owner_id')
        if owner_id:
             user = get_object_or_404(User, pk=owner_id)
             serializer = self.get_serializer(data=request.data)
             serializer.is_valid(raise_exception=True)
             self.perform_create(serializer, owner=user)
             headers = self.get_success_headers(serializer.data)
             return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer, owner=None):
        if owner:
            serializer.save(owner=owner)
        else:
            serializer.save()
