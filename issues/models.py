from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from model_utils import Choices
from model_utils.models import TimeStampedModel

from ttp import ttp

from .utils import parse_draft_struct, draft_struct_to_comment


TwitterParser = ttp.Parser()

ISSUE_STATUS_CHOICES = Choices(
    ('open', _('open')),
    ('closed', _('closed'))
)

class IssueType(TimeStampedModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    svg_icon = models.FileField(blank=True, upload_to='markers')

    def __str__(self):
        return self.name


class Issue(TimeStampedModel):

    PRIORITY_CHOICES = Choices(
        (0, 'low', _('low')),
        (1, 'normal', _('normal')),
        (2, 'high', _('high')),
        (3, 'alarm', _('alarm'))
    )

    VISIBILITY_CHOICES = Choices(
        (0, 'private', _('private')),
        (1, 'members', _('all organisation members')),
        (2, 'users', _('all registered users')),
        (3, 'public', _('public')),
    )

    STATUS_CHOICES = ISSUE_STATUS_CHOICES

    title = models.CharField(
        max_length=300,
        verbose_name=_('issue title')
    )

    description = models.TextField(blank=False)

    FORMAT_CHOICES = Choices(
        ('', _('Just text')),
        ('markdown', _('Markdown')),
        ('html', _('HTML'))
    )
    description_format = models.CharField(blank=True, choices=FORMAT_CHOICES, default='', max_length=20)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    point = models.PointField(verbose_name=_('location'), null=True)
    # location = models.ForeignKey('organisations.Location', null=True, verbose_name='location')

    organisation = models.ForeignKey(
        'organisations.Organisation',
        null=True, blank=False,
        default='',
        verbose_name=_('organisation')
    )

    issue_type = models.ForeignKey(
        IssueType,
        null=True,
        blank=False,
        default=1,
        on_delete=models.SET_NULL,
        verbose_name=_('issue type')
    )

    priority = models.SmallIntegerField(choices=PRIORITY_CHOICES, default=1)
    visibility = models.SmallIntegerField(choices=VISIBILITY_CHOICES, default=3)

    current_status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=10,
        db_index=True,
        default='open',
        verbose_name=_('issue status')
    )

    site = models.ForeignKey(
        Site,
        default=1
    )

    def update_status(self):
        status = self.status
        if self.current_status != status:
            self.current_status = status
            self.save()

    @property
    def users(self):
        '''Get a list of all involved users'''
        User = get_user_model()
        return User.objects.all()

    @property
    def status(self):
        try:
            return self.status_changes.latest().status
        except IssueStatus.DoesNotExist:
            return 'open'

    def get_absolute_url(self):
        url = reverse('home_issue', kwargs={'issue_id': self.pk})
        return 'https://%s%s' % (self.site.domain, url)

    @property
    def gis_location(self):
        return self.point

    class Meta:
        verbose_name = _('issue')
        verbose_name_plural = _('issues')
        ordering = ('-created',)
        get_latest_by = 'created'

    def __str__(self):
        return self.title


class AbstractIssueRelatedModel(TimeStampedModel):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        abstract = True
        ordering = ('created',)


class IssueComment(AbstractIssueRelatedModel):

    issue = models.ForeignKey(Issue, related_name='comments')
    comment = models.TextField(blank=False, verbose_name=_('comment'))

    draft_struct = JSONField(default=dict, blank=True)

    def get_mentions(self):
        text = self.get_comment()
        results = TwitterParser.parse(text)
        return results.users

    def get_comment(self):
        if self.comment:
            return self.comment
        else:
            return draft_struct_to_comment(self.draft_struct)

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        get_latest_by = 'created'

    def __str__(self):
        return 'Comment by user %s on issue #%d' % (self.user.username, self.issue_id)


class IssueStatus(AbstractIssueRelatedModel):

    issue = models.ForeignKey(Issue, related_name='status_changes')

    STATUS_CHOICES = ISSUE_STATUS_CHOICES

    status = models.CharField(max_length=10, db_index=True, choices=STATUS_CHOICES)

    class Meta:
        verbose_name = _('issue status')
        verbose_name_plural = _('issue statuses')
        get_latest_by = 'created'
