import React from 'react'
import {Bar, Line} from 'react-chartjs-2'

class Graph extends React.Component {


  constructor(props) {
    super(props);
    this.state = {
      data :  {
        labels: [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        datasets: [{
          label: "Mood Barometer",
          backgroundColor: 'green',
          borderColor: 'rgba(134,159,152, 1)',
          hoverBackgroundColor: 'rgba(230, 236, 235, 0.75)',
          hoverBorderColor: 'rgba(230, 236, 235, 0.75)',
          data: [0,0,0,0,0,0,0,0,0,0,0,0]
        }]
      }
    }


    this.options = {
      scaleBeginAtZero: true,
      responsive: true,
      scaleStartValue: 0,
      maintainAspectRatio: false,
      scales: {
        xAxes: [{
          gridLines: {
            display: false
          }
        }],
        yAxes: [{
          ticks: {
            max: 50,
            min: -50
          },
        }]
      }
    }


    this.temp = [];
    this.holder = [];
    this.list = [];
    this.isLive = true;
    this.interval = null;
    this.addData = this.addData.bind(this);
  }






  addData() {

    if(this.isLive == true){
        this.temp = this.state.data.datasets[0].data;
    }
    else{
      this.temp = this.holder;
    }


    if(this.temp.length > 11){
      this.temp.pop();
      this.temp.unshift(this.list.pop())
    }
    else {
      this.temp.shift(this.list.pop())
    }


    if(this.isLive == true){
      this.setState({
        data :  {
          labels:  [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
          datasets: [{
            label: "Mood Barometer",
            backgroundColor: 'green',
            borderColor: 'rgba(134,159,152, 1)',
            hoverBackgroundColor: 'rgba(230, 236, 235, 0.75)',
            hoverBorderColor: 'rgba(230, 236, 235, 0.75)',
            data: this.temp

          }]
        }
      });
      this.refs.chart.chartInstance.update();
      this.runMeter(this.temp[0]);
    }
    else {
      this.runMeter(0);
      this.temp = this.holder;
    }
  }



  runMeter(num){
    var fillHeight = 0;
    var barSize = $('#barometer-top').height();

    if (num > 0) {
      fillHeight = (num / 100) * barSize;
      $('#barometer-fill-bottom').css('height', '0');
      $('#barometer-fill-top').css('height', 12 + fillHeight);
    } else {
      fillHeight = (num * (-1) / 100) * barSize;
      $('#barometer-fill-top').css('height', '0');
      $('#barometer-fill-bottom').css('height', 7 + fillHeight);
    }
  }



  intervalManager(flag, func, time){
    if(flag){
      if(this.interval != null){
        clearInterval(this.interval);
        this.refs.chart.chartInstance.update();
      }
      this.interval = setInterval(func, time);
    }
    else{
      this.refs.chart.chartInstance.update();
      clearInterval(this.interval)
    }
  }


  componentWillMount() {

    Chart.pluginService.register({
      beforeUpdate: function(chart) {
        var backgroundColor = [];
        var borderColor = [];

        for (var i = 0; i < chart.config.data.datasets[0].data.length; i++) {

          var value = chart.config.data.datasets[0].data[i];
          var color = value < 0 ? 'red' : 'green';

          backgroundColor.push(color);
          borderColor.push(color);
        }

        chart.config.data.datasets[0].backgroundColor = backgroundColor;
        chart.config.data.datasets[0].borderColor = borderColor;
      }
    });
  }





  componentDidMount() {
    this.intervalManager(this.isLive,this.addData,1000);
  }



  componentWillReceiveProps(nextProps){

    if(nextProps.data['data']){

        this.list = nextProps.data['data']
        this.isLive = true;
    }

    else if(nextProps.data['live']){


        this.setState({
          data :  {
            labels: this.holder,
            datasets: [{
              label: "Mood Barometer",
              backgroundColor: 'green',
              borderColor: 'rgba(134,159,152, 1)',
              hoverBackgroundColor: 'rgba(230, 236, 235, 0.75)',
              hoverBorderColor: 'rgba(230, 236, 235, 0.75)',
              data: this.holder

            }]
          }
        });
        this.isLive = true;

    }

    else if(nextProps.data['year1']){

      if(this.isLive == true){
        this.holder = this.state.data.datasets[0].data;
        this.isLive = false;
      }

        this.setState({
          data :  {
            labels: [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
            datasets: [{
              label: "Mood Barometer",
              backgroundColor: 'green',
              borderColor: 'rgba(134,159,152, 1)',
              hoverBackgroundColor: 'rgba(230, 236, 235, 0.75)',
              hoverBorderColor: 'rgba(230, 236, 235, 0.75)',
              data: nextProps.data['year1']

            }]
          }
        });
        this.refs.chart.chartInstance.update();
    }


    else if(nextProps.data['year2']){
      if(this.isLive == true){
        this.holder = this.state.data.datasets[0].data;
        this.isLive = false;
      }
      this.setState({
        data :  {
          labels: [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
          datasets: [{
            label: "Mood Barometer",
            backgroundColor: 'green',
            borderColor: 'rgba(134,159,152, 1)',
            hoverBackgroundColor: 'rgba(230, 236, 235, 0.75)',
            hoverBorderColor: 'rgba(230, 236, 235, 0.75)',
            data: nextProps.data['year2']

          }]
        }
      });
      this.refs.chart.chartInstance.update();
    }

    else if(nextProps.data['months']){
      var temp = [0,0,0,0,0,0,0,0,0,0,0,0];
      Object.keys(nextProps.data['months']).map(function(v,i){
        temp[v-1]=(nextProps.data['months'][v]*100);
      })
      if(this.isLive == true){
        this.holder = this.state.data.datasets[0].data;
        this.isLive = false;
      }
      this.setState({
        data :  {
          labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
          datasets: [{
            label: "Mood Barometer",
            backgroundColor: 'green',
            borderColor: 'rgba(134,159,152, 1)',
            hoverBackgroundColor: 'rgba(230, 236, 235, 0.75)',
            hoverBorderColor: 'rgba(230, 236, 235, 0.75)',
            data: temp

          }]
        }
      });
      this.refs.chart.chartInstance.update();
    }


  }



  render() {

    return (
      <div id = "graph-container" >

      <Bar ref = 'chart'
      data = {this.state.data}
      options = {this.options}
      width = {500}
      height = {500}
      />

      </div>
    )
  }
}



export default Graph;
