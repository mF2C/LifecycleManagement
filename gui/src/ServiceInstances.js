import React, { Component } from "react";

import vis from "vis-network";


class ServiceInstances extends Component {


  constructor(props, context) {
    super(props, context);

    this.state = {
      selserviceinstance: "",
    };

    this.handleView = this.handleView.bind(this);
    this.handleView2 = this.handleView2.bind(this);
    this.handleStart = this.handleStart.bind(this);
    this.handleStop = this.handleStop.bind(this);
    this.handleDelete = this.handleDelete.bind(this);
  }


  componentDidMount() {
    ////////////////////////////////////////////////////////////////////////////
    // create an array with nodes
    var nodes = new vis.DataSet([
      {id: 'ag_1', label: 'local mF2C AGENT', image: './img/node_mini.png', shape: 'image', title: 'mF2C agent'},
      {id: 'ag_2', label: '192.168.1.21', image: './img/node_mini.png', shape: 'image', title: 'mF2C agent'},
      {id: 'ag_3', label: '192.168.1.25', image: './img/node_mini.png', shape: 'image', title: 'mF2C agent'},
      {id: 'ag_4', label: '192.168.1.26', image: './img/node_mini.png', shape: 'image', title: 'mF2C agent'},
      {id: 'si_1_1', label: 'Service Instance 1', image: 'img/apps_mini.png', shape: 'image', title: 'service instance'},
      {id: 'si_1_2', label: 'Service Instance 1', image: 'img/apps_mini.png', shape: 'image', title: 'service instance'},
      {id: 'si_1_3', label: 'Service Instance 1', image: 'img/apps_mini.png', shape: 'image', title: 'service instance'},
      {id: 'si_2_1', label: 'Service Instance 2', image: './img/apps_mini.png', shape: 'image', title: 'service instance'},
      {id: 'si_2_2', label: 'Service Instance 2', image: './img/apps_mini.png', shape: 'image', title: 'service instance'}
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

    // EVENTS
    network.on("click", function (params) {
        params.event = "[original event]";
        document.getElementById('eventSpan').innerHTML = '<h2>Click event:</h2>' + JSON.stringify(params, null, 4);
        console.log('click event, getNodeAt returns: ' + this.getNodeAt(params.pointer.DOM));
    });

    network.on("hoverNode", function (params) {
        console.log('hoverNode Event:', params);
    });

    network.on("showPopup", function (params) {
        console.log('params returns: ' + params);
        document.getElementById('eventSpan').innerHTML = '<h2>showPopup event: </h2>' + JSON.stringify(params, null, 4);
    });

    ////////////////////////////////////////////////////////////////////////////
    // create an array with nodes
    var nodes2 = new vis.DataSet([
      {id: 'ag_1', label: 'local mF2C AGENT', image: './img/node_mini.png', shape: 'image'},
      {id: 'si_1', label: 'Service Instance 1', image: 'img/apps_mini.png', shape: 'image'},
      {id: 'si_2', label: 'Service Instance 2', image: './img/apps_mini.png', shape: 'image'},
      {id: 'si_3', label: 'Service Instance 3', image: './img/apps_mini.png', shape: 'image'},
      {id: 'si_4', label: 'Service Instance 4', image: './img/apps_mini.png', shape: 'image'}
    ]);

    // create an array with edges
    var edges2 = new vis.DataSet([
      {from: 'ag_1', to: 'si_1', color:{color:'darkgreen'}, dashes: true},
      {from: 'ag_1', to: 'si_2', color:{color:'darkgreen'}, dashes: true},
      {from: 'ag_1', to: 'si_3', color:{color:'darkgreen'}, dashes: true},
      {from: 'ag_1', to: 'si_4', color:{color:'darkgreen'}, dashes: true}
    ]);

    // create a network2
    var container2 = document.getElementById('mynetwork2');
    var data2 = {
      nodes: nodes2,
      edges: edges2
    };
    var options2 = {};
    var network2 = new vis.Network(container2, data2, options2);
  }


  handleView(event) {
    alert('handleView');
    event.preventDefault();
  }


  handleStart(event) {
    alert('handleStart');
    event.preventDefault();
  }


  handleStop(event) {
    alert('handleStop');
    event.preventDefault();
  }


  handleDelete(event) {
    alert('handleDelete');
    event.preventDefault();
  }


  handleView2(event) {
    alert('handleView2');
    event.preventDefault();
  }

  render() {
    return (
      <div>
        <h2>Service Instances</h2>
        <form>
          <div className="form-group row">
            <div className="col-sm-6">Service Instances launched by this agent</div>
            <div className="col-sm-6">Service Instances running in this agent</div>
          </div>
          <div className="form-group row">
            <pre id="eventSpan"></pre>
          </div>
          <div className="form-group row">
            <div id="mynetwork"></div>
            <div id="mynetwork2"></div>
          </div>
          <div className="form-group row">
            <div className="col-sm-6">
              <button className="btn btn-primary" onClick={this.handleView}>View</button>
              <button className="btn btn-success" onClick={this.handleStart}>Start</button>
              <button className="btn btn-warning" onClick={this.handleStop}>Stop</button>
              <button className="btn btn-danger" onClick={this.handleDelete}>Delete</button>
            </div>
            <div className="col-sm-6">
              <button className="btn btn-primary" onClick={this.handleView2}>View</button>
            </div>
          </div>
        </form>
      </div>
    );
  }
}

export default ServiceInstances;
