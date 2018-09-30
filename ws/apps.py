from django.apps import AppConfig


class WsConfig(AppConfig):
    name = 'ws'

    def ready(self):
        from .client_events import base
