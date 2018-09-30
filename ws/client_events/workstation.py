from .base import BaseClientEvent


class BaseWorkstationClientEvent(BaseClientEvent):
    async def receive(self, content):
        raise NotImplementedError()


class RegisterConn(BaseWorkstationClientEvent):
    event_type = 'workstation.reg_conn'

    async def receive(self, content):
        workstation_mac = content.get('mac')
        if not workstation_mac:
            await self.consumer.close(); return

        await self.consumer.channel_layer.group_add(
            workstation_mac.replace(':', '-'),
            self.consumer.channel_name
        )
