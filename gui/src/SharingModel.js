import React, { Component } from "react";
import request from "request";
import { Alert, Button, Badge, Spinner, OverlayTrigger, Tooltip } from 'react-bootstrap';


class SharingModel extends Component {


  constructor(props, context) {
    super(props, context);

    this.state = {
      isLoading: false,
      msg: "",
      msg_content: "",
      show_alert: false,
      show_info: false,
      // sharing model properties
      gps: "",
      id_sharing_model: "",
      max_cpu: 0,
      max_mem: 0,
      max_sto: 0,
      max_ban: 0,
      bat_lev: 0,
      gps_allowed: false,
      max_apps: 0
    };

    this.handleView = this.handleView.bind(this);
    this.handleSave = this.handleSave.bind(this);
    this.onDismiss = this.onDismiss.bind(this);
    this.handleChange_max_cpu = this.handleChange_max_cpu.bind(this);
    this.handleChange_max_mem = this.handleChange_max_mem.bind(this);
    this.handleChange_max_sto = this.handleChange_max_sto.bind(this);
    this.handleChange_max_ban = this.handleChange_max_ban.bind(this);
    this.handleChange_bat_lev = this.handleChange_bat_lev.bind(this);
    this.handleChange_gps_allowed = this.handleChange_gps_allowed.bind(this);
    this.handleChange_max_apps = this.handleChange_max_apps.bind(this);
    this.checkNumber = this.checkNumber.bind(this);
  }


  componentDidMount() {
    this.handleView(null);
  }


  handleChange_max_cpu(event) {
    this.setState({max_cpu: event.target.value});
  }


  handleChange_max_mem(event) {
    this.setState({max_mem: event.target.value});
  }


  handleChange_max_sto(event) {
    this.setState({max_sto: event.target.value});
  }


  handleChange_max_ban(event) {
    this.setState({max_ban: event.target.value});
  }


  handleChange_bat_lev(event) {
    this.setState({bat_lev: event.target.value});
  }


  handleChange_max_apps(event) {
    this.setState({max_apps: event.target.value});
  }


  handleChange_gps_allowed(event) {
    if (this.state.gps_allowed) {
      this.setState({gps_allowed: false});
    } else {
      this.setState({gps_allowed: true});
    }
  }


  checkNumber(val, defval) {
    try {
      return Number(val);
    }
    catch(err) {
      console.error(err);
      return defval;
    }
  }


  handleView(event) {
    this.setState({isLoading: true});
    console.log('Getting data from sharing model ...');
    // call to api
    try {
      var that = this;
      request.get({url: global.rest_api_um + 'sharing-model'}, function(err, resp, body) {
        if (err) {
          console.error(err);
          that.setState({ show_alert: true, msg: "GET /api/v2/um/sharing-model", msg_content: err.toString() });
        }
        else {
          console.log('Getting data from sharing model ... ok');
          if (global.debug) {
            //that.setState({ show_info: true, msg: "GET /api/v2/um/sharing-model => " + resp.statusCode, msg_content: "Sharing-model retrieved: response: " + body });
          }
          // sharing-model properties
          try {
            body = JSON.parse(body);
            that.setState({ max_cpu: body['sharing_model']['max_cpu_usage'], max_mem: body['sharing_model']['max_memory_usage'],
                            max_sto: body['sharing_model']['max_storage_usage'], max_ban: body['sharing_model']['max_bandwidth_usage'],
                            bat_lev: body['sharing_model']['battery_limit'], gps_allowed: body['sharing_model']['gps_allowed'],
                            max_apps: body['sharing_model']['max_apps'], id_sharing_model: body['sharing_model']['id']});
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
      this.setState({ show_alert: true, msg: "GET /api/v2/um/sharing-model", msg_content: err.toString(), isLoading: false });
    }
  }


  handleSave(event) {
    this.setState({isLoading: true});
    console.log('Updating sharing model ...');
    // call to api
    try {
      var that = this;
      var formData = {
        id: this.state.id_sharing_model,
        max_cpu_usage: this.checkNumber(this.state.max_cpu, 50),
        max_memory_usage: this.checkNumber(this.state.max_mem, 50),
        max_storage_usage: this.checkNumber(this.state.max_sto, 50),
        max_bandwidth_usage: this.checkNumber(this.state.max_ban, 50),
        battery_limit: this.checkNumber(this.state.bat_lev, 50),
        gps_allowed: this.state.gps_allowed,
        max_apps: this.checkNumber(this.state.max_apps, 1)
      };
      request.put({url: global.rest_api_um + this.state.id_sharing_model, json: formData}, function(err, resp, body) {
        if (err) {
          console.error(err);
          that.setState({ show_alert: true, msg: "PUT /api/v2/um/" + that.state.id_sharing_model, msg_content: err.toString() });
        }
        else {
          if (resp.statusCode == 500) {
            that.setState({ show_alert: true, msg: "PUT /api/v2/um/" + that.state.id_sharing_model, msg_content: JSON.stringify(body) + " => " + resp.statusCode });
          }
          else {
            console.log('Updating sharing model ... ok');
            that.setState({ show_info: true, msg: "PUT /api/v2/um/" + that.state.id_sharing_model + " => " + resp.statusCode,
                            msg_content: "Sharing-model updated: response: " + JSON.stringify(body) });
          }
        }

        that.setState({isLoading: false});
      });
    }
    catch(err) {
      console.error(err);
      this.setState({ show_alert: true, msg: "PUT /api/v2/um/sharing-model", msg_content: err.toString(), isLoading: false });
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
        <h3><b>Sharing Model</b>&nbsp;&nbsp;&nbsp;
          {this.state.isLoading ?
            <Spinner animation="border" role="status" variant="primary">
              <span className="sr-only">Loading...</span>
            </Spinner> : ""}
        </h3>
        <p>List of agent's resources shared in mF2C.</p>
        <form>
          <div className="form-group row">
            <div className="col-sm-3">GPS</div>
            <div className="col-sm-9">
              <div className="form-check">
                <input className="form-check-input" type="checkbox" id="GPSCheck1" checked={this.state.gps_allowed} onChange={this.handleChange_gps_allowed}/>
                <small className="form-check-label text-muted" htmlFor="GPSCheck1">
                  Allow the use of GPS by mF2C
                </small>
              </div>
            </div>
          </div>

          <div className="form-group row">
            <label htmlFor="cpuUsageLbl" className="col-sm-3 col-form-label">Max. CPU usage</label>
            <div className="col-sm-2">
              <input type="number" className="form-control" id="cpuUsage" placeholder="10 - 90" value={this.state.max_cpu}
                onChange={this.handleChange_max_cpu} min="10" max="90"/>
            </div>
            <OverlayTrigger placement="right" delay={{ show: 250, hide: 400 }}
                overlay={<Tooltip><i>Integer Value between 10 - 90</i></Tooltip>}>
              <img src="img/help_icon.png" height="20" width="20" />
            </OverlayTrigger>
          </div>

          <div className="form-group row">
            <label htmlFor="memUsageLbl" className="col-sm-3 col-form-label">Max. memory usage</label>
            <div className="col-sm-2">
              <input type="number" className="form-control" id="memUsage" placeholder="10 - 90" value={this.state.max_mem}
                onChange={this.handleChange_max_mem} min="10" max="90"/>
            </div>
            <OverlayTrigger placement="right" delay={{ show: 250, hide: 400 }}
                overlay={<Tooltip><i>Integer Value between 10 - 90</i></Tooltip>}>
              <img src="img/help_icon.png" height="20" width="20" />
            </OverlayTrigger>
          </div>

          <div className="form-group row">
            <label htmlFor="storageUsageLbl" className="col-sm-3 col-form-label">Max. storage usage</label>
            <div className="col-sm-2">
              <input type="number" className="form-control" id="storageUsage" placeholder="10 - 90" value={this.state.max_sto}
                onChange={this.handleChange_max_sto} min="10" max="90"/>
            </div>
            <OverlayTrigger placement="right" delay={{ show: 250, hide: 400 }}
                overlay={<Tooltip><i>Integer Value between 10 - 90</i></Tooltip>}>
              <img src="img/help_icon.png" height="20" width="20" />
            </OverlayTrigger>
          </div>

          <div className="form-group row">
            <label htmlFor="bandwidthUsageLbl" className="col-sm-3 col-form-label">Max. bandwidth usage</label>
            <div className="col-sm-2">
              <input type="number" className="form-control" id="cpuUsage" placeholder="10 - 90" value={this.state.max_ban}
                onChange={this.handleChange_max_ban} min="10" max="90"/>
            </div>
            <OverlayTrigger placement="right" delay={{ show: 250, hide: 400 }}
                overlay={<Tooltip><i>Integer Value between 10 - 90</i></Tooltip>}>
              <img src="img/help_icon.png" height="20" width="20" />
            </OverlayTrigger>
          </div>

          <div className="form-group row">
            <label htmlFor="batteryUsageLbl" className="col-sm-3 col-form-label">Max. battery level usage</label>
            <div className="col-sm-2">
              <input type="number" className="form-control" id="batteryUsage" placeholder="10 - 90" value={this.state.bat_lev}
                onChange={this.handleChange_bat_lev} min="10" max="90"/>
            </div>
            <OverlayTrigger placement="right" delay={{ show: 250, hide: 400 }}
                overlay={<Tooltip><i>Integer Value between 10 - 90</i></Tooltip>}>
              <img src="img/help_icon.png" height="20" width="20" />
            </OverlayTrigger>
          </div>

          <div className="form-group row">
            <label htmlFor="batteryUsageLbl" className="col-sm-3 col-form-label">Max. apps</label>
            <div className="col-sm-2">
              <input type="number" className="form-control" id="batteryUsage" placeholder="1 - 10" value={this.state.max_apps}
                onChange={this.handleChange_max_apps} min="1" max="10"/>
            </div>
            <OverlayTrigger placement="right" delay={{ show: 250, hide: 400 }}
                overlay={<Tooltip>Max. allowed mF2C services that can run in the device / agent. <br/><i>(Integer Value between 1 - 10)</i></Tooltip>}>
              <img src="img/help_icon.png" height="20" width="20" />
            </OverlayTrigger>
          </div>

          <Badge variant="secondary">{this.state.id_sharing_model}</Badge><br />

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

export default SharingModel;
