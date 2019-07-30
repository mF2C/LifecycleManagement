import React, { Component } from "react";
import { Dropdown } from 'react-bootstrap';


class LaunchService extends Component {


  constructor(props, context) {
    super(props, context);

    this.state = {
      selservice: "",
      username: 'wsvincent',
      dropdownOpen: false,
      value : ""
    };

    this.handleClick = this.handleClick.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.select = this.select.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleCancel = this.handleCancel.bind(this);
  }


  handleClick(e) {
    e.preventDefault();
    this.setState({selservice: e.target.value})
  }


  handleChange(e) {
    this.setState({
      username: e.target.value,
      selservice: e.target.value
    });
  }


  select(event) {
    this.setState({
      dropdownOpen: !this.state.dropdownOpen,
      value: event.target.innerText,
      selservice: event.target.innerText
    });
  }


  handleSubmit(event) {
    alert('handleSubmit: A new service was submitted: ' + this.state.value);
    event.preventDefault();
  }


  handleCancel(event) {
    alert('handleCancel: Service submit cancelled');
    event.preventDefault();
  }

  /*
  <div>
    Hello {this.state.username} <br />
    Change name: <input type="text" onChange={this.handleChange}/>
  </div>
  */

  render() {
    return (
      <div style={{margin: "-25px 0px 0px 0px"}}>
        <h3><b>Launch a new service</b></h3>
        <p>Select a service and run it in mF2C</p>
        <form onSubmit={this.handleSubmit}>
          <div className="form-group row">
            <Dropdown className="col-sm-2">
              <Dropdown.Toggle variant="secondary" id="dropdown-basic">
                Service
              </Dropdown.Toggle>

              <Dropdown.Menu>
                <Dropdown.Item onClick={this.select}>Service 1</Dropdown.Item>
                <Dropdown.Item onClick={this.select}>Service 2</Dropdown.Item>
                <Dropdown.Item onClick={this.select}>Service 3</Dropdown.Item>
              </Dropdown.Menu>
            </Dropdown>
            <div className="col-sm-4">
              <input type="text" className="form-control" id="service" value={this.state.selservice} readonly/>
            </div>
          </div>

          <button type="submit" value="Submit" className="btn btn-success">Launch</button>
          <button className="btn btn-warning" onClick={this.handleCancel}>Cancel</button>
        </form>
      </div>
    );
  }
}

export default LaunchService;
