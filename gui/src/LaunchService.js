import React, { Component } from "react";
import { Dropdown } from 'react-bootstrap';


class LaunchService extends Component {


  constructor(props, context) {
    super(props, context);

    this.state = {
      selservice: "",
      username: 'wsvincent',
      dropdownOpen: false,
      value : "",
      lservices: []
    };

    this.handleClick = this.handleClick.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.select = this.select.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleCancel = this.handleCancel.bind(this);
  }


  componentDidMount() {
    this.setState({
      lservices: ['one', 'two', 'three', 'four']
    });
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
    const items = []
    for (const [index, value] of this.state.lservices.entries()) {
      items.push(<Dropdown.Item onClick={this.select}>{value}</Dropdown.Item>)
    }

    return (
      <div style={{margin: "25px 0px 0px 0px"}}>
        <h3><b>Launch a new service</b></h3>
        <p>Select a service and run it in mF2C</p>
        <form onSubmit={this.handleSubmit}>
          <div className="form-group row">
            <Dropdown className="col-sm-2">
              <Dropdown.Toggle variant="secondary" id="dropdown-basic">
                Service
              </Dropdown.Toggle>

              <Dropdown.Menu>
                {items}
                <Dropdown.Item onClick={this.select}>Service a</Dropdown.Item>
                <Dropdown.Item onClick={this.select}>Service b</Dropdown.Item>
                <Dropdown.Item onClick={this.select}>Service c</Dropdown.Item>
              </Dropdown.Menu>
            </Dropdown>
            <div className="col-sm-4">
              <input type="text" className="form-control" id="service" value={this.state.selservice} disabled/>
            </div>
          </div>

          <button type="submit" value="Submit" className="btn btn-success"><i class="fa fa-rocket" aria-hidden="true"></i>&nbsp;Launch</button>
          &nbsp;
          <button className="btn btn-warning" onClick={this.handleCancel}><i class="fa fa-times" aria-hidden="true"></i>&nbsp;Cancel</button>
        </form>
      </div>
    );
  }
}

export default LaunchService;
