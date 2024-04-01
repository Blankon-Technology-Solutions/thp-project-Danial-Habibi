import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Task
from .serializers import TaskSerializer
from .auth_backend import TokenAuthBackend
from asgiref.sync import sync_to_async

class TodoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract authentication token from query parameters
        token = self.scope['query_string'].decode().split('=')[1]
        
        # Authenticate user based on token
        user = await TokenAuthBackend().authenticate(request=None, token=token)
        
        # Check if user is authenticated
        if user is not None and user.is_authenticated:
            # Accept the WebSocket connection
            await self.accept()
            print(user.username)
            # Add the connection to a group or perform any other actions
            await self.channel_layer.group_add(
                str(user.username),  # Convert username to string
                self.channel_name
            )
        else:
            # Reject the connection
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self.scope['user'], 'username') and self.scope['user'].username:
            await self.channel_layer.group_discard(
                self.scope['user'].username,
                self.channel_name
            )

    async def receive(self, text_data):
        token = self.scope['query_string'].decode().split('=')[1]
        
        # Authenticate user based on token
        user = await TokenAuthBackend().authenticate(request=None, token=token)
 
        if user:
            text_data_json = json.loads(text_data)
            action = text_data_json['action']
            task_data = text_data_json.get('task')
            if action == 'sync':
                tasks = await sync_to_async(Task.objects.filter)(created_by=user.id)
                serializer = TaskSerializer(tasks, many=True)
                serializer_data = await sync_to_async(serializer.data.__getitem__)(slice(None))
                await self.send(text_data=json.dumps({
                    'action': 'sync',
                    'tasks': serializer_data
                }))

            elif action == 'add':
                if task_data:
                    task_data['created_by'] = user.id
                    serializer = TaskSerializer(data=task_data)
                    if serializer.is_valid():
                        serializer.save()
                        await self.channel_layer.group_send(
                            str(self.scope['user'].username),
                            {
                                'type': 'send_todo_update',
                                'action': 'add',
                                'task': serializer.data
                            }
                        )

            elif action == 'update':
                if task_data:
                    task = await sync_to_async(Task.objects.get)(id=task_data['id'])
                    serializer = TaskSerializer(instance=task, data=task_data)
                    if serializer.is_valid():
                        serializer.save()
                        await self.channel_layer.group_send(
                            str(self.scope['user'].username),
                            {
                                'type': 'send_todo_update',
                                'action': 'update',
                                'task': serializer.data
                            }
                        )

            elif action == 'delete':
                task_id = text_data_json.get('task_id')
                if task_id:
                    task = await sync_to_async(Task.objects.get)(id=task_id)
                    task.delete()
                    await self.channel_layer.group_send(
                        str(self.scope['user'].username),
                        {
                            'type': 'send_todo_update',
                            'action': 'delete',
                            'task_id': task_id
                        }
                    )
        else:
            # User is not authenticated, handle accordingly
            print("User is not authenticated")

    async def send_todo_update(self, event):
        await self.send(text_data=json.dumps(event))
