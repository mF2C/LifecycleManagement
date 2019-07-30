import React, { Component } from "react";
import request from "request";
import { Alert, Button, Dropdown, Badge } from 'react-bootstrap';
import vis from "vis-network";


class ServiceInstances extends Component {


  constructor(props, context) {
    super(props, context);

    this.state = {
      sel_service_instance: "",
      sel_service_instance_id: "",
      start_si_button: false,
      stop_si_button: false,
      delete_si_button: false,
      msg: "",
      msg_content: "",
      show_alert: false,
      show_info: false
    };

    this.handleView = this.handleView.bind(this);
    this.handleView2 = this.handleView2.bind(this);
    this.handleStart = this.handleStart.bind(this);
    this.handleStop = this.handleStop.bind(this);
    this.handleDelete = this.handleDelete.bind(this);
  }


  checkSelectedItem(id_item) {
    if (id_item == null) {
      this.setState({ start_si_button: false, stop_si_button: false, delete_si_button: false });
    } else if (id_item.startsWith("si_")) {
      this.setState({ start_si_button: true, stop_si_button: true, delete_si_button: true });
    } else {
      this.setState({ start_si_button: false, stop_si_button: false, delete_si_button: false });
    }

    this.parseItemId(id_item);
  }


  parseItemId(id_item) {
    if (id_item == null) {
      this.setState({sel_service_instance_id: ""});
    } else if (id_item.startsWith("si_")) {
      var item_id = id_item.substring(3);
      var pos_f = item_id.indexOf("_");
      item_id = item_id.substring(0, pos_f);
      this.setState({sel_service_instance_id: item_id});
    } else {
      this.setState({sel_service_instance_id: ""});
    }
  }


  componentDidMount() {
    var uri = "/api/v2/lm/";
    // call to api
    try {
      request.get(uri)
        .on('response', function(response) {
          console.log(response.statusCode); // 200
          this.setState({ show_info: true });
          this.setState({ msg: "GET " + uri + " : " + response.statusCode });
          this.setState({ msg_content: "Response: " + response.toString() });
        })
        .on('error', function(err) {
          console.error(err);
          this.setState({ show_alert: true });
          this.setState({ msg: "GET " + uri });
          this.setState({ msg_content: err.toString() });
        })
    }
    catch(err) {
      console.error(err);
      this.setState({ show_alert: true });
      this.setState({ msg: "GET " + uri });
      this.setState({ msg_content: err.toString() });
    }

    ////////////////////////////////////////////////////////////////////////////
    // create an array with nodes
    var nodes = new vis.DataSet([
      {id: 'ag_1', label: 'local mF2C AGENT', image: './img/node_mini.png', shape: 'image', title: 'mF2C agent'},
      {id: 'ag_2', label: '192.168.1.21', image: './img/node_mini.png', shape: 'image', title: 'mF2C agent'},
      {id: 'ag_3', label: '192.168.1.25', image: './img/node_mini.png', shape: 'image', title: 'mF2C agent'},
      {id: 'ag_4', label: '192.168.1.26', image: './img/node_mini.png', shape: 'image', title: 'mF2C agent'},
      {id: 'si_a0fdd615-e5a5-4716-8612-7b4f78d090bf_1', label: 'Service Instance 1', image: 'img/apps_mini.png', shape: 'image', title: 'service instance'},
      {id: 'si_a0fdd615-e5a5-4716-8612-7b4f78d090bf_2', label: 'Service Instance 1', image: 'img/apps_mini.png', shape: 'image', title: 'service instance'},
      {id: 'si_a0fdd615-e5a5-4716-8612-7b4f78d090bf_3', label: 'Service Instance 1', image: 'img/apps_mini.png', shape: 'image', title: 'service instance'},
      {id: 'si_fffdd615-e5a5-4716-8612-7b4f78d09aaa_1', label: 'Service Instance 2', image: './img/apps_mini.png', shape: 'image', title: 'service instance'},
      {id: 'si_fffdd615-e5a5-4716-8612-7b4f78d09aaa_2', label: 'Service Instance 2', image: './img/apps_mini.png', shape: 'image', title: 'service instance'}
    ]);

    // create an array with edges
    var edges = new vis.DataSet([
      {from: 'ag_1', to: 'ag_2', dashes: true, color:{color:'#111111'}},
      {from: 'ag_1', to: 'ag_3', dashes: true, color:{color:'#111111'}},
      {from: 'ag_1', to: 'ag_4', dashes: true, color:{color:'#111111'}},
      {from: 'ag_1', to: 'si_a0fdd615-e5a5-4716-8612-7b4f78d090bf_1', color:{color:'darkgreen'}},
      {from: 'ag_1', to: 'si_fffdd615-e5a5-4716-8612-7b4f78d09aaa_1', color:{color:'darkgreen'}},
      {from: 'ag_2', to: 'si_a0fdd615-e5a5-4716-8612-7b4f78d090bf_2', color:{color:'darkgreen'}},
      {from: 'ag_3', to: 'si_a0fdd615-e5a5-4716-8612-7b4f78d090bf_3', color:{color:'darkgreen'}},
      {from: 'ag_4', to: 'si_fffdd615-e5a5-4716-8612-7b4f78d09aaa_2', color:{color:'darkgreen'}}
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
    var that = this;
    network.on("click", function (params) {
        console.log('params returns: ' + params);
        if (params != null) {
          that.setState({ sel_service_instance: params.nodes[0] });
          that.checkSelectedItem(params.nodes[0]);
        }
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
    //event.preventDefault();
    console.log('Updating instances graph ...');

    var uri = "/api/v2/lm/";
    // call to api
    try {
      request.get(uri)
        .on('response', function(response) {
          console.log(response.statusCode); // 200
          this.setState({ show_info: true });
          this.setState({ msg: "GET " + uri + " : " + response.statusCode });
          this.setState({ msg_content: "Response: " + response.toString() });
        })
        .on('error', function(err) {
          console.error(err);
          this.setState({ show_alert: true });
          this.setState({ msg: "GET " + uri });
          this.setState({ msg_content: err.toString() });
        })
    }
    catch(err) {
      console.error(err);
      this.setState({ show_alert: true });
      this.setState({ msg: "GET " + uri });
      this.setState({ msg_content: err.toString() });
    }
  }


  handleStart(event) {
    //event.preventDefault();
    console.log("Starting service instance [" + this.state.sel_service_instance_id + "] ...");

    var uri = "/api/v2/lm/" + this.state.sel_service_instance_id;
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


  handleStop(event) {
    //event.preventDefault();
    console.log("Stopping service instance [" + this.state.sel_service_instance_id + "] ...");

    var uri = "/api/v2/lm/" + this.state.sel_service_instance_id;
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


  handleDelete(event) {
    //event.preventDefault();
    console.log("Terminating service instance [" + this.state.sel_service_instance_id + "] ...");

    var uri = "/api/v2/lm/" + this.state.sel_service_instance_id;
    // call to api
    try {
      request.delete(uri)
        .on('response', function(response) {
          console.log(response.statusCode); // 200
          this.setState({ show_info: true });
          this.setState({ msg: "DELETE " + uri + " : " + response.statusCode });
          this.setState({ msg_content: "Response: " + response.toString() });
        })
        .on('error', function(err) {
          console.error(err);
          this.setState({ show_alert: true });
          this.setState({ msg: "DELETE " + uri });
          this.setState({ msg_content: err.toString() });
        })
    }
    catch(err) {
      console.error(err);
      this.setState({ show_alert: true });
      this.setState({ msg: "DELETE " + uri });
      this.setState({ msg_content: err.toString() });
    }
  }


  handleView2(event) {
    //event.preventDefault();
    console.log('Updating instances graph ...');

    var uri = "/api/v2/lm/";
    // call to api
    try {
      request.get(uri)
        .on('response', function(response) {
          console.log(response.statusCode); // 200
          this.setState({ show_info: true });
          this.setState({ msg: "GET " + uri + " : " + response.statusCode });
          this.setState({ msg_content: "Response: " + response.toString() });
        })
        .on('error', function(err) {
          console.error(err);
          this.setState({ show_alert: true });
          this.setState({ msg: "GET " + uri });
          this.setState({ msg_content: err.toString() });
        })
    }
    catch(err) {
      console.error(err);
      this.setState({ show_alert: true });
      this.setState({ msg: "GET " + uri });
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
        <h3><b>Service Instances</b></h3>
        <form>
          <div className="form-group row">
            <div className="col-sm-6">
              Service Instances launched by this agent

            </div>
            <div className="col-sm-6">Service Instances running in this agent</div>
          </div>
          <div className="form-group row">
            <div id="mynetwork"></div>
            <div id="mynetwork2"></div>
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

          <div className="form-group row">
            <div className="col-sm-6">
              <Badge variant="secondary">selected service instance:</Badge>
              &nbsp;
              <Badge variant="primary">{this.state.sel_service_instance_id}</Badge>
            </div>
          </div>
          <div className="form-group row">
            <div className="col-sm-6">
              <button className="btn btn-primary" onClick={this.handleView}>View</button>
              &nbsp;
              <button className="btn btn-success" onClick={this.handleStart} disabled={!this.state.start_si_button}>Start</button>
              &nbsp;
              <button className="btn btn-warning" onClick={this.handleStop} disabled={!this.state.stop_si_button}>Stop</button>
              &nbsp;
              <button className="btn btn-danger" onClick={this.handleDelete} disabled={!this.state.delete_si_button}>Delete</button>
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
