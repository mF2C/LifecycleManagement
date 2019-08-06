import React, { Component } from 'react';

import {
  Route,
  HashRouter
} from "react-router-dom";

import { Navbar, Nav } from 'react-bootstrap';

import Home from "./Home";
import LaunchService from "./LaunchService";
import ServiceInstances from "./ServiceInstances";
import SharingModel from "./SharingModel";
import UserProfile from "./UserProfile";
import User from "./User";
import LaunchJob from "./LaunchJob";
import './App.css';


class App extends Component {


  constructor(props, context) {
    super(props, context);

    //Setting up global variables
    global.rest_api_lm = 'http://192.168.252.41:46000/api/v2/lm/';
    global.rest_api_um = 'http://192.168.252.41:46300/api/v2/um/';
    global.const_rest_api_lm = 'http://192.168.252.41:46000/api/v2/lm/';
    global.const_rest_api_um = 'http://192.168.252.41:46300/api/v2/um/';
    global.debug = true;
  }


  render() {
    return (
      <HashRouter>
        <Navbar style={{background: "#777777"}} fixed="top">
          <Navbar.Brand href="/">
            <img
              src="img/mf2c_logo_mini.png"
              width="45"
              height="25"
              className="d-inline-block align-top"
              alt="React Bootstrap logo"
            />
          </Navbar.Brand>
          <Nav className="mr-auto" defaultActiveKey="#/" as="ul">
            <Nav.Item as="li">
              <Nav.Link style={{color: "#E0F2F7"}} exact href="#/">
                <i class="fa fa-home" aria-hidden="true"></i>&nbsp;<b>Home</b>
              </Nav.Link>
            </Nav.Item>
            <Nav.Item as="li"></Nav.Item>
            <Nav.Item as="li">
              <Nav.Link style={{color: "#F5ECCE"}} href="#/launchservice">
                <i class="fa fa-file-text-o" aria-hidden="true"></i>&nbsp;<b>Services</b>
              </Nav.Link>
            </Nav.Item>
            <Nav.Item as="li">
              <Nav.Link style={{color: "#F5ECCE"}} href="#/serviceinstances">
                <i class="fa fa-tasks" aria-hidden="true"></i>&nbsp;<b>Service instances</b>
              </Nav.Link>
            </Nav.Item>
            <Nav.Item as="li">
              <Nav.Link style={{color: "#F5ECCE"}} href="#/launchjob">
                <i class="fa fa-cogs" aria-hidden="true"></i>&nbsp;<b>Jobs (DER)</b>
              </Nav.Link>
            </Nav.Item>
            <Nav.Item as="li"></Nav.Item>
            <Nav.Item as="li">
              <Nav.Link style={{color: "#D8D8D8"}} href="#/userprofile">
                <i class="fa fa-address-card-o" aria-hidden="true"></i>&nbsp;<b>User-Profile</b>
              </Nav.Link>
            </Nav.Item>
            <Nav.Item as="li">
              <Nav.Link style={{color: "#D8D8D8"}} href="#/sharingmodel">
                <i class="fa fa-share-alt" aria-hidden="true"></i>&nbsp;<b>Sharing-Model</b>
              </Nav.Link>
            </Nav.Item>
            <Nav.Item as="li">
              <Nav.Link style={{color: "#D8D8D8"}} href="#/user">
                <i class="fa fa-user" aria-hidden="true"></i>&nbsp;<b>User</b>
              </Nav.Link>
            </Nav.Item>
          </Nav>
          <Navbar.Collapse className="justify-content-end">
            <Navbar.Text>
              <font color="lightgray" size="1"><i>v1.0.0</i></font>
            </Navbar.Text>
          </Navbar.Collapse>
        </Navbar>

        <div className="content">
          <Route exact path="/" component={Home}/>
          <Route path="/launchservice" component={LaunchService}/>
          <Route path="/serviceinstances" component={ServiceInstances}/>
          <Route path="/launchjob" component={LaunchJob}/>
          <Route path="/userprofile" component={UserProfile}/>
          <Route path="/sharingmodel" component={SharingModel}/>
          <Route path="/user" component={User}/>
        </div>
      </HashRouter>
    );
  }
}

export default App;
