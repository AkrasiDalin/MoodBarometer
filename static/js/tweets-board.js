import React from 'react'
import TweetContainer from './tweet-container'


class TweetsBoard extends React.Component {

  constructor(props){
    super(props);

    this.state = {
      list: [],
      items : []
    }
  }

  componentDidMount(){
    setInterval(function(){
      this.addToItems()
    }.bind(this),2000);
  }


  componentWillReceiveProps(nextProps){
    this.addToList(nextProps.data)
  }


  addToList(data){
    var listTemp = this.state.list.concat(data);
    this.setState({
      list: listTemp
    })

  }

  addToItems(){
      var listTemp = this.state.list;
      var itemsTemp = this.state.items;
      //remove first item from list
      if(listTemp.length > 0){
        var item = listTemp.shift()
        // add item to items
        if(itemsTemp.length > 2){
          // remove last element from items
          itemsTemp.pop();
          // enter new one at the start
          itemsTemp.unshift(item);
        }
        else itemsTemp.unshift(item);

        this.setState({
          list: listTemp,
          items: itemsTemp
        })
    }
  }


  isPositive(value){
    if(value>0)return 'POSITIVE';
    else if(value<0) return 'NEGATIVE';
    else if(value == 0)  return 'NEUTRAL';
  }


  render(){

      return (
        <div className="container">
            <div className="panel-group">
                <div className="panel text-center panel-default">
                    <div className="panel-heading">
                        <h4 className="panel-title"> <a>tweets</a>
                        </h4>
                    </div>
                    <div className="list-container">
                        <ul className="list-group">

                            {this.state.items.map(function(v,i){
                              return <TweetContainer
                                          key={i}
                                          polarity={this.isPositive(v.value)}
                                          time={v.time}
                                          text={v.text}
                                      />;
                                    }.bind(this))
                              }
                        </ul>
                    </div>
                </div>
            </div>
        </div>


      )
  }
}

export default TweetsBoard;
