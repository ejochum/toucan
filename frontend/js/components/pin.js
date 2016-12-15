/**
 * Created by sean on 15/12/16.
 */
import React from 'react'
import classNames from 'classnames'
import Icon from 'react-fa'

let fallBackClick = (e) => {
    e.stopPropagation();
    console.log('pin clicked');
}

function Pin(props) {
    let onClick = props.togglePin || fallBackClick
    let active = props.active ? true : false;
    return <Icon name="thumb-tack"
                 className={classNames({
                     "text-muted": !active,
                     "text-danger": active
                 })
                 }
                 title={
                     props.active ?
                         "Click to un-pin":
                         "Click to pin"
                 }
                 onClick={onClick}
             />

}

Pin.propTypes = {
    active: React.PropTypes.bool,
    togglePin: React.PropTypes.func
}

export default Pin
