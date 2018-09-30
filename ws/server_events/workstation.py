from ws.server_events.base import BaseServerEvent


class BaseWorkstationEvent(BaseServerEvent):
    def __init__(self, workstation_mac):
        self.workstation_mac = workstation_mac.lower().replace(':', '-')

    def get_group_name(self):
        return self.workstation_mac

    def send(self, *args, **kwargs):
        raise NotImplementedError()


class PowerOff(BaseWorkstationEvent):
    def send(self, *args, **kwargs):
        self._send({
            'type': 'workstation.power_off'
        })


class Lock(BaseWorkstationEvent):
    def send(self, *args, **kwargs):
        self._send({
            'type': 'workstation.lock'
        })
