import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "issue_tracker.settings")

from channels.asgi import get_channel_layer

channel_layer = get_channel_layer()
