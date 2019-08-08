import React, { Component } from "react";
import { Button, Card, CardColumns, InputGroup, FormControl } from 'react-bootstrap';


class Home extends Component {


  constructor(props, context) {
    super(props, context);

    this.state = {
      url_rest_api_um: global.rest_api_um,
      url_rest_api_lm: global.rest_api_lm
    }

    this.handleChange_rest_api_lm = this.handleChange_rest_api_lm.bind(this);
    this.handleChange_rest_api_um = this.handleChange_rest_api_um.bind(this);
    this.handleSave = this.handleSave.bind(this);
    this.handleRestore = this.handleRestore.bind(this);
  }


  handleChange_rest_api_lm(event) {
    this.setState({url_rest_api_lm: event.target.value});
  }


  handleChange_rest_api_um(event) {
    this.setState({url_rest_api_um: event.target.value});
  }


  handleSave(event) {
    global.rest_api_um = this.state.url_rest_api_um;
    global.rest_api_lm = this.state.url_rest_api_lm;
  }


  handleRestore(event) {
    global.rest_api_um = global.const_rest_api_um;
    global.rest_api_lm = global.const_rest_api_lm;

    this.setState({url_rest_api_lm: global.rest_api_lm});
    this.setState({url_rest_api_um: global.rest_api_um});
  }


  render() {
    return (
      <div style={{margin: "25px 0px 0px 0px"}}>
        <CardColumns>
          <Card bg="light" text="black" style={{ width: '19rem' }}>
            <Card.Img variant="top" src="img/mf2c_logo.png" fluid />
            <Card.Body>
              <Card.Title>Lifecycle Manager</Card.Title>
              <Card.Subtitle className="mb-2 text-muted"><i>version 1.3.6</i></Card.Subtitle>
              <Card.Text>
                This module is responsible for managing the deployment and execution of applications in mF2C.
              </Card.Text>
              <Card.Text>
                The Lifecycle Manager can deploy services in agents with Docker and Docker Swarm.
              </Card.Text>
            </Card.Body>
          </Card>

          <Card bg="dark" text="white" style={{ width: '19rem' }}>
            <Card.Img variant="top" src="img/mf2c_logo.png" fluid />
            <Card.Body>
              <Card.Title>User Management module</Card.Title>
              <Card.Subtitle className="mb-2 text-muted"><i>version 1.3.6</i></Card.Subtitle>
              <Card.Text>
                The User Management module is responsible for managing the user’s profile and the definition of the device's resources that will be shared in mF2C. It also checks that the mF2C applications act according to these properties.
              </Card.Text>
            </Card.Body>
          </Card>

          <Card bg="secondary" text="white" style={{ width: '21rem' }}>
            <Card.Header><b>REST API</b></Card.Header>
            <Card.Body>
              <Card.Title style={{color: "#F5ECCE"}}>Lifecycle</Card.Title>
              <Card.Text>
                <InputGroup size="sm" className="mb-3">
                  <FormControl aria-label="Small" aria-describedby="inputGroup-sizing-sm" value={this.state.url_rest_api_lm}
                    onChange={this.handleChange_rest_api_lm} style={{ backgroundColor: "#E0F2F7" }}/>
                </InputGroup>
              </Card.Text>
              <Card.Title style={{color: "#D8D8D8"}}>User Management</Card.Title>
              <Card.Text>
                <InputGroup size="sm" className="mb-3">
                  <FormControl aria-label="Small" aria-describedby="inputGroup-sizing-sm" value={this.state.url_rest_api_um}
                    onChange={this.handleChange_rest_api_um} style={{ backgroundColor: "#E0F2F7" }}/>
                </InputGroup>
              </Card.Text>
              <Button variant="info" size="sm" onClick={this.handleSave}><i class="fa fa-floppy-o" aria-hidden="true"></i>&nbsp;Save</Button>
              &nbsp;
              <Button variant="light" size="sm" onClick={this.handleRestore}><i class="fa fa-eraser" aria-hidden="true"></i>&nbsp;Restore default</Button>
            </Card.Body>
          </Card>
        </CardColumns>
      </div>
    );
  }
}

export default Home;
