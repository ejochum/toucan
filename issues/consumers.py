from channels import Group

from channels.generic.websockets import WebsocketConsumer
from channels.auth import channel_session_user_from_http, channel_session_user


def resolve_site_channel(message):
    domain = message.content.get('server', ['default'])[0]

    from django.contrib.sites.models import Site
    try:
        site = Site.objects.select_related('siteconfig').get(domain=domain)
        return site.siteconfig.group_name
    except Site.DoesNotExist:
        pass

    return domain



@channel_session_user_from_http
def ws_connect(message):

    site_channel = resolve_site_channel(message)
    channels = [
        site_channel
    ]
    # if user is authenticated add to personal notification group
    if message.user.is_authenticated():
        channels.append('user:%d' % message.user.pk)

    message.channel_session['groups'] = channels
    print('subscribing to ', channels)
    for group in channels:
        Group(group).add(message.reply_channel)


@channel_session_user
def ws_disconnect(message):
    for group_name in message.channel_session.get('groups', []):
        Group(group_name).discard(message.reply_channel)


class SiteNotifications(WebsocketConsumer):
    # this does not work due to user problems
    # see https://github.com/andrewgodwin/channels/issues/221

    def get_site(self):
        return self.message.content['server'][0]

    @channel_session_user
    def connection_groups(self, **kwargs):
        groups = [
            self.get_site()
        ]
        if self.message.user.is_authenticated():
            groups.append('user:%d' % self.message.user.pk)

        return groups

    @channel_session_user_from_http
    def connect(self, message, **kwargs):
        print(self.message.user)
        return super().connect(message, **kwargs)
