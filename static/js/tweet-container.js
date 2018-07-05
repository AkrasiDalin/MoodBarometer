import React from 'react'

class TweetContainer extends React.Component{

  render(){
    return (
      <li id="tweet-container" className="row list-group-item">

          <div className="row list-group-item active">
            <div className="col-md-6 polarity">{this.props.polarity}</div>
            <div className="col-md-6 time">{this.props.time}</div>
          </div>

          <div className="row list-group-item body">
            <p className="msg">{this.props.text}</p>
          </div>

      </li>
    )
  }
}

export default TweetContainer;
