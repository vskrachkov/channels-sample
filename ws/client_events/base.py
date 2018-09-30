from ws.dispatcher import register_handler


class ClientEventMeta(type):
    @classmethod
    def __new__(mcs, *args, **kwargs):
        metaclass, name, bases, attrs = args
        cls = super().__new__(mcs, name, bases, attrs)
        event_type = getattr(cls, 'event_type', None)
        if event_type: register_handler(event_type)(cls)
        return cls


class BaseClientEvent(metaclass=ClientEventMeta):
    event_type = None

    def __init__(self, consumer):
        self.consumer = consumer

    async def handle(self, content):
        await self.receive(content)

    async def receive(self, content):
        raise NotImplementedError()
