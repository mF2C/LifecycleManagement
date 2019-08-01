import React, { Component } from "react";
import request from "request";
import { Alert, Button, Badge, Card, CardColumns } from 'react-bootstrap';

class Home extends Component {


  render() {
    return (
      <div style={{margin: "25px 0px 0px 0px"}}>

        <CardColumns>
          <Card bg="light" text="black" style={{ width: '18rem' }}>
            <Card.Img variant="top" src="img/mf2c_logo.png" fluid />
            <Card.Body>
              <Card.Title>Lifecycle Manager</Card.Title>
              <Card.Text>
                This module is responsible for managing the deployment and execution of the applications in mF2C.
              </Card.Text>
              <Card.Text>
                The Lifecycle Manager can deploy services in agents with Docker and Docker Swarm.
              </Card.Text>
              <Button variant="secondary" style={{color: "#F5ECCE"}} href="#/serviceinstances">View Service instances</Button>
            </Card.Body>
          </Card>

          <Card bg="dark" text="white" style={{ width: '18rem' }}>
            <Card.Img variant="top" src="img/mf2c_logo.png" fluid />
            <Card.Body>
              <Card.Title>User Management module</Card.Title>
              <Card.Text>
                The User Management module is responsible for managing the user’s profile and the definition of the user’s device resources that will be shared in mF2C. It also checks that the mF2C applications act according to these properties.
              </Card.Text>
              <Button variant="secondary" style={{color: "#D8D8D8"}} href="#/userprofile">User Profile</Button>
              &nbsp;
              <Button variant="secondary" style={{color: "#D8D8D8"}} href="#/sharingmodel">Sharing Model</Button>
            </Card.Body>
          </Card>
        </CardColumns>
      </div>
    );
  }
}

export default Home;
