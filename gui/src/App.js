import React, { Component } from 'react';

import {
  Route,
  NavLink,
  HashRouter
} from "react-router-dom";
import Home from "./Home";
import LaunchService from "./LaunchService";
import ServiceInstances from "./ServiceInstances";
import SharingModel from "./SharingModel";
import UserProfile from "./UserProfile";
import User from "./User";
import LaunchJob from "./LaunchJob";

import './App.css';


class App extends Component {
  render() {
    return (
      <HashRouter>
        <div style={{margin: "-25px 0px 0px 0px"}}>
          <font size="5"> <b>Apps Lifecycle Dashboard</b></font>

          <ul className="header">
            <li><NavLink style={{color: "lightblue"}} exact to="/">Home</NavLink></li>
            <li style={{color: "gray"}}>|</li>
            <li><NavLink style={{color: "lightyellow"}} to="/launchservice">Launch new service</NavLink></li>
            <li><NavLink style={{color: "lightyellow"}} to="/serviceinstances">Service instances</NavLink></li>
            <li><NavLink style={{color: "lightyellow"}} to="/launchjob">Launch job (DER)</NavLink></li>
            <li style={{color: "gray"}}>|</li>
            <li><NavLink style={{color: "lightgray"}} to="/userprofile">User-Profile</NavLink></li>
            <li><NavLink style={{color: "lightgray"}} to="/sharingmodel">Sharing-Model</NavLink></li>
            <li><NavLink style={{color: "lightgray"}} to="/user">User</NavLink></li>
          </ul>
          <div className="content">
            <Route exact path="/" component={Home}/>
            <Route path="/launchservice" component={LaunchService}/>
            <Route path="/serviceinstances" component={ServiceInstances}/>
            <Route path="/launchjob" component={LaunchJob}/>
            <Route path="/userprofile" component={UserProfile}/>
            <Route path="/sharingmodel" component={SharingModel}/>
            <Route path="/user" component={User}/>
          </div>
        </div>
      </HashRouter>
    );
  }
}

export default App;
