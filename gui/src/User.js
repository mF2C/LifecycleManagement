import React, { Component } from "react";
import request from "request";
import { Alert, Button } from 'react-bootstrap';


class User extends Component {


  constructor(props, context) {
    super(props, context);

    this.state = {
      username: "username",
      msg: "",
      msg_content: "",
      show_alert: false,
      show_info: false
    };

    this.handleView = this.handleView.bind(this);
    this.handleRemove = this.handleRemove.bind(this);
    this.onDismiss = this.onDismiss.bind(this);
  }


  handleView(event) {
    //event.preventDefault();
    console.log('Getting data from user [' + this.state.username + '] ...');

    // call to api
    try {
      request.get('/api/v2/um/user/' + this.state.username)
        .on('response', function(response) {
          console.log(response.statusCode); // 200
          this.setState({ show_info: true });
          this.setState({ msg: "GET /api/v2/um/user/" + this.state.username + " : " + response.statusCode });
          this.setState({ msg_content: "User removed from mF2C: response: " + response.toString() });
        })
        .on('error', function(err) {
          console.error(err);
          this.setState({ show_alert: true });
          this.setState({ msg: "GET /api/v2/um/user/" + this.state.username});
          this.setState({ msg_content: err.toString() });
        })
    }
    catch(err) {
      console.error(err);
      this.setState({ show_alert: true });
      this.setState({ msg: "GET /api/v2/um/user/" + this.state.username});
      this.setState({ msg_content: err.toString() });
    }
  }


  handleRemove(event) {
    //event.preventDefault();
    console.log('Removing user [' + this.state.username + '] ...');

    // call to api
    try {
      request.delete('/api/v2/um/user/' + this.state.username)
        .on('response', function(response) {
          console.log(response.statusCode); // 200
          this.setState({ show_info: true });
          this.setState({ msg: "DELETE /api/v2/um/user/" + this.state.username + " : " + response.statusCode });
          this.setState({ msg_content: "User removed from mF2C: response: " + response.toString() });
        })
        .on('error', function(err) {
          console.error(err);
          this.setState({ show_alert: true });
          this.setState({ msg: "DELETE /api/v2/um/user/" + this.state.username});
          this.setState({ msg_content: err.toString() });
        })
    }
    catch(err) {
      console.error(err);
      this.setState({ show_alert: true });
      this.setState({ msg: "DELETE /api/v2/um/user/" + this.state.username});
      this.setState({ msg_content: err.toString() });
    }
  }


  onDismiss() {
    this.setState({ show_alert: false });
    this.setState({ show_info: false });
    this.setState({ msg: "" });
    this.setState({ msg_content: "" });
  }


  render() {
    return (
      <div style={{margin: "25px 0px 0px 0px"}}>
        <h3><b>User</b></h3>
        <p>MF2C user information:</p>
        <form>
          <div className="form-group row">
            <label htmlFor="cpuUsageLbl" className="col-sm-2 col-form-label">Username</label>
            <div className="col-sm-4">
              <input type="text" className="form-control" id="username" value={this.state.username} readOnly/>
            </div>
          </div>

          <Alert variant="danger" toggle={this.onDismiss} show={this.state.show_alert}>
            <p><b>{this.state.msg}</b></p>
            <p className="mb-0">{this.state.msg_content}</p>
            <div className="d-flex justify-content-end">
              <Button onClick={() => this.setState({ show_alert: false })} variant="outline-danger">
                Close
              </Button>
            </div>
          </Alert>

          <Alert variant="primary" toggle={this.onDismiss} show={this.state.show_info}>
            <p><b>{this.state.msg}</b></p>
            <p className="mb-0">{this.state.msg_content}</p>
            <div className="d-flex justify-content-end">
              <Button onClick={() => this.setState({ show_info: false })} variant="outline-primary">
                Close
              </Button>
            </div>
          </Alert>

          <button type="submit" className="btn btn-primary" onClick={this.handleView}>View</button>
          &nbsp;
          <button className="btn btn-danger" onClick={this.handleRemove}>Remove</button>
        </form>
      </div>
    );
  }
}

export default User;
