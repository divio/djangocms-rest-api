var React = require('react');
var Menu = require('./Menu.js');

var ExampleApp = React.createClass({


    /**
     * @return {object}
     */
    render: function () {
        return (
            <div>
                <Menu />
            </div>
        );
    },


});

module.exports = ExampleApp;
