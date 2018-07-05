import React from 'react'


class Month extends React.Component {

  getMonth(num){
      if(num== 1) return 'January';
      else if(num==2) return 'February';
      else if(num==3) return 'March';
      else if(num== 4) return 'April';
      else if(num== 5) return 'May';
      else if(num== 6) return 'June';
      else if(num== 7) return 'July';
      else if(num== 8) return 'August';
      else if(num== 9) return 'September';
      else if(num== 10) return 'October';
      else if(num== 11) return 'November';
      else if(num== 12) return 'December';
  }


  render(){
    return (
          <div className="panel-body">
          <a href='#' onClick={()=>this.props.updater(this.props.index, this.props.month, this.props.year)}>{this.getMonth(this.props.month)}
          </a>
          </div>

    )
  }
}




class Year extends React.Component {

  render(){
    return (
      <div className="panel panel-default">
          <div className="panel-heading">
              <h4 className="panel-title">
                  <a onClick={()=>this.props.updater(this.props.index, 0, this.props.data.year.numeric)} data-toggle="collapse" data-parent="#accordion" href={"#collapse"+(this.props.index)+""}>
                      {this.props.data.year.numeric}</a>
              </h4>
          </div>
          <div id={'collapse'+this.props.index} className="panel-collapse collapse">

          {Object.keys(this.props.data.months).map(function(v,i){
            return (
              <Month key={i} month={v} index={i} year={this.props.index} updater={this.props.updater}/>
              )
            }.bind(this))
          }

          </div>
      </div>
    )
  }
}


class DateBoard extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      data : []
    }
  }

  componentDidMount(){
    setTimeout(function(){
      this.setState({
        data: this.props.data
      });
    }.bind(this),100);
  }



  render(){
    return (
      <div id="dates-board" className="col-xl-1 col-lg-2 col-md-2 col-sm-2 hidden-xs">

          <div className="panel-group pan" id="accordion">
          <div className="panel panel-default">
              <div className="panel-heading" id="current">
                  <h4 className="panel-title">
                      <a onClick={()=>this.props.updater('current')} data-toggle="collapse" data-parent="#accordion" href={"#collapse"+(this.props.index)+""}>
                          CURRENT</a>
                  </h4>
              </div>
          </div>

              {this.state.data.map((k,i) => {
                return <Year key={i} data={k} index={i} updater={this.props.updater} />
              })}

          </div>
      </div>
    )
  }
}

export default DateBoard;
