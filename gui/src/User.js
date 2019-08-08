import React, { Component } from "react";
import request from "request";
import { Alert, Button, Spinner } from 'react-bootstrap';


class User extends Component {


  constructor(props, context) {
    super(props, context);

    this.state = {
      isLoading: false,
      username: "",
      msg: "",
      msg_content: "",
      show_alert: false,
      show_info: false
    };

    this.handleView = this.handleView.bind(this);
    this.handleRemove = this.handleRemove.bind(this);
    this.onDismiss = this.onDismiss.bind(this);
    this.handleChangeUsername = this.handleChangeUsername.bind(this);
  }


  handleView(event) {
    this.setState({isLoading: true});
    console.log('Getting data from user [' + this.state.username + '] ...');
    // call to api
    try {
      var that = this;
      request.get({url: global.rest_api_um + 'user/' + this.state.username}, function(err, resp, body) {
        if (err) {
          console.error(err);
          that.setState({ show_alert: true, msg: "GET /api/v2/um/", msg_content: err.toString() });
        }
        else {
          console.log('Getting data from user ... ok');
          if (global.debug) {
            that.setState({ show_info: true, msg: "GET /api/v2/um/l => " + resp.statusCode, msg_content: "User retrieved: response: " + JSON.stringify(body) });
          }
          // user properties
          try {
            body = JSON.parse(body);

          }
          catch(err) {
            console.error(err);
          }
        }

        that.setState({isLoading: false});
      });
    }
    catch(err) {
      console.error(err);
      this.setState({ show_alert: true, msg: "GET /api/v2/um/", msg_content: err.toString(), isLoading: false });
    }
  }


  handleRemove(event) {
    this.setState({isLoading: true});
    console.log('Removing user [' + this.state.username + '] from mF2C...');
    // call to api
    try {
      var that = this;
      var formData = {
        user_id: this.state.username
      };
      request.delete({url: global.rest_api_um + 'user', json: formData}, function(err, resp, body) {
        if (err) {
          console.error(err);
          that.setState({ show_alert: true, msg: "DELETE /api/v2/um/", msg_content: err.toString() });
        }
        else {
          console.log('Removing user from mF2C... ok');
          if (global.debug) {
            that.setState({ show_info: true, msg: "DELETE /api/v2/um/l => " + resp.statusCode, msg_content: "User removed: response: " + JSON.stringify(body) });
          }
        }

        that.setState({isLoading: false});
      });
    }
    catch(err) {
      console.error(err);
      this.setState({ show_alert: true, msg: "DELETE /api/v2/um/", msg_content: err.toString(), isLoading: false });
    }
  }


  handleChangeUsername(event) {
    this.setState({username: event.target.value});
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
        <h3><b>User</b>&nbsp;&nbsp;&nbsp;
          {this.state.isLoading ?
            <Spinner animation="border" role="status" variant="primary">
              <span className="sr-only">Loading...</span>
            </Spinner> : ""}
        </h3>
        <p>MF2C user information:</p>
        <form>
          <div className="form-group row">
            <label htmlFor="cpuUsageLbl" className="col-sm-2 col-form-label">Username</label>
            <div className="col-sm-4">
              <input type="text" className="form-control" id="username" value={this.state.username} onChange={this.handleChangeUsername} placeholder="Username"/>
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

          <Button variant="primary" onClick={this.handleView} disabled={this.state.username.length == 0 || this.state.isLoading}>
            <i class="fa fa-search" aria-hidden="true"></i>&nbsp;View</Button>
          &nbsp;
          <Button variant="danger" onClick={this.handleRemove} disabled={this.state.username.length == 0 || this.state.isLoading}>
            <i class="fa fa-trash" aria-hidden="true"></i>&nbsp;Remove</Button>
        </form>
      </div>
    );
  }
}

export default User;
