import logging

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.conf import settings

log = logging.getLogger('channels')


class WobSocketConsumer(AsyncJsonWebsocketConsumer):
    # region WebSocket communication methods

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
        event_type = content.get('type')
        assert event_type, '`type` is required'
        assert not event_type.startswith('_'), \
            '`type` cannot starts with underscore'

        event_type = event_type.replace('.', '_')
        handler_name = f'on_{event_type}'
        handler = getattr(self, handler_name, None)

        if handler:
            await handler(content)
        else:
            await self.unknown_event_type(content)

    async def disconnect(self, code):
        pass

    # endregion

    # region Common events

    @staticmethod
    async def unknown_event_type(content):
        log.info(f'Unknown event: {content}')

    # endregion

    # region Workstation websocket events handlers

    async def on_workstation_reg_conn(self, content):
        workstation_mac = content.get('mac')
        if not workstation_mac:
            await self.close(); return

        await self.channel_layer.group_add(
            workstation_mac.replace(':', '-'),
            self.channel_name
        )

    # endregion

    # region Workstation server events handlers

    async def workstation_power_off(self, event):
        await self.send_json({'type': 'power_off'})

    # endregion
