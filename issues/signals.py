from .models import IssueStatus, IssueComment, Issue
from django.db.models.signals import post_save

from .actions import issue_updated

def set_issue_status(**kwargs):
    issue_status = kwargs['instance']
    issue = issue_status.issue
    issue.update_status()


post_save.connect(set_issue_status, sender=IssueStatus)


def comment_posted(**kwargs):
    comment = kwargs['instance']
    issue_updated(comment.issue)

post_save.connect(comment_posted, sender=IssueComment)


def issue_crud(**kwargs):
    issue = kwargs['instance']
    issue_updated(issue)

post_save.connect(issue_crud, sender=Issue)
