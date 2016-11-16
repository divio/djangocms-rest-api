// Menu component
var React = require('react');
var MenuStore = require('../stores/MenuStore.js');
// var Actions = require('../actions/Actions.js');
var MenuItem = require('./MenuItem.js');
var Nav = require('react-bootstrap/lib/Nav');


var Menu = React.createClass({

    getInitialState: function () {
        return MenuStore.getItems();
    },

    componentDidMount: function () {
        MenuStore.addChangeListener(this._onChange);
    },

    componentWillUnmount: function () {
        MenuStore.removeChangeListener(this._onChange);
    },

    _onChange: function () {
        this.setState(MenuStore.getItems());
    },

    /**
     * @return {object}
     */
    render: function () {
        var menu_items = [];
        if (this.state.items.length) {
            this.state.items.map(function (item, index) {
                menu_items.push(<MenuItem key={index} index={index} item={item}/>);
                return true;
            });
        }

        return (
            <Nav bsStyle="tabs" activeKey="1" onSelect={this.handleSelect}>
                {menu_items}
            </Nav>
        );
    },


});

module.exports = Menu;
