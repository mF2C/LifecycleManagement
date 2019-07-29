import React, { Component } from "react";

class UserProfile extends Component {
  render() {
    return (
      <div>
        <h3><b>User Profile</b></h3>
        <p>How the agent will make use of mF2C:</p>
        <form>
          <div className="form-group row">
            <div className="col-sm-2">Resource contributor</div>
            <div className="col-sm-10">
              <div className="form-check">
                <input className="form-check-input" type="checkbox" id="RCCheck1"/>
                <small className="form-check-label text-muted" htmlFor="RCCheck1">
                  Allow other mF2C devices to use agent's resources (RAM, Battery ...)
                </small>
              </div>
            </div>
          </div>

          <div className="form-group row">
            <div className="col-sm-2">Service Consumer</div>
            <div className="col-sm-10">
              <div className="form-check">
                <input className="form-check-input" type="checkbox" id="SCCheck1"/>
                <small className="form-check-label text-muted" htmlFor="SCCheck1">
                  Check if you will launch services to be executed in mF2C
                </small>
              </div>
            </div>
          </div>

          <button type="submit" className="btn btn-primary">View</button>
        </form>
      </div>
    );
  }
}

export default UserProfile;
