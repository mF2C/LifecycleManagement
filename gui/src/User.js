import React, { Component } from "react";

class User extends Component {
  render() {
    return (
      <div>
        <h3><b>User Profile</b></h3>
        <p>MF2C user information:</p>
        <form>
          <div className="form-group row">
            <label htmlFor="cpuUsageLbl" className="col-sm-2 col-form-label">Username</label>
            <div className="col-sm-4">
              <input type="username" className="form-control" id="username"/>
            </div>
          </div>

          <button type="submit" className="btn btn-primary">View</button>
          <button type="submit" className="btn btn-danger">Remove</button>
        </form>
      </div>
    );
  }
}

export default User;
