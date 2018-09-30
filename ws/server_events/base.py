from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()


class BaseServerEvent:
    def get_group_name(self):
        raise NotImplementedError()

    def _send(self, message):
        async_to_sync(channel_layer.group_send)(
            self.get_group_name(),
            {
                'type': 'server_event',
                'message': message
            }
        )

    def send(self, *args, **kwargs):
        raise NotImplementedError()
