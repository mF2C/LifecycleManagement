import React, { Component } from "react";

import vis from "vis-network";
import { Dropdown } from 'react-bootstrap';


class LaunchJob extends Component {


  constructor(props, context) {
    super(props, context);

    this.state = {
      selservice: "",
      value : ""
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
    alert('A new service was submitted: ' + this.state.value);
    event.preventDefault();
  }


  render() {
    return (
      <div>
        <h2>Service Instances</h2>
        <form>
          <div className="form-group row">
            <div className="col-sm-6">DER instances managed by this agent</div>
            <div className="col-sm-6">Select a DER and launch a job</div>
          </div>
          <div className="form-group row">
            <div id="mynetwork"></div>
            <div className="col-sm-6">
              <form onSubmit={this.handleSubmit}>
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
                    <input type="text" className="form-control" id="service" value={this.state.selservice}
                    onChange={this.handleChange}/>
                  </div>
                </div>

                <div className="form-group row">
                  <div className="col-sm-10">
                    <textarea className="form-control" id="job" rows="10"/>
                  </div>
                </div>

                <button type="submit" value="Submit" className="btn btn-success">Launch</button>
                <button className="btn btn-warning">Cancel</button>
              </form>
            </div>
          </div>
          <div className="form-group row">
            <div className="col-sm-6">
              <button type="submit" className="btn btn-primary">View</button>
              <button type="submit" className="btn btn-success">Start</button>
              <button type="submit" className="btn btn-warning">Stop</button>
              <button type="submit" className="btn btn-danger">Delete</button>
            </div>
            <div className="col-sm-6">

            </div>
          </div>
        </form>
      </div>
    );
  }
}

export default LaunchJob;
