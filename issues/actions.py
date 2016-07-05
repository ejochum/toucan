
import json

def issue_updated(issue):
    sc = issue.site.siteconfig
    print('sending issue update')
    print(sc.group_name)
    sc.group.send({
        'text': json.dumps({'action': 'ISSUE_UPDATED'})
    })

