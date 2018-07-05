import React from "react";
import ReactDOM from "react-dom";
import Chart from './chart'
import TweetsBoard from './tweets-board'
import Header from './header'
import Meter from './gauge-meter'
import DateBoard from './dates-board'


class Barometer extends React.Component {
  render(){
    return (
      <div className="col-xl-1 col-lg-1 col-md-1 col-xs-1">
          <div id="barometer">
              <div id="barometer-top">
                  <div id="barometer-fill-top"></div>
              </div>
              <div id="barometer-center">
                  <span></span>
              </div>
              <div id="barometer-bottom">
                  <div id="barometer-fill-bottom"></div>
              </div>
          </div>
      </div>


    )
  }
}
var stuff = []

class Main extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      user_id: '',
      isUpdated: false,
      chartData: [],
      tweetsBoardData: [],
      datesBoardData: {},
      meterData: 10
    }
    this.chartTemp = [];
    this.updateGraph = this.updateGraph.bind(this);
  }


  componentWillMount(){
    this.getData()
  }






  updateData(){
    var self = this;
    setInterval(function(){
      $('#result').text(self.state.tweetsBoardData[0].time);
      return false;
    }, 1000);
  }

  getData(){
    var self = this;
      $.getJSON('/_data_req', {
        req: 'graph_data'
      }, function(data){
        self.chartTemp = self.chartTemp.concat(self.prepareForChart(data.response['live']));
        self.setState({
          user_id: data.response['user_id'],
          tweetsBoardData: data.response['live'],
          chartData: {'data':self.chartTemp},
          meterData: {'data': data.response['dates_table'][0].year.value},
          datesBoardData: data.response['dates_table'],
          isUpdated: true
        });
      });
  }


  prepareForChart(data){
    var temp = [];
    data.map(function(item, val){
      temp.push((item.value*100))
    })
    return temp;
  }

  updateGraph(index, month, year){
    var self = this;
    if(index=='current'){
      this.setState({
        chartData: {'live':[]}
      })
    }
    else {
      if(month == 0){
        this.yearGraph(index, month, year)
      }
      else {
        this.monthGraph(index, month, year)
      }
    }
  }

  yearGraph(index, month, year){
    this.setState({
      chartData: {'months': this.state.datesBoardData[index].months},
      meterData: {'year': this.state.datesBoardData[index].year.value}
    })
  }


  monthGraph(index, month, year){
    this.setState({
      meterData: {'month': this.state.datesBoardData[year].months[month]}
    })
  }



  render(){

    return (
      <div>
      <nav  className="col-sm-2 col-md-2 hidden-sm hidden-xs bg-faded sidebar">

      <div id="tweets-board">
        <TweetsBoard id="board" data={this.state.tweetsBoardData}/>
      </div>
        <Meter data={this.state.meterData}/>
        </nav>
        <main className="col-md-10 offset-md-2 col-sm-12 offset-sm-3 pt-3">

          <Header userid={this.state.user_id}/>

          <div className="row body">

              <div className="col-xl-10 col-lg-10 col-md-10 col-sm-10 col-xs-12 baro-graph">

                  <Barometer/>

                  <Chart data={this.state.chartData}/>

              </div>
              <DateBoard data={this.state.datesBoardData} updater={this.updateGraph}/>
          </div>
      </main>
    </div>
    )
  }
}

ReactDOM.render(<Main/>, document.getElementById('app'));
