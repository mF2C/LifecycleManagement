import React, { Component } from "react";
import request from "request";
import { Alert, Button, Badge, Spinner } from 'react-bootstrap';
import vis from "vis-network";


class LaunchJob extends Component {


  constructor(props, context) {
    super(props, context);

    this.state = {
      isLoading: false,
      total_service_instances_1: 0,
      sel_service_instance_id_1: "",
      job_def: "",
      start_si_button: false,
      report_si_button: false,
      cancel_si_button: false,
      msg: "",
      msg_content: "",
      show_alert: false,
      show_info: false,
      job_report: ""
    };

    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleView2 = this.handleView2.bind(this);
    this.viewReport = this.viewReport.bind(this);
    this.handleChange_job_def = this.handleChange_job_def.bind(this);
    this.handleCancel = this.handleCancel.bind(this);
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
   *
   */
  viewReport(event) {
    console.log("Getting report [service_instance=" + this.state.sel_service_instance_id_1 + "]  ...");
    // call to api
    try {
      var that = this;
      request.get({url: global.rest_api_lm + "service-instances/" + this.state.sel_service_instance_id_1 + "/report"}, function(err, resp, body) {
        if (err) {
          console.error(err);
          that.setState({ show_alert: true, msg: "GET /api/v2/lm/service-instances/" + this.state.sel_service_instance_id_1 + "/der", msg_content: err.toString() });
        }
        else {
          console.log('Getting report ... ok');
          if (global.debug) {
            //that.setState({ show_info: true, msg: "GET /api/v2/um/user-profile => " + resp.statusCode, msg_content: "User-profile retrieved: response: " + body });
          }
          try {
            console.log(body);
            that.setState({ job_report: body});
          }
          catch(err) {
            console.error(err);
          }
        }
      });
    }
    catch(err) {
      console.error(err);
      this.setState({ show_alert: true, msg: "GET /api/v2/lm/service-instances/_id_/report", msg_content: err.toString() });
    }
  }


  /**
   * Get service instance info
   */
  getSIinfo() {
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
            if (body['service_instance'] != null) {
              console.log(body['service_instance']);
              if (body['service_instance']['service_type'] == "compss") {
                that.setState({ start_si_button: true, report_si_button: true, cancel_si_button: true });
              } else {
                that.setState({ start_si_button: false, report_si_button: false, cancel_si_button: false });
              }
            }
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
              var total_compss_services = 0;

              body['service_instances'].forEach(function(element) {
                var ncolor = "white";
                if (element['status'] == "started") {
                  ncolor = "lightgreen";
                } else if (element['status'] == "error") {
                  ncolor = "lightred";
                }

                if (element['service_type'] == "compss") {
                  nodes2.add({id: element['id'], label: element['id'].substring(17), image: './img/apps_compss_mini.png', shape: 'circularImage',
                              font: {size:11, multi: true, color: ncolor}, level: 1});
                  edges2.add({from: 'ag_1', to: element['id'], color:{color:ncolor}, dashes: true});
                  total_compss_services++;
                } else {
                  nodes2.add({id: element['id'], label: element['id'], image: './img/apps_mini_disabled.png', shape: 'image',
                              font: {size:11, multi: true, color:"gray"}, level: 1});
                  edges2.add({from: 'ag_1', to: element['id'], color:{color:"gray"}, dashes: true});
                }
              });

              // create a network2
              var container2 = document.getElementById('mynetwork3');
              var data2 = {
                nodes: nodes2,
                edges: edges2
              };
              var options2 = {
                nodes: {
                  size:15
                }
              };
              var network2 = new vis.Network(container2, data2, options2);

              that.setState({total_service_instances_1: total_compss_services});

              // EVENTS
              network2.on("click", function (params) {
                  console.log('params returns: ' + params);
                  console.log(params);
                  if (params != null) {
                    that.setState({ sel_service_instance_1: params.nodes[0] });
                    that.parseItemId_1(params.nodes[0]);
                    if (that.state.sel_service_instance_id_1 != "") {
                      that.getSIinfo();
                    } else {
                      that.setState({ start_si_button: false, report_si_button: false, cancel_si_button: false });
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


  componentDidMount() {
    this.handleView2(null);
  }


  handleChange_job_def(event) {
    this.setState({job_def: event.target.value});
  }


  handleCancel(event) {
    this.setState({job_def: ""});
  }


  handleSubmit(event) {
    this.setState({isLoading: true});
    console.log("Launching job in DER [service_instance=" + this.state.sel_service_instance_id_1 + "] ...");

    // call to api
    try {
      var that = this;
      var formData = JSON.parse(this.state.job_def);

      request.put({url: global.rest_api_lm + 'service-instances/' + this.state.sel_service_instance_id_1 + "/der", json: formData}, function(err, resp, body) {
        if (err) {
          console.error(err);
          that.setState({ show_alert: true, msg: "PUT /api/v2/lm/service-instances/" + that.state.sel_service_instance_id_1 + "/der", msg_content: err.toString() });
        }
        else {
          console.log("Launching job in DER ... ok");
          if (resp.statusCode < 400) {
            that.setState({ show_info: true, msg: "PUT /api/v2/lm/service-instances/" + that.state.sel_service_instance_id_1 + "/der => " + resp.statusCode, msg_content: "Job launched: response: " + body });
          }
          else {
            that.setState({ show_alert: true, msg: "PUT /api/v2/lm/service-instances/" + that.state.sel_service_instance_id_1 + "/der => ERROR CODE: " + resp.statusCode, msg_content: "Could not launch job" });
          }
        }

        that.setState({isLoading: false});
      });
    }
    catch(err) {
      console.error(err);
      this.setState({ show_alert: true, msg: "PUT /api/v2/lm/service-instances/_id_/der", msg_content: err.toString(), isLoading: false });
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
        <h3><b>DER Jobs</b>&nbsp;&nbsp;&nbsp;
          {this.state.isLoading ?
            <Spinner animation="border" role="status" variant="primary">
              <span className="sr-only">Loading...</span>
            </Spinner> : ""}
        </h3>
        <form>
          <div className="form-group row">
            <div className="col-sm-6">
              DER instances managed by this agent <Badge variant="secondary">{this.state.total_service_instances_1}</Badge>
            </div>
            <div className="col-sm-6">Select a DER instance and launch a job</div>
          </div>

          <div className="form-group row">
            <div className="col-sm-6">
              <div id="mynetwork3"></div>
            </div>

            <div className="col-sm-6">
              <div className="form-group row">
                <div className="col-sm-11">
                  <input type="text" className="form-control" id="service" value={this.state.sel_service_instance_id_1} readOnly/>
                </div>
              </div>

              <div className="form-group row">
                <div className="col-sm-11">
                  <textarea className="form-control" id="job" rows="10" value={this.state.job_def} onChange={this.handleChange_job_def}>
                  </textarea>
                </div>
              </div>

              <button type="submit" value="Submit" className="btn btn-success" onClick={this.handleSubmit} disabled={!this.state.start_si_button}>
                <i class="fa fa-rocket" aria-hidden="true"></i>&nbsp;Launch
              </button>
              &nbsp;
              <button className="btn btn-warning" disabled={!this.state.cancel_si_button} onClick={this.handleCancel}><i class="fa fa-times" aria-hidden="true"></i>&nbsp;Cancel</button>
            </div>
          </div>

          <div className="form-group row">
            <div className="col-sm-12">
              <Button variant="primary" onClick={this.viewReport} disabled={!this.state.report_si_button}>
                <i class="fa fa-search" aria-hidden="true"></i>&nbsp;View report
              </Button>
              <textarea className="form-control" id="result" rows="3" value={this.state.job_report}/>
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
