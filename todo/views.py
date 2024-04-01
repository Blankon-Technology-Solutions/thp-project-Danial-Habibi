# todo/views.py

from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import TaskSerializer
from .models import Task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List' : '/task-list/',
        'Detail View' : '/task-detail/<str:pk>/',
        'Create' : '/task-create/',
        'Update' : '/task-update/<str:pk>/',
        'Delete' : '/task-delete/<str:pk>/',
    }
    return Response(api_urls)

@api_view(['GET'])
def taskList(request):
    tasks = Task.objects.filter(created_by=request.user)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def taskDetail(request, pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(task)
    return Response(serializer.data)

@api_view(['POST'])
def taskCreate(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        
        # Broadcast todo creation to all connected clients via WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            str(request.user.username),
            {
                'type': 'send_todo_update',
                'action': 'create',
                'task': serializer.data
            }
        )
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def taskUpdate(request, pk):
    try:
        task = Task.objects.get(id=pk, created_by=request.user)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(instance=task, data=request.data)
    if serializer.is_valid():
        serializer.save()
        
        # Broadcast todo update to all connected clients via WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            str(request.user.username),
            {
                'type': 'send_todo_update',
                'action': 'update',
                'task': serializer.data
            }
        )
        
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def taskDelete(request, pk):
    try:
        task = Task.objects.get(id=pk, created_by=request.user)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    task.delete()
    
    # Broadcast todo deletion to all connected clients via WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        str(request.user.username),
        {
            'type': 'send_todo_update',
            'action': 'delete',
            'task_id': pk
        }
    )
    
    return Response({'message': 'Task deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
