import React, { Component } from "react";
import request from "request";
import { Alert, Button } from 'react-bootstrap';


class SharingModel extends Component {


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
    console.log('Getting data from sharing model ...');

    // call to api
    try {
      request.get('/api/v2/um/sharing-model')
        .on('response', function(response) {
          console.log(response.statusCode); // 200
          this.setState({ show_info: true });
          this.setState({ msg: "GET /api/v2/um/sharing-model : " + response.statusCode });
          this.setState({ msg_content: "Sharing-model retrieved: response: " + response.toString() });
        })
        .on('error', function(err) {
          console.error(err);
          this.setState({ show_alert: true });
          this.setState({ msg: "GET /api/v2/um/sharing-model" });
          this.setState({ msg_content: err.toString() });
        })
    }
    catch(err) {
      console.error(err);
      this.setState({ show_alert: true });
      this.setState({ msg: "GET /api/v2/um/sharing-model" });
      this.setState({ msg_content: err.toString() });
    }
  }


  handleSave(event) {
    //event.preventDefault();
    console.log('Updating sharing model ...');

    // call to api
    // call to api
    try {
      request.put('/api/v2/um/sharing-model')
        .on('response', function(response) {
          console.log(response.statusCode); // 200
          this.setState({ show_info: true });
          this.setState({ msg: "PUT /api/v2/um/sharing-model : " + response.statusCode });
          this.setState({ msg_content: "Sharing-model updated: response: " + response.toString() });
        })
        .on('error', function(err) {
          console.error(err);
          this.setState({ show_alert: true });
          this.setState({ msg: "PUT /api/v2/um/sharing-model" });
          this.setState({ msg_content: err.toString() });
        })
    }
    catch(err) {
      console.error(err);
      this.setState({ show_alert: true });
      this.setState({ msg: "PUT /api/v2/um/sharing-model" });
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
        <h3><b>Sharing Model</b></h3>
        <p>List of agent's resources shared in mF2C:</p>
        <form>
          <div className="form-group row">
            <div className="col-sm-2">GPS</div>
            <div className="col-sm-10">
              <div className="form-check">
                <input className="form-check-input" type="checkbox" id="GPSCheck1"/>
                <small className="form-check-label text-muted" htmlFor="GPSCheck1">
                  Allow the use of GPS by mF2C
                </small>
              </div>
            </div>
          </div>

          <div className="form-group row">
            <label htmlFor="cpuUsageLbl" className="col-sm-2 col-form-label">Max. CPU usage</label>
            <div className="col-sm-2">
              <input type="cpuUsage" className="form-control" id="cpuUsage" placeholder="10 - 90"/>
            </div>
            <small id="cpuUsageHelp" className="col-sm-2 form-text text-muted">Integer Value between 10 - 90</small>
          </div>

          <div className="form-group row">
            <label htmlFor="memUsageLbl" className="col-sm-2 col-form-label">Max. memory usage</label>
            <div className="col-sm-2">
              <input type="memUsage" className="form-control" id="memUsage" placeholder="10 - 90"/>
            </div>
            <small id="memUsageHelp" className="col-sm-2 form-text text-muted">Integer Value between 10 - 90</small>
          </div>

          <div className="form-group row">
            <label htmlFor="storageUsageLbl" className="col-sm-2 col-form-label">Max. storage usage</label>
            <div className="col-sm-2">
              <input type="cpuUsage" className="form-control" id="storageUsage" placeholder="10 - 90"/>
            </div>
            <small id="storageUsageHelp" className="col-sm-2 form-text text-muted">Integer Value between 10 - 90</small>
          </div>

          <div className="form-group row">
            <label htmlFor="bandwidthUsageLbl" className="col-sm-2 col-form-label">Max. bandwidth usage</label>
            <div className="col-sm-2">
              <input type="bandwidthUsage" className="form-control" id="cpuUsage" placeholder="10 - 90"/>
            </div>
            <small id="bandwidthUsageHelp" className="col-sm-2 form-text text-muted">Integer Value between 10 - 90</small>
          </div>

          <div className="form-group row">
            <label htmlFor="batteryUsageLbl" className="col-sm-2 col-form-label">Max. battery level usage</label>
            <div className="col-sm-2">
              <input type="batteryUsage" className="form-control" id="batteryUsage" placeholder="10 - 90"/>
            </div>
            <small id="batteryUsageHelp" className="col-sm-2 form-text text-muted">Integer Value between 10 - 90</small>
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

export default SharingModel;
