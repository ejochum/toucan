from channels.generic.websockets import WebsocketConsumer


def resolve_site_channel(message):
    domain = message.content.get('server', ['default'])[0]

    from django.contrib.sites.models import Site
    try:
        site = Site.objects.select_related('siteconfig').get(domain=domain)
        return site.siteconfig.group_name
    except Site.DoesNotExist:
        pass

    return domain


class SiteNotifications(WebsocketConsumer):

    http_user = True

    def get_site(self):
        return resolve_site_channel(self.message)

    def connection_groups(self, **kwargs):
        groups = [
            self.get_site()
        ]

        if self.message.user.is_authenticated():
            groups.append('user:%d' % self.message.user.pk)

        return groups

