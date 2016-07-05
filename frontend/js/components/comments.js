import React, {PropTypes} from 'react'
import Timeago from 'react-timeago'
import Icon from 'react-fa'
import CommentEditor from '../containers/commentEditor'
import DraftEditor, { convertToRaw, convertFromRaw, EditorState, ContentState } from 'draft-js'
import concat from 'lodash/concat'
import isEmpty from 'lodash/isEmpty'
import { fromJS } from 'immutable'
import CommentView from './commentView'
import UserLink from './userLink'


export class CommentForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = this._getInitialState()
    this.handleSubmit = this.handleSubmit.bind(this)
    this.handleEditorStateChange = this.handleEditorStateChange.bind(this)
    this.handleStatusChangeAndSubmit = this.handleStatusChangeAndSubmit.bind(this)
  }

  _getInitialState() {
    return {
      editorState: CommentEditor.getEmptyEditorState(),
      toggleState: false
    }
  }

  resetEditorState() {
    let editorState = EditorState.push(
      this.state.editorState,
      ContentState.createFromText('')
    );
    this.setState({
      editorState
    })
  }

  handleSubmit(e) {
    e.preventDefault();
    this.postComment();
  }

  postComment() {
    let comment = {
      id: Date.now(),
      draft_struct: convertToRaw(this.state.editorState.getCurrentContent()),
      user: {
        username: 'You'
      },
      toggleState: this.state.toggleState
    }
    this.props.onComment(comment);
    this.resetEditorState();
  }

  handleEditorStateChange(state) {
    this.setState({
      editorState: state
    })
  }

  handleStatusChangeAndSubmit(e) {
    this.setState({
        toggleState: true
      },
      () => {
        this.postComment()
      }
    );
  }

  render() {
    return (<div className='commentForm'>
      <form onSubmit={this.handleSubmit} ref={(e) => this._form =e }>
        <CommentEditor onStateChange={this.handleEditorStateChange}
                       mention_suggestions={this.props.users}
                       editorState={this.state.editorState} />

        <div className='btn-toolbar pull-right'>
           <button className='btn btn-sm btn-default' type='button' onClick={this.handleStatusChangeAndSubmit}>
             { this.props.status == 'open' ? 'Close' : 'Reopen issue' }
           </button>
           <button className='btn btn-sm btn-success' type='submit'>
             Comment
           </button>
        </div>

      </form>
    </div>);
  }
}

CommentForm.propTypes = {
  onComment: PropTypes.func.isRequired,
  status: PropTypes.string.isRequired,
  users: PropTypes.array.isRequired
}

export class Comment extends React.Component {
  render() {
    let c = this.props.comment;
    return (<div className='panel panel-default'>
      <div className='panel-heading'>
        <UserLink username={c.user.username} /> commented <Timeago date={c.created} />
      </div>
      <div className="panel-body" style={{whiteSpace: 'pre-line'}}>
        {c.comment === '' ? <em>No comment was added.</em> : <CommentView comment={c.comment} /> }
      </div>
    </div>);
  }
}

Comment.propTypes = {
  comment: PropTypes.object.isRequired
}


export class StatusChange extends React.Component {
  render() {
    let sc = this.props.statusChange;
    return <p className='text-right text-muted'>
      <a>{sc.user.username}</a>&nbsp;
      { sc.status === 'open' ? <span className='label label-success'>re-opened</span> : null }
      { sc.status === 'closed' ? <span className='label label-danger'>closed</span> : null }
      &nbsp;this issue.
    </p>;
  }
}

export class CommentList extends React.Component {

  flattenCommentsAndStatusChanges(comments=[], statusChanges=[]) {
    let m_comments = comments.map((c) => {
       return {type: 'comment', data: c, created: c.created}
    });
    let m_statusChanges = statusChanges.map((sc) => {
      return { type:'status', data: sc, created: sc.created}
    });
    let all = concat(m_comments, m_statusChanges);
    return all.sort(function(a,b) {
      return a.created < b.created ? -1 : (a.created > b.created ? 1 : 0)
    })
  }

  flattenUsers(users=[]) {
    return fromJS(
      users.map((u) => {
        return {
          name: u.username
        }
      })
    )
  }

  render() {

    let all = this.flattenCommentsAndStatusChanges(
      this.props.comments,
      this.props.statusChanges
    );
    let users = this.flattenUsers(this.props.users)
    let items = all.map((x) => {
      if (x.type === 'comment') {
        return <Comment key={'comment-' + x.data.id} comment={x.data} users={users} />
      }
      if (x.type === 'status') {
        return <StatusChange key={'status-' + x.data.id} statusChange={x.data}/>
      }
      return null;
    });
    return (<div>{items}</div>);
  }

}

CommentList.propTypes = {
  comments: PropTypes.array.isRequired,
  statusChanges: PropTypes.array.isRequired
}
