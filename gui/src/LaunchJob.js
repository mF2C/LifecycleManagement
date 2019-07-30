import React, { Component } from "react";
import request from "request";
import { Alert, Button, Dropdown, Badge } from 'react-bootstrap';
import vis from "vis-network";


class LaunchJob extends Component {


  constructor(props, context) {
    super(props, context);

    this.state = {
      selservice: "",
      value : "",
      start_si_button: false,
      msg: "",
      msg_content: "",
      show_alert: false,
      show_info: false
    };

    this.select = this.select.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }


  componentDidMount() {
    ////////////////////////////////////////////////////////////////////////////
    // create an array with nodes
    var nodes = new vis.DataSet([
      {id: 'ag_1', label: 'local mF2C AGENT', image: './img/node_mini.png', shape: 'image'},
      {id: 'ag_2', label: '192.168.1.21', image: './img/node_mini.png', shape: 'image'},
      {id: 'ag_3', label: '192.168.1.25', image: './img/node_mini.png', shape: 'image'},
      {id: 'ag_4', label: '192.168.1.26', image: './img/node_mini.png', shape: 'image'},
      {id: 'si_1_1', label: 'Service Instance 1', image: 'img/apps_mini.png', shape: 'image'},
      {id: 'si_1_2', label: 'Service Instance 1', image: 'img/apps_mini.png', shape: 'image'},
      {id: 'si_1_3', label: 'Service Instance 1', image: 'img/apps_mini.png', shape: 'image'},
      {id: 'si_2_1', label: 'Service Instance 2', image: './img/apps_mini.png', shape: 'image'},
      {id: 'si_2_2', label: 'Service Instance 2', image: './img/apps_mini.png', shape: 'image'}
    ]);

    // create an array with edges
    var edges = new vis.DataSet([
      {from: 'ag_1', to: 'ag_2', dashes: true, color:{color:'#111111'}},
      {from: 'ag_1', to: 'ag_3', dashes: true, color:{color:'#111111'}},
      {from: 'ag_1', to: 'ag_4', dashes: true, color:{color:'#111111'}},
      {from: 'ag_1', to: 'si_1_1', color:{color:'darkgreen'}},
      {from: 'ag_1', to: 'si_2_1', color:{color:'darkgreen'}},
      {from: 'ag_2', to: 'si_1_2', color:{color:'darkgreen'}},
      {from: 'ag_3', to: 'si_1_3', color:{color:'darkgreen'}},
      {from: 'ag_4', to: 'si_2_2', color:{color:'darkgreen'}}
    ]);

    // create a network
    var container = document.getElementById('mynetwork');
    var data = {
      nodes: nodes,
      edges: edges
    };
    var options = {};
    var network = new vis.Network(container, data, options);
  }


  select(event) {
    this.setState({
      value: event.target.innerText,
      selservice: event.target.innerText
    });
  }


  handleSubmit(event) {
    //event.preventDefault();
    console.log("Launching job in DER [service_instance=" + this.state.selservice + "] ...");

    var uri = "/api/v2/lm/" + this.state.selservice;
    // call to api
    try {
      request.put(uri)
        .on('response', function(response) {
          console.log(response.statusCode); // 200
          this.setState({ show_info: true });
          this.setState({ msg: "PUT " + uri + " : " + response.statusCode });
          this.setState({ msg_content: "Response: " + response.toString() });
        })
        .on('error', function(err) {
          console.error(err);
          this.setState({ show_alert: true });
          this.setState({ msg: "PUT " + uri });
          this.setState({ msg_content: err.toString() });
        })
    }
    catch(err) {
      console.error(err);
      this.setState({ show_alert: true });
      this.setState({ msg: "PUT " + uri });
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
        <h3><b>Jobs / DER</b></h3>
        <form>
          <div className="form-group row">
            <div className="col-sm-6">DER instances managed by this agent</div>
            <div className="col-sm-6">Select a DER and launch a job</div>
          </div>
          <div className="form-group row">
            <div id="mynetwork"></div>
            <div className="col-sm-6">
              <div className="form-group row">
                <Dropdown className="col-sm-2">
                  <Dropdown.Toggle variant="secondary" id="dropdown-basic">
                    Service
                  </Dropdown.Toggle>

                  <Dropdown.Menu>
                    <Dropdown.Item onClick={this.select}>COMPSs 1</Dropdown.Item>
                    <Dropdown.Item onClick={this.select}>COMPSs 2</Dropdown.Item>
                    <Dropdown.Item onClick={this.select}>COMPSs 3</Dropdown.Item>
                  </Dropdown.Menu>
                </Dropdown>
                <div className="col-sm-6">
                  <input type="text" className="form-control" id="service" value={this.state.selservice} readOnly/>
                </div>
              </div>

              <div className="form-group row">
                <div className="col-sm-10">
                  <textarea className="form-control" id="job" rows="10"/>
                </div>
              </div>

              <button type="submit" value="Submit" className="btn btn-success" onClick={this.handleSubmit}>Launch</button>
              &nbsp;
              <button className="btn btn-warning">Cancel</button>
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
          
        </form>
      </div>
    );
  }
}

export default LaunchJob;
