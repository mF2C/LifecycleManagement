import React, { Component } from "react";
import request from "request";
import { Alert, Button, Dropdown, Badge } from 'react-bootstrap';
import vis from "vis-network";


class ServiceInstances extends Component {


  constructor(props, context) {
    super(props, context);

    this.state = {
      sel_service_instance: "",
      start_si_button: false,
      stop_si_button: false,
      delete_si_button: false,
      msg: "",
      msg_content: "",
      show_alert: false,
      show_info: false,
      sel_service_instance_id_1: "",
      total_service_instances_1: 0
    };

    this.handleView2 = this.handleView2.bind(this);
    this.handleStart = this.handleStart.bind(this);
    this.handleStop = this.handleStop.bind(this);
    this.handleDelete = this.handleDelete.bind(this);
  }


  checkSelectedItem_1(id_item) {
    if (id_item == null) {
      this.setState({ start_si_button: false, stop_si_button: false, delete_si_button: false });
    } else if (id_item.startsWith("service-instance/")) {
      this.setState({ start_si_button: true, stop_si_button: true, delete_si_button: true });
    } else {
      this.setState({ start_si_button: false, stop_si_button: false, delete_si_button: false });
    }

    this.parseItemId_1(id_item);
  }


  parseItemId_1(id_item) {
    if (id_item == null) {
      this.setState({sel_service_instance_id_1: ""});
    } else if (id_item.startsWith("service-instance/")) {
      var item_id = id_item.substring(17);
      this.setState({sel_service_instance_id_1: item_id});
    } else {
      this.setState({sel_service_instance_id_1: ""});
    }
  }


  displaySIAgents() {
    // call to api
    try {
      var that = this;
      request.get({url: global.rest_api_lm + 'service-instances/' + that.state.sel_service_instance_id_1}, function(err, resp, body) {
        if (err) {
          console.error(err);
          that.setState({ show_alert: true, msg: "GET /api/v2/lm/service-instances/" + that.state.sel_service_instance_id_1, msg_content: err.toString() });
        }
        else {
          if (resp.statusCode == 200) {
            console.log('Getting data service instances ... ok');
            if (global.debug) {
              that.setState({ show_info: true, msg: "GET /api/v2/lm/service-instances/" + that.state.sel_service_instance_id_1 + " => " + resp.statusCode, msg_content: "Service instances retrieved: response: " + body });
            }

            body = JSON.parse(body);
            console.log(body);

            ////////////////////////////////////////////////////////////////////////////
            if (body['service_instance'] != null && body['service_instance']['agents'].length > 0) {
              // create an array with nodes
              var nodes2 = new vis.DataSet([
                {id: body['service_instance']['id'], label: body['service_instance']['id'], image: './img/apps_mini.png', shape: 'image'}
              ]);

              var edges2 = new vis.DataSet([]);

              body['service_instance']['agents'].forEach(function(element) {
                nodes2.add({id: element['url'], label: element['url'], image: './img/node_mini.png', shape: 'image'});

                edges2.add({from: body['service_instance']['id'], to: element['url'], color:{color:'darkgreen'}, dashes: true});
              });

              // create a network2
              var container2 = document.getElementById('mynetwork');
              var data2 = {
                nodes: nodes2,
                edges: edges2
              };
              var options2 = {};
              var network2 = new vis.Network(container2, data2, options2);
            }
            ////////////////////////////////////////////////////////////////////////////
          }
          else {
            that.setState({ show_alert: true, msg: "GET /api/v2/lm/service-instances/all", msg_content: JSON.stringify(body) + " => " + resp.statusCode });
          }
        }
      });
    }
    catch(err) {
      console.error(err);
      this.setState({ show_alert: true, msg: "GET /api/v2/lm/service-instances/all", msg_content: err.toString() });
    }
  }


  handleView2(event) {
    console.log('Getting data service instances ...');
    // call to api
    try {
      var that = this;
      request.get({url: global.rest_api_lm + 'service-instances/all'}, function(err, resp, body) {
        if (err) {
          console.error(err);
          that.setState({ show_alert: true, msg: "GET /api/v2/lm/service-instances/all", msg_content: err.toString() });
        }
        else {
          if (resp.statusCode == 200) {
            console.log('Getting data service instances ... ok');
            if (global.debug) {
              that.setState({ show_info: true, msg: "GET /api/v2/lm/service-instances/all => " + resp.statusCode, msg_content: "Service instances retrieved: response: " + body });
            }

            body = JSON.parse(body);
            console.log(body);

            ////////////////////////////////////////////////////////////////////////////
            if (body['service_instances'] != null && body['service_instances'].length > 0) {
              // create an array with nodes
              var nodes2 = new vis.DataSet([
                {id: 'ag_1', label: 'local mF2C AGENT', image: './img/node_mini.png', shape: 'image'}
              ]);

              var edges2 = new vis.DataSet([]);

              body['service_instances'].forEach(function(element) {
                nodes2.add({id: element['id'], label: element['id'], image: './img/apps_mini.png', shape: 'image'});

                edges2.add({from: 'ag_1', to: element['id'], color:{color:'darkgreen'}, dashes: true});
              });

              // create a network2
              var container2 = document.getElementById('mynetwork2');
              var data2 = {
                nodes: nodes2,
                edges: edges2
              };
              var options2 = {};
              var network2 = new vis.Network(container2, data2, options2);

              that.setState({total_service_instances_1: body['service_instances'].length});

              // EVENTS
              network2.on("click", function (params) {
                  console.log('params returns: ' + params);
                  if (params != null) {
                    that.setState({ sel_service_instance_1: params.nodes[0] });
                    that.checkSelectedItem_1(params.nodes[0]);
                    that.displaySIAgents();
                  }
              });
            }
            ////////////////////////////////////////////////////////////////////////////
          }
          else {
            that.setState({ show_alert: true, msg: "GET /api/v2/lm/service-instances/all", msg_content: JSON.stringify(body) + " => " + resp.statusCode });
          }
        }
      });
    }
    catch(err) {
      console.error(err);
      this.setState({ show_alert: true, msg: "GET /api/v2/lm/service-instances/all", msg_content: err.toString() });
    }
  }


  componentDidMount() {
    this.handleView2(null)
  }


  handleStart(event) {
    console.log("Starting service instance [" + this.state.sel_service_instance_id_1 + "] ...");

  }


  handleStop(event) {
    console.log("Stopping service instance [" + this.state.sel_service_instance_id_1 + "] ...");

  }


  handleDelete(event) {
    console.log('Deleting service instance ...');
    // call to api
    var that = this;
    try {
      request.delete({url: global.rest_api_lm + 'service-instances/' + this.state.sel_service_instance_id_1}, function(err, resp, body) {
        if (err) {
          console.error(err);
          that.setState({ show_alert: true, msg: "DELETE /api/v2/lm/service-instances/" + that.state.sel_service_instance_id_1, msg_content: err.toString() });
        }
        else {
          console.log('Deleting service instance ... ok');
          if (global.debug) {
            that.setState({ show_info: true, msg: "DELETE /api/v2/lm/service-instances/" + that.state.sel_service_instance_id_1 + " => " + resp.statusCode, msg_content: "Service instance deleted: response: " + body });
          }
        }
      });
    }
    catch(err) {
      console.error(err);
      this.setState({ show_alert: true, msg: "GET /api/v2/um/sharing-model", msg_content: err.toString() });
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
        <h3><b>Service Instances</b></h3>
        <form>
          <div className="form-group row">
            <div className="col-sm-6">Service Instances managed by this agent <Badge variant="secondary">{this.state.total_service_instances_1}</Badge></div>
            <div className="col-sm-6">
              <Badge variant="secondary">selected service instance:</Badge>
              &nbsp;
              <Badge variant="primary">{this.state.sel_service_instance_id_1}</Badge>
            </div>
          </div>
          <div className="form-group row">
            <div id="mynetwork2"></div>
            <div id="mynetwork"></div>
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
              <button className="btn btn-primary" onClick={this.handleView2}>View</button>
              &nbsp;
              <button className="btn btn-success" onClick={this.handleStart} disabled={!this.state.start_si_button}>Start</button>
              &nbsp;
              <button className="btn btn-warning" onClick={this.handleStop} disabled={!this.state.stop_si_button}>Stop</button>
              &nbsp;
              <button className="btn btn-danger" onClick={this.handleDelete} disabled={!this.state.delete_si_button}>Delete</button>
            </div>
            <div className="col-sm-6">
            </div>
          </div>
        </form>
      </div>
    );
  }
}

export default ServiceInstances;
