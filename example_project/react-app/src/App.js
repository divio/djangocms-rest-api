import React, {Component} from "react";

var ExampleApp = require('./components/ExampleApp.js');

class App extends Component {
    render() {
        return (
            <div className="App">

                <ExampleApp/>

            </div>
        );
    }
}

export default App;
