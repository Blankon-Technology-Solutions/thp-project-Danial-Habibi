# todo/routing.py
from django.urls import path
from .consumers import TodoConsumer

websocket_urlpatterns = [
    path('ws/todo/', TodoConsumer.as_asgi()),
]
