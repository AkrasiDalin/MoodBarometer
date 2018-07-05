import React from 'react'

class Header extends React.Component {

  constructor(props){
    super(props);
    this.updatePassword = this.updatePassword.bind(this)
  }

  updatePassword(){
    if(this.refs.password1.value == this.refs.password2.value){
      $.ajax({
        type: "POST",
        url: "/update",
        contentType: "application/json; charset=utf-8",
        data:  JSON.stringify({'user':this.props.userid,
                                    'opassword':this.refs.password0.value,
                                    'npassword': this.refs.password1.value}),
        success: function(data) {
          if(data=='/') window.location.href = data;
        }
      });
    }
  }


  render(){
    return (
      <div className="row">
      <div className="col-md-6 col-sm-6 col-xs-6 switch-container">
      
      </div>

      <div className="col-md-6 col-sm-6 col-xs-6">
        <div className="section">




          <ul className="nav">

            <li className="dropdown col-md-6">
              <a className="dropdown-toggle" href="#" data-toggle="dropdown">Change password</a>
              <div className="dropdown-menu dm">
                <form className="form-signin" ref='formy'>
                <input type="password" className="form-control" name="password0" ref="password0" placeholder="Current password" required="" />
                <input type="password" className="form-control" name="password1" ref="password1" placeholder="New password" required=""/>
                <input type="password" className="form-control" name="password2" ref="password2" placeholder="Confirm password" required=""/>

                  <input className="btn btn-primary btn-block" type="button" id="update" onClick={this.updatePassword} value="CHANGE" />
                </form>
              </div>
            </li>
            <li className="dropdown col-md-6">
            <a href="/logout">Logout</a>
            </li>
          </ul>



        </div>
      </div>
      </div>
    )
  }
}

export default Header;
