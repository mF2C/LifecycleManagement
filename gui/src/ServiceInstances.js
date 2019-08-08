import React, { Component } from "react";
import request from "request";
import { Alert, Button, Badge, Form, Row, Col, Spinner, Tooltip, Modal } from 'react-bootstrap';
import vis from "vis-network";


class ServiceInstances extends Component {


  constructor(props, context) {
    super(props, context);

    this.state = {
      sel_service_instance: "",
      isLoading: false,
      start_si_button: false,
      isStarting: false,
      stop_si_button: false,
      isStopping: false,
      delete_si_button: false,
      isDeleting: false,
      msg: "",
      msg_content: "",
      show_alert: false,
      show_info: false,
      sel_service_instance_id_1: "",
      total_service_instances_1: 0,
      img_icon_service_type: "img/apps_mini.png",
      // service instance
      si_id: "",
      si_status: "",
      si_created: "",
      si_service: "",
      si_agreement: "",
      si_type: "",
      si_agents: "",
      // Modal
      show: false,
      service_instance_json: "{}"
    };

    this.handleView2 = this.handleView2.bind(this);
    this.handleStart = this.handleStart.bind(this);
    this.handleStop = this.handleStop.bind(this);
    this.handleDelete = this.handleDelete.bind(this);
    this.handleShow = this.handleShow.bind(this);
    this.handleClose = this.handleClose.bind(this);
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


  /**
   * Display agents running the selected service instance
   */
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
              //that.setState({ show_info: true, msg: "GET /api/v2/lm/service-instances/" + that.state.sel_service_instance_id_1 + " => " + resp.statusCode, msg_content: "Service instances retrieved: response: " + body });
            }

            body = JSON.parse(body);
            console.log(body);

            ////////////////////////////////////////////////////////////////////////////
            // FORM
            if (body['service_instance'] != null) {
              // service instance
              that.setState({si_id: body['service_instance']['id'],
                             si_status: body['service_instance']['status'],
                             si_created: body['service_instance']['created'],
                             si_service: body['service_instance']['service'],
                             si_agreement: body['service_instance']['agreement'],
                             si_type: body['service_instance']['service_type']});

              if (body['service_instance']['agents'] != null) {
                that.setState({si_agents: body['service_instance']['agents'].length});
              }

              if (body['service_instance']['service_type'] != null) {
                if (body['service_instance']['service_type'] == "docker") {
                  that.setState({img_icon_service_type: "img/docker-logo.png"});
                } else if (body['service_instance']['service_type'] == "docker-swarm") {
                  that.setState({img_icon_service_type: "img/docker-swarm-logo.png"});
                } else if (body['service_instance']['service_type'] == "compss") {
                  that.setState({img_icon_service_type: "img/compss-logo.png"});
                } else if (body['service_instance']['service_type'] == "docker-compose") {
                  that.setState({img_icon_service_type: "img/docker-compose-logo.png"});
                } else {
                  that.setState({img_icon_service_type: "img/apps_mini.png"});
                }
              }
            }

            ////////////////////////////////////////////////////////////////////////////
            if (body['service_instance'] != null && body['service_instance']['agents'] != null && body['service_instance']['agents'].length > 0) {
              // create an array with nodes
              var app_icon = "./img/apps_mini.png";
              if (body['service_instance']['status'] == "started") {
                app_icon = "./img/apps_started_mini.png";
              }

              var nodes2 = new vis.DataSet([
                {id: body['service_instance']['id'], label: body['service_instance']['id'].substring(17), image: app_icon, shape: 'image'}
              ]);

              var edges2 = new vis.DataSet([]);

              body['service_instance']['agents'].forEach(function(element) {
                nodes2.add({id: element['url'], label: element['url'], image: './img/node_mini.png', shape: 'circularImage'});

                edges2.add({from: body['service_instance']['id'], to: element['url'], color:{color:'white'}, dashes: true});
              });

              // create a network2
              var container2 = document.getElementById('mynetwork');
              var data2 = {
                nodes: nodes2,
                edges: edges2
              };
              var options2 = {
                nodes: {
                  size:15,
                  font:{color:'#ffffff', size:10}
                },
                edges: {
                  color: 'lightgray'
                }
              };
              var network2 = new vis.Network(container2, data2, options2);

              that.setState({ service_instance_json: JSON.stringify(body, null, "\t") });
            }
            ////////////////////////////////////////////////////////////////////////////
          }
          else {
            that.setState({ show_alert: true, msg: "GET /api/v2/lm/service-instances/all",
                            msg_content: JSON.stringify(body) + " => " + resp.statusCode, service_instance_json: "{}" });
          }
        }
      });
    }
    catch(err) {
      console.error(err);
      this.setState({ show_alert: true, msg: "GET /api/v2/lm/service-instances/all", msg_content: err.toString() });
    }
  }


  /**
   * Load initial graph with all service instances managed by the agent
   */
  handleView2(event) {
    this.setState({isLoading: true});
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
              //that.setState({ show_info: true, msg: "GET /api/v2/lm/service-instances/all => " + resp.statusCode, msg_content: "Service instances retrieved: response: " + body });
            }

            body = JSON.parse(body);
            console.log(body);

            ////////////////////////////////////////////////////////////////////////////
            if (body['service_instances'] != null && body['service_instances'].length > 0) {
              // create an array with nodes
              var nodes2 = new vis.DataSet([
                {id: 'ag_1', label: "<b>mf2c agent</b>", image: './img/node_mini.png', shape: 'image', title: "local mF2C agent",
                 font: {size:13, multi: true, color: "black", strokeWidth:2, strokeColor: "#dddddd"}, level: 0}
              ]);

              var edges2 = new vis.DataSet([]);

              body['service_instances'].forEach(function(element) {
                var ncolor = "white";
                if (element['status'] == "started") {
                  ncolor = "lightgreen";
                } else if (element['status'] == "error") {
                  ncolor = "lightred";
                }

                if (element['service_type'] == "docker") {
                  nodes2.add({id: element['id'], label: element['id'].substring(17), image: './img/apps_docker_mini.png', shape: 'circularImage',
                              font: {size:11, multi: true, color: ncolor}, level: 1});
                } else if (element['service_type'] == "docker-swarm") {
                  nodes2.add({id: element['id'], label: element['id'].substring(17), image: './img/apps_docker_swarm_mini.png', shape: 'circularImage',
                              font: {size:11, multi: true, color: ncolor}, level: 1});
                } else if (element['service_type'] == "docker-compose") {
                  nodes2.add({id: element['id'], label: element['id'].substring(17), image: './img/apps_docker_compose_mini.png', shape: 'circularImage',
                              font: {size:11, multi: true, color: ncolor}, level: 1});
                } else if (element['service_type'] == "compss") {
                  nodes2.add({id: element['id'], label: element['id'].substring(17), image: './img/apps_compss_mini.png', shape: 'circularImage',
                              font: {size:11, multi: true, color: ncolor}, level: 1});
                } else {
                  nodes2.add({id: element['id'], label: element['id'], image: './img/apps_mini.png', shape: 'circularImage',
                              font: {size:11, multi: true, color: ncolor}, level: 1});
                }

                if (element['status'] == "started") {
                  edges2.add({from: 'ag_1', to: element['id'], color:{color:"lightgreen"}, dashes: true});
                } else if (element['status'] == "error") {
                  edges2.add({from: 'ag_1', to: element['id'], color:{color:"lightred"}, dashes: true});
                } else {
                  edges2.add({from: 'ag_1', to: element['id'], color:{color:"white"}, dashes: [2,2,10,10]});
                }
              });

              // create a network2
              var container2 = document.getElementById('mynetwork2');
              var data2 = {
                nodes: nodes2,
                edges: edges2
              };
              var options2 = {
                nodes: {
                  size:20
                },
                edges: {
                  color: 'lightgray'
                }
              };
              var network2 = new vis.Network(container2, data2, options2);

              that.setState({total_service_instances_1: body['service_instances'].length});

              // EVENTS
              network2.on("click", function (params) {
                  console.log('params returns: ' + params);
                  if (params != null) {
                    that.setState({ sel_service_instance_1: params.nodes[0] });
                    that.checkSelectedItem_1(params.nodes[0]);
                    if (that.state.sel_service_instance_id_1 != "") {
                      that.displaySIAgents();
                    } else {
                      // service instance
                      that.setState({si_id: "",
                                     si_status: "",
                                     si_created: "",
                                     si_service: "",
                                     si_agreement: "",
                                     si_type: "",
                                     si_agents: "",
                                     img_icon_service_type: "img/apps_mini.png",
                                     service_instance_json: "{}"});
                    }
                  }
              });
            }
            ////////////////////////////////////////////////////////////////////////////
          }
          else {
            that.setState({ show_alert: true, msg: "GET /api/v2/lm/service-instances/all", msg_content: JSON.stringify(body) + " => " + resp.statusCode });
          }
        }

        that.setState({isLoading: false});
      });
    }
    catch(err) {
      console.error(err);
      this.setState({ show_alert: true, msg: "GET /api/v2/lm/service-instances/all", msg_content: err.toString(), isLoading: false });
    }
  }


  /**
   * after components are ready: load graph
   */
  componentDidMount() {
    this.handleView2(null);
  }


  // sleep
  sleep(milliseconds) {
    var start = new Date().getTime();
    for (var i = 0; i < 1e7; i++) {
      if ((new Date().getTime() - start) > milliseconds){
        break;
      }
    }
  }


  // start service instance
  handleStart(event) {
    this.setState({isStarting: true});
    console.log("Starting service instance [" + this.state.sel_service_instance_id_1 + "] ...");
    // call to api
    try {
      var that = this;
      var formData = {
        operation: "start"
      };
      request.put({url: global.rest_api_lm + 'service-instances/' + this.state.sel_service_instance_id_1, json: formData}, function(err, resp, body) {
        if (err) {
          console.error(err);
          that.setState({ show_alert: true, msg: "PUT /api/v2/lm/service-instances/" + that.state.sel_service_instance_id_1, msg_content: err.toString() });
        }
        else {
          console.log("Starting service instance ... ok");
          if (global.debug) {
            that.setState({ show_info: true, msg: "PUT /api/v2/lm/service-instances/" + that.state.sel_service_instance_id_1 + " => " + resp.statusCode, msg_content: "Service instance deleted: response: " + body });
          }
          that.sleep(5000);
          that.handleView2(null);
          that.displaySIAgents();
        }

        that.setState({isStarting: false});
      });
    }
    catch(err) {
      console.error(err);
      this.setState({ show_alert: true, msg: "GET /api/v2/um/sharing-model", msg_content: err.toString(), isStarting: false });
    }
  }


  // stop service instance
  handleStop(event) {
    this.setState({isStopping: true});
    console.log("Stopping service instance [" + this.state.sel_service_instance_id_1 + "] ...");
    // call to api
    try {
      var that = this;
      var formData = {
        operation: "stop"
      };
      request.put({url: global.rest_api_lm + 'service-instances/' + this.state.sel_service_instance_id_1, json: formData}, function(err, resp, body) {
        if (err) {
          console.error(err);
          that.setState({ show_alert: true, msg: "PUT /api/v2/lm/service-instances/" + that.state.sel_service_instance_id_1, msg_content: err.toString() });
        }
        else {
          console.log("Stopping service instance ... ok");
          if (global.debug) {
            that.setState({ show_info: true, msg: "PUT /api/v2/lm/service-instances/" + that.state.sel_service_instance_id_1 + " => " + resp.statusCode, msg_content: "Service instance deleted: response: " + body });
          }
          that.sleep(5000);
          that.handleView2(null);
          that.displaySIAgents();
        }

        that.setState({isStopping: false});
      });
    }
    catch(err) {
      console.error(err);
      this.setState({ show_alert: true, msg: "GET /api/v2/um/sharing-model", msg_content: err.toString(), isStopping: false});
    }
  }


  // delete service instance
  handleDelete(event) {
    this.setState({isDeleting: true});
    console.log("Deleting service instance [" + this.state.sel_service_instance_id_1 + "] ...");
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
          that.sleep(5000);
          that.handleView2(null);
          // service instance
          that.setState({si_id: "",
                         si_status: "",
                         si_created: "",
                         si_service: "",
                         si_agreement: "",
                         si_type: "",
                         si_agents: "",
                         img_icon_service_type: "img/apps_mini.png",
                         service_instance_json: "{}"});
        }

        that.setState({isDeleting: false});
      });
    }
    catch(err) {
      console.error(err);
      this.setState({ show_alert: true, msg: "GET /api/v2/um/sharing-model", msg_content: err.toString(), isDeleting: false});
    }
  }


  handleClose(event) {
    this.setState({show: false});
  }


  handleShow(event) {
    this.setState({show: true});
  }


  // alert messages
  onDismiss() {
    this.setState({ show_alert: false });
    this.setState({ show_info: false });
    this.setState({ msg: "" });
    this.setState({ msg_content: "" });
  }


  /**
   * render component
   */
  render() {
    return (
      <div style={{margin: "25px 0px 0px 0px"}}>
        <h3><b>Service Instances</b>&nbsp;&nbsp;&nbsp;
          {this.state.isLoading ?
            <Spinner animation="border" role="status" variant="primary">
              <span className="sr-only">Loading...</span>
            </Spinner> : ""}
        </h3>
        <form>
          <div className="form-group row">
            <div className="col-sm-6">Service Instances managed by this agent <Badge variant="secondary">{this.state.total_service_instances_1}</Badge></div>
            <div className="col-sm-6">
              <img src={this.state.img_icon_service_type} alt="service type" height="25" width="25" />
              &nbsp;&nbsp;
              <Badge variant="info" onClick={this.handleShow}>{this.state.sel_service_instance_id_1}</Badge>
            </div>
          </div>

          <div className="form-group row">
            <div className="col-sm-6">
              <div id="mynetwork2"></div>

              <Button variant="primary" onClick={this.handleView2} disabled={this.state.isLoading}>
                <i class="fa fa-search" aria-hidden="true"></i>&nbsp;
                {this.state.isLoading ? "Loading ..." : "View"}
              </Button>
              &nbsp;
              <Button variant="success" onClick={this.handleStart} disabled={!this.state.start_si_button && !this.state.isStarting}>
                <i class="fa fa-rocket" aria-hidden="true"></i>&nbsp;
                {this.state.isStarting ? "Starting ..." : "Start"}
              </Button>
              &nbsp;
              <Button variant="warning" onClick={this.handleStop} disabled={!this.state.stop_si_button && !this.state.isStopping}>
                <i class="fa fa-hand-paper-o" aria-hidden="true"></i>&nbsp;
                {this.state.isStopping ? "Stopping ..." : "Stop"}
              </Button>
              &nbsp;
              <Button variant="danger" onClick={this.handleDelete} disabled={!this.state.delete_si_button && !this.state.isDeleting}>
                <i class="fa fa-trash" aria-hidden="true"></i>&nbsp;
                {this.state.isDeleting ? "Deleting ..." : "Delete"}
              </Button>
            </div>

            <div className="col-sm-6">
              <div id="mynetwork"></div>

              <Form style={{margin: "10px 0px 0px 15px"}}>
                <Form.Group as={Row}>
                  <Form.Text size="sm" column  className="col-sm-2">Id</Form.Text>
                  <Col sm={8}>
                    <Form.Control size="sm" placeholder="id" value={this.state.si_id}
                     style={{ backgroundColor: "#FFFFFC" }} disabled/>
                  </Col>
                </Form.Group>
                <Form.Group as={Row}>
                  <Form.Text size="sm" column  className="col-sm-2">Status</Form.Text>
                  <Col sm={6}>
                    <Form.Control size="sm" placeholder="status" value={this.state.si_status}
                     style={{ backgroundColor: "#EEEEEE"}} disabled/>
                  </Col>
                </Form.Group>
                <Form.Group as={Row}>
                  <Form.Text size="sm" column  className="col-sm-2">Created</Form.Text>
                  <Col sm={6}>
                    <Form.Control size="sm" placeholder="created" value={this.state.si_created}
                     style={{ backgroundColor: "#EEEEEE" }} disabled/>
                  </Col>
                </Form.Group>
                <Form.Group as={Row}>
                  <Form.Text size="sm" column  className="col-sm-2">Service</Form.Text>
                  <Col sm={8}>
                    <Form.Control size="sm" placeholder="service id" value={this.state.si_service}
                     style={{ backgroundColor: "#FFFFFC" }} disabled/>
                  </Col>
                </Form.Group>
                <Form.Group as={Row}>
                  <Form.Text size="sm" column className="col-sm-2">Agreement</Form.Text>
                  <Col sm={8}>
                    <Form.Control size="sm" placeholder="agreement id" value={this.state.si_agreement}
                     style={{ backgroundColor: "#FFFFFC" }} disabled/>
                  </Col>
                </Form.Group>
                <Form.Group as={Row}>
                  <Form.Text size="sm" column  className="col-sm-2">Type</Form.Text>
                  <Col sm={3}>
                    <Form.Control size="sm" placeholder="service type" value={this.state.si_type}
                     style={{ backgroundColor: "#EEEEEE" }} disabled/>
                  </Col>
                </Form.Group>
                <Form.Group as={Row}>
                  <Form.Text size="sm" column  className="col-sm-2">Agents</Form.Text>
                  <Col sm={3}>
                    <Form.Control size="sm" placeholder="agents" value={this.state.si_agents}
                     style={{ backgroundColor: "#EEEEEE" }} disabled/>
                  </Col>
                </Form.Group>
              </Form>
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

        <Modal show={this.state.show} onHide={this.handleClose} size="lg">
          <Modal.Header closeButton>
            <Modal.Title>Service Instance (JSON)</Modal.Title>
          </Modal.Header>
          <Modal.Body>{this.state.service_instance_json}</Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={this.handleClose}>
              Close
            </Button>
          </Modal.Footer>
        </Modal>
      </div>
    );
  }
}

export default ServiceInstances;
