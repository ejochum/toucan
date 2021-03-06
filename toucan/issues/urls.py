from django.conf.urls import url, include
from django.conf import settings
from django.views.generic import TemplateView

from .views import HomeView, IssueList, IssueDetail, IssueCreateView, CommentCreateView, EditIssueView

app_name = 'issues'

urlpatterns = [
    url(r'^$', IssueList.as_view(), name='issue_list'),
    url(r'^create/$', IssueCreateView.as_view(), name='issue_create'),
    url(r'^(?P<issue_id>\d+)/', include([
        url(r'^$', IssueDetail.as_view(), name='issue_detail'),
        url(r'^edit/$', EditIssueView.as_view(), name='issue_edit'),
        url(r'^comment/$', CommentCreateView.as_view(), name='comment_create')
    ])),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^debug/', TemplateView.as_view(template_name='debug/editor.html'))
    ]