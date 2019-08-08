import React, { Component } from "react";
import request from "request";
import { Alert, Button, Badge, Spinner } from 'react-bootstrap';


class UserProfile extends Component {


  constructor(props, context) {
    super(props, context);

    this.state = {
      isLoading: false,
      msg: "",
      msg_content: "",
      show_alert: false,
      show_info: false,
      // user-profile properties
      id_user_profile: "",
      resource_contributor: false,
      service_consumer: false
    };

    this.handleView = this.handleView.bind(this);
    this.handleSave = this.handleSave.bind(this);
    this.onDismiss = this.onDismiss.bind(this);
    this.handleChange_resource_contributor = this.handleChange_resource_contributor.bind(this);
    this.handleChange_service_consumer = this.handleChange_service_consumer.bind(this);
  }


  componentDidMount() {
    this.handleView(null);
  }


  handleChange_resource_contributor(event) {
    if (this.state.resource_contributor) {
      this.setState({resource_contributor: false});
    } else {
      this.setState({resource_contributor: true});
    }
  }


  handleChange_service_consumer(event) {
    if (this.state.service_consumer) {
      this.setState({service_consumer: false});
    } else {
      this.setState({service_consumer: true});
    }
  }


  handleView(event) {
    this.setState({isLoading: true});
    console.log('Getting data from user-profile ...');
    // call to api
    try {
      var that = this;
      request.get({url: global.rest_api_um + 'user-profile'}, function(err, resp, body) {
        if (err) {
          console.error(err);
          that.setState({ show_alert: true, msg: "GET /api/v2/um/user-profile", msg_content: err.toString() });
        }
        else {
          console.log('Getting data from user-profile ... ok');
          if (global.debug) {
            //that.setState({ show_info: true, msg: "GET /api/v2/um/user-profile => " + resp.statusCode, msg_content: "User-profile retrieved: response: " + body });
          }
          // user-profile properties
          try {
            body = JSON.parse(body);
            that.setState({ resource_contributor: body['user_profile']['resource_contributor'], service_consumer: body['user_profile']['service_consumer'],
                            id_user_profile: body['user_profile']['id']});
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
      this.setState({ show_alert: true, msg: "GET /api/v2/um/user-profile", msg_content: err.toString(), isLoading: false });
    }
  }


  handleSave(event) {
    this.setState({isLoading: true});
    console.log('Updating user-profile ...');
    // call to api
    try {
      var that = this;
      var formData = {
        id: this.state.id_user_profile,
        service_consumer: this.state.service_consumer,
        resource_contributor: this.state.resource_contributor,
      };
      console.log(formData);
      request.put({ url: global.rest_api_um + this.state.id_user_profile, json: formData}, function(err, resp, body) {
        if (err) {
          console.error(err);
          that.setState({ show_alert: true, msg: "PUT /api/v2/um/" + that.state.id_user_profile, msg_content: err.toString() });
        }
        else {
          console.log('Updating user-profile ... ok');
          that.setState({ show_info: true, msg: "PUT /api/v2/um/" + that.state.id_user_profile + " => " + resp.statusCode,
                          msg_content: "User-profile updated: response: " + JSON.stringify(body) });
        }

        that.setState({isLoading: false});
      });
    }
    catch(err) {
      console.error(err);
      this.setState({ show_alert: true, msg: "PUT /api/v2/um/user-profile", msg_content: err.toString(), isLoading: false });
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
        <h3><b>User Profile</b>&nbsp;&nbsp;&nbsp;
          {this.state.isLoading ?
            <Spinner animation="border" role="status" variant="primary">
              <span className="sr-only">Loading...</span>
            </Spinner> : ""}
        </h3>
        <p>How the agent will make use of mF2C:</p>
        <form>
          <div className="form-group row">
            <div className="col-sm-3">Resource contributor</div>
            <div className="col-sm-9">
              <div className="form-check">
                <input className="form-check-input" type="checkbox" id="RCCheck1" checked={this.state.resource_contributor} onChange={this.handleChange_resource_contributor}/>
                <small className="form-check-label text-muted" htmlFor="RCCheck1">
                  Allow other mF2C devices to use agent's resources (RAM, Battery ...)
                </small>
              </div>
            </div>
          </div>

          <div className="form-group row">
            <div className="col-sm-3">Service Consumer</div>
            <div className="col-sm-9">
              <div className="form-check">
                <input className="form-check-input" type="checkbox" id="SCCheck1" disabled checked={this.state.service_consumer} onChange={this.handleChange_service_consumer}/>
                <small className="form-check-label text-muted" htmlFor="SCCheck1">
                  Check if you will launch services to be executed in mF2C
                </small>
              </div>
            </div>
          </div>

          <Badge variant="secondary">{this.state.id_user_profile}</Badge><br />

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

          <Button variant="primary" onClick={this.handleView} disabled={this.state.isLoading}><i class="fa fa-search" aria-hidden="true"></i>&nbsp;View</Button>
          &nbsp;
          <Button variant="success" onClick={this.handleSave} disabled={this.state.isLoading}><i class="fa fa-floppy-o" aria-hidden="true"></i>&nbsp;Save</Button>
        </form>
      </div>
    );
  }
}

export default UserProfile;
