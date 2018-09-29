from django.urls import path

from .consumers import WobSocketConsumer

websocket_urlpatterns = [
    path('ws/', WobSocketConsumer),
]