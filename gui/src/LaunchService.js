import React, { Component } from "react";
import { Alert, Spinner, Button, Tabs, Tab, TabPane } from 'react-bootstrap';
import request from "request";


class LaunchService extends Component {


  constructor(props, context) {
    super(props, context);

    this.state = {
      isLoading: false,
      serv_def: "{}",
      msg: "",
      msg_content: "",
      show_alert: false,
      show_info: false
    };

    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleCancel = this.handleCancel.bind(this);
    this.handleChange_serv_def = this.handleChange_serv_def.bind(this);
  }


  handleChange_serv_def(event) {
    this.setState({serv_def: event.target.value});
  }


  handleSubmit(event) {
    this.setState({isLoading: true});
    console.log("Launching a new service in mF2C ...");

    // call to api
    try {
      var that = this;
      var formData = JSON.parse(this.state.serv_def);

      request.post({url: global.rest_api_lm + "service", json: formData}, function(err, resp, body) {
        if (err) {
          console.error(err);
          that.setState({ show_alert: true, msg: "POST /api/v2/lm/service" + that.state.sel_service_instance_id_1 + "/der", msg_content: err.toString() });
        }
        else {
          console.log("Launching a new service in mF2C ... ok");
          if (global.debug) {
            body = JSON.stringify(body);
            that.setState({ show_info: true, msg: "POST /api/v2/lm/service" + that.state.sel_service_instance_id_1 + "/der => " + resp.statusCode, msg_content: "Service launched: response: " + body });
          }
        }

        that.setState({isLoading: false});
      });
    }
    catch(err) {
      console.error(err);
      this.setState({ show_alert: true, msg: "POST /api/v2/lm/servicer", msg_content: err.toString(), isLoading: false });
    }
  }


  handleCancel(event) {
    this.setState({serv_def: "{}"});
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
        <h3><b>Launch a new service</b>&nbsp;&nbsp;&nbsp;
          {this.state.isLoading ?
            <Spinner animation="border" role="status" variant="primary">
              <span className="sr-only">Loading...</span>
            </Spinner> : ""}
        </h3>


        <Tabs defaultActiveKey="json">
          <TabPane eventKey="json" title="json" style={{backgroundColor: "white"}}>
            <p>Define a service (json) and run it in mF2C</p>

            <form onSubmit={this.handleSubmit}>
              <div className="form-group row">
                <div className="col-sm-8">
                  <textarea className="form-control" id="job" rows="10" value={this.state.serv_def} onChange={this.handleChange_serv_def}>
                  </textarea>
                </div>
              </div>

              <Button variant="success" onClick={this.handleSubmit} disabled={this.state.isLoading}><i class="fa fa-rocket" aria-hidden="true"></i>&nbsp;Launch</Button>
              &nbsp;
              <Button variant="warning" onClick={this.handleCancel} disabled={this.state.isLoading}><i class="fa fa-times" aria-hidden="true"></i>&nbsp;Cancel</Button>

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
            </form>
          </TabPane>

          <TabPane eventKey="other" title="other" disabled></TabPane>
        </Tabs>
      </div>
    );
  }
}

export default LaunchService;
