from channels.routing import route, route_class
from notifications.consumers import parse_mentions, send_comment_notification
from issues.consumers import SiteNotifications, ws_connect, ws_disconnect

channel_routing = [
    route("notifications.parse_mentions", parse_mentions),
    route("notifications.send_comment_notification", send_comment_notification),
    route("websocket.connect", ws_connect),
    route("websocket.disconnect", ws_disconnect),
    # route_class(SiteNotifications) # https://github.com/andrewgodwin/channels/issues/221
]
