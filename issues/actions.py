
import json
from api.serializers import IssueSerializer

def issue_updated(issue):

    sc = issue.site.siteconfig

    sc.group.send({
        'text': json.dumps({
            'type': 'INVALIDATE_ISSUE',
            'issue_id': issue.pk,
            'payload': IssueSerializer(issue).data
        })
    })

