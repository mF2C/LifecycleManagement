import React, { Component } from "react";
import request from "request";
import { Alert, Button } from 'react-bootstrap';


class UserProfile extends Component {


  constructor(props, context) {
    super(props, context);

    this.state = {
      msg: "",
      msg_content: "",
      show_alert: false,
      show_info: false
    };

    this.handleView = this.handleView.bind(this);
    this.handleSave = this.handleSave.bind(this);
    this.onDismiss = this.onDismiss.bind(this);
  }


  handleView(event) {
    //event.preventDefault();
    console.log('Getting data from user-profile ...');

    // call to api
    try {
      request.get('/api/v2/um/user-profile')
        .on('response', function(response) {
          console.log(response.statusCode); // 200
          this.setState({ show_info: true });
          this.setState({ msg: "GET /api/v2/um/user-profile : " + response.statusCode });
          this.setState({ msg_content: "User-profile retrieved: response: " + response.toString() });
        })
        .on('error', function(err) {
          console.error(err);
          this.setState({ show_alert: true });
          this.setState({ msg: "GET /api/v2/um/user-profile" });
          this.setState({ msg_content: err.toString() });
        })
    }
    catch(err) {
      console.error(err);
      this.setState({ show_alert: true });
      this.setState({ msg: "GET /api/v2/um/user-profile" });
      this.setState({ msg_content: err.toString() });
    }
  }


  handleSave(event) {
    //event.preventDefault();
    console.log('Updating user-profile ...');

    // call to api
    // call to api
    try {
      request.put('/api/v2/um/user-profile')
        .on('response', function(response) {
          console.log(response.statusCode); // 200
          this.setState({ show_info: true });
          this.setState({ msg: "PUT /api/v2/um/user-profile : " + response.statusCode });
          this.setState({ msg_content: "User-profile updated: response: " + response.toString() });
        })
        .on('error', function(err) {
          console.error(err);
          this.setState({ show_alert: true });
          this.setState({ msg: "PUT /api/v2/um/user-profile" });
          this.setState({ msg_content: err.toString() });
        })
    }
    catch(err) {
      console.error(err);
      this.setState({ show_alert: true });
      this.setState({ msg: "PUT /api/v2/um/user-profile" });
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
      <div style={{margin: "-25px 0px 0px 0px"}}>
        <h3><b>User Profile</b></h3>
        <p>How the agent will make use of mF2C:</p>
        <form>
          <div className="form-group row">
            <div className="col-sm-2">Resource contributor</div>
            <div className="col-sm-10">
              <div className="form-check">
                <input className="form-check-input" type="checkbox" id="RCCheck1"/>
                <small className="form-check-label text-muted" htmlFor="RCCheck1">
                  Allow other mF2C devices to use agent's resources (RAM, Battery ...)
                </small>
              </div>
            </div>
          </div>

          <div className="form-group row">
            <div className="col-sm-2">Service Consumer</div>
            <div className="col-sm-10">
              <div className="form-check">
                <input className="form-check-input" type="checkbox" id="SCCheck1"/>
                <small className="form-check-label text-muted" htmlFor="SCCheck1">
                  Check if you will launch services to be executed in mF2C
                </small>
              </div>
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
          <button className="btn btn-success" onClick={this.handleSave}>Save</button>
        </form>
      </div>
    );
  }
}

export default UserProfile;
