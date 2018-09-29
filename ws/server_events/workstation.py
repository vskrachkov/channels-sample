from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class BaseWorkstationEvent:
    event_type = None

    def __init__(self, workstation_mac):
        self.workstation_mac = workstation_mac.lower().replace(':', '-')
        self.channel_layer = get_channel_layer()

    def _send(self, *args, **kwargs):
        return async_to_sync(self.channel_layer.group_send)(*args, **kwargs)

    def send(self, *args, **kwargs):
        self._send(
            self.workstation_mac,
            {
                'type': self.event_type,
                'args': args,
                'kwargs': kwargs
            }
        )


class PowerOff(BaseWorkstationEvent):
    event_type = 'workstation.power_off'
