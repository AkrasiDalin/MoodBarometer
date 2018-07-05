import React from 'react'

class Meter extends React.Component {

  constructor(props){
    super(props);
    this.degree = 0;
  }


  componentWillReceiveProps(nextProps){
    var need = document.getElementById('needle')
    var percentage = 0;
    if('data' in nextProps.data){
      percentage = (Math.floor(Math.random()*(nextProps.data['data']*100)) + 1)/100;
    }
    else if('year' in nextProps.data){
        percentage = (Math.floor(Math.random()*(nextProps.data['year']*100)) + 1)/100;
    }
    else if('month' in nextProps.data){
      percentage = (Math.floor(Math.random()*(nextProps.data['month']*100)) + 1)/100;
    }
    else if('weeks' in nextProps.data){

    }

    this.degree = percentage * 180;
    need.style.transform = 'rotate('+this.degree+'deg)';
  }


  getSentiment(val){
      if(val == 0) return 'NEUTRAL';
      else if(val < -60 && val >= -120) return 'VERY NEGATIVE';
      else if(val < -30 && val >= -60) return 'NEGATIVE';
      else if(val < 0 && val >= -30) return 'FAIRLY NEGATIVE';

      else if(val > 0 && val <= 30) return 'FAIRLY POSITIVE';
      else if(val > 30 && val <= 60) return 'POSITIVE';
      else if(val > 60 && val <= 120) return 'VERY POSITIVE';
  }


  render(){
    return (
    <div className="meter-container">
      <div className="meter">
        <div className="gauge">
          <div className="category very_poor"></div>
          <div className="category poor"></div>
          <div className="category fair"> </div>
          <div className="category good"></div>
          <div className="category very_good"></div>
          <div className="category excellent"></div>
        <div className="needle" id="needle"></div>

      </div><p id="gauge-evaluation">{this.getSentiment(this.degree)}</p>
    </div>
    <div className="glass"></div>
  </div>


    )
  }
}

export default Meter;
