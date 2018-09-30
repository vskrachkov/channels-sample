from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class BaseWorkstationEvent:
    def __init__(self, workstation_mac):
        self.workstation_mac = workstation_mac.lower().replace(':', '-')
        self.channel_layer = get_channel_layer()

    def _send(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.workstation_mac,
            {
                'type': 'workstation',
                'message': message
            }
        )

    def send(self, *args, **kwargs):
        raise NotImplementedError()


class PowerOff(BaseWorkstationEvent):
    def send(self, *args, **kwargs):
        self._send({
            'type': 'workstation.power_off'
        })
