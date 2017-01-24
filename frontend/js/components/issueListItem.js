import React, { PropTypes } from 'react'
import classNames from 'classnames'
import Icon from 'react-fa'

import Status from './status'
import {DateOnlyDisplay, DateOrTimeDisplay} from './date'
import getIconClassForIssueType from './icons/issueType'

function CommentCount({count}) {
    return (<span className={classNames({'text-muted': count === 0})}>
        <Icon name='comment-o' size='lg'/>
        { count === 0 ? count : <strong>{count}</strong>}
    </span>);
}

function Organisation ({organisation}) {
    return <span>{organisation.name}</span>;
}

function IssueTypes({types}) {
    let typeIcons = types.map((type) => <li key={type.slug}><Icon name={getIconClassForIssueType(type)} title={type.name} /></li>);
    return <ul className="issue-types">{typeIcons}</ul>;
}

class IssueListItem extends React.Component {

    render() {
        const {issue} = this.props;
        return <div className="issue-list-item"
                    onClick={(e) => {e.preventDefault;this.props.selectIssue(issue);}}
        >
            <h3>{issue.title}</h3>
            <Status status={issue.status} />
            {issue.organisation ? <Organisation organisation={issue.organisation} /> : null }
            <CommentCount count={issue.comment_count || 0}/>
            <IssueTypes types={issue.issue_types || []} />
            <DateOrTimeDisplay date={issue.created} />
        </div>;
    }
}

export default IssueListItem;
