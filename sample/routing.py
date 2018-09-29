from channels.routing import ProtocolTypeRouter, URLRouter

import ws.routing
from sample.middleware import GeneralMiddleware

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': GeneralMiddleware(
        URLRouter(ws.routing.websocket_urlpatterns)
    ),
})
