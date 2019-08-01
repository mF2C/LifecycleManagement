import React, { Component } from 'react';

import {
  Route,
  NavLink,
  HashRouter
} from "react-router-dom";

import { Navbar, Nav, Button } from 'react-bootstrap';

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
    global.debug = true;
  }


  render() {
    return (
      <HashRouter>
        <Navbar style={{background: "#666666"}} fixed="top">
          <Navbar.Brand href="/">
            <img
              src="img/mf2c_logo_mini.png"
              width="50"
              height="25"
              className="d-inline-block align-top"
              alt="React Bootstrap logo"
            />
          </Navbar.Brand>
          <Nav className="mr-auto">
            <Nav.Link style={{color: "#E0F2F7"}} exact href="#/"><b>Home</b></Nav.Link>
            <Nav.Link style={{color: "#F5ECCE"}} href="#/launchservice"><b>Launch new service</b></Nav.Link>
            <Nav.Link style={{color: "#F5ECCE"}} href="#/serviceinstances"><b>Service instances</b></Nav.Link>
            <Nav.Link style={{color: "#F5ECCE"}} href="#/launchjob"><b>Launch job (DER)</b></Nav.Link>
            <Nav.Link style={{color: "#D8D8D8"}} href="#/userprofile"><b>User-Profile</b></Nav.Link>
            <Nav.Link style={{color: "#D8D8D8"}} href="#/sharingmodel"><b>Sharing-Model</b></Nav.Link>
            <Nav.Link style={{color: "#D8D8D8"}} href="#/user"><b>User</b></Nav.Link>
          </Nav>
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
