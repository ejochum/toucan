import React, {PropTypes} from 'react'
import { connect } from 'react-redux'
import UI from '../components/main'
import getFilteredIssues from '../issueSelector'
import ReconnectingWebSocket from 'reconnectingwebsocket';

import { selectIssue, fetchIssues, setCoordinates,
         resetCoordinates, loadCurrentUserInformation,
         receiveMessage } from '../actions'


class IssueTrackerApp extends React.Component {

  componentDidMount() {
    this.props.loadCurrentUserInformation()
    this.props.fetchIssues();
    this.ws = this.connectWS();
    this.ws.onmessage = (e) => { this.props.receiveWSMessage(e.data) };
  }

  connectWS() {
    let ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    let ws_path = ws_scheme + '://' + window.location.host;
    let ws = new ReconnectingWebSocket(ws_path);
    ws.onopen = function() { console.log("Connected to notification socket"); }
    ws.onclose = function() { console.log("Disconnected from notification socket"); }
    return ws;
  }

  render() {
    return <UI {...this.props} />
  }
}

IssueTrackerApp.propType = {
  fetchIssues: PropTypes.func.isRequired,
  setCoordinates: PropTypes.func.isRequired,
  issues: PropTypes.array.isRequired,
  coordinates: PropTypes.object,
  loadCurrentUserInformation: PropTypes.func.isRequired,
  bounds: PropTypes.array.isRequired,
  receiveWSMessage: PropTypes.func.isRequired,
  // Injected by React Router
  children: PropTypes.node
}

const mapStateToProps = (state) => {
  return {
    allIssues: state.redux_issues,
    issues: getFilteredIssues(state.redux_issues, state.issueFilters.selections),
    geojson: state.geojson,
    selectedIssue: state.selectedIssue,
    bounds: state.currentUser.bbox,
    coordinates: state.coordinates
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    fetchIssues: () => {
      dispatch(fetchIssues())
    },
    setCoordinates: (latLng) => {
      dispatch(setCoordinates(latLng))
    },
    clearCoordinates: () => {
      dispatch(resetCoordinates())
    },
    selectIssue: (issue_id) => {
      dispatch(selectIssue(issue_id));
    },
    loadCurrentUserInformation: () => {
      dispatch(loadCurrentUserInformation())
    },
    receiveWSMessage: (data) => {
      console.log('receiveWSMessage called', data);
      dispatch(receiveMessage(data));
    }
  };
}

const RootUI = connect(
  mapStateToProps,
  mapDispatchToProps
)(IssueTrackerApp)

export default RootUI
