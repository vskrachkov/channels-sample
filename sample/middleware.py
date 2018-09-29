from channels.middleware import BaseMiddleware


class GeneralMiddleware(BaseMiddleware):
    def populate_scope(self, scope):
        pass

    async def resolve_scope(self, scope):
        pass
