import React from "react";
import App from "./App";
import Page from "./components/Page";
import { render } from 'react-dom';
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/css/bootstrap-theme.css";
import "./index.css";

var Router = require('react-router').Router;
var Route = require('react-router').Route;
var browserHistory = require('react-router').browserHistory;

render((
  <Router history={browserHistory}>
    <Route path="/" component={App}>
        <Route path="/page/:pageId" component={Page}/>

    </Route>
  </Router>
), document.getElementById('root'));
