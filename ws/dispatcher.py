import logging

log = logging.getLogger('channels')


class Dispatcher:
    handlers_map = {}

    @classmethod
    def register_handler(cls, event_type):
        def wrapper(handler):
            cls.handlers_map[event_type] = handler
            return handler
        return wrapper

    def __init__(self, consumer):
        self.consumer = consumer

    async def dispatch(self, content):
        event_type = content.get('type')
        assert event_type, '`type` is required'

        Handler = self.handlers_map.get(event_type)

        if Handler:
            handler = Handler(self.consumer)
            await handler.handle(content)
        else:
            log.info(f'unknown event : {content}')


register_handler = Dispatcher.register_handler
