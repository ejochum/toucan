import uwsgi
from daphne.server import Server
from channels import DEFAULT_CHANNEL_LAYER, channel_layers

import django
django.setup()

# get the channel layer
channel_layer = channel_layers[DEFAULT_CHANNEL_LAYER]


uwsgi.accepting()

# spawn a handler for every uWSGI socket
for fd in uwsgi.sockets[:1]:
    try:
        s = Server(
            channel_layer=channel_layer,
            file_descriptor=fd,
            http_timeout=60,
            signal_handlers=True
        ).run()
    except KeyboardInterrupt:
        pass

