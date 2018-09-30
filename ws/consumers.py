import logging

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.conf import settings

from ws.dispatcher import Dispatcher

log = logging.getLogger('channels')


class WobSocketConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = Dispatcher(self)

    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        try:
            await super().receive(text_data, bytes_data, **kwargs)
        except Exception as e:
            if settings.DEBUG:
                raise e
            else:
                log.error(
                    f'Error in websocket!!!\n'
                    f'{e.__class__.__name__}: {e}\n'
                    f'Scope: {self.scope}\n'
                    f'Text data: {text_data}'
                )

    async def receive_json(self, content, **kwargs):
        await self.dispatcher.dispatch(content)

    async def disconnect(self, code):
        pass

    async def server_event(self, event):
        await self.send_json(event['message'])
