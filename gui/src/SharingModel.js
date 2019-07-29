import React, { Component } from "react";

class SharingModel extends Component {
  render() {
    return (
      <div>
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

          <button type="submit" className="btn btn-primary">View</button>
        </form>
      </div>
    );
  }
}

export default SharingModel;
