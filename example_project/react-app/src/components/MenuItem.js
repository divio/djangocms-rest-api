// MenuItem component
var React = require('react');

var NavItem = require('react-bootstrap/lib/NavItem');

var MenuItem = React.createClass({

    _handleClick: function () {
        alert(this.props.item.id);
    },

    /**
     * @return {object}
     */
    render: function () {

        return (
            <NavItem eventKey={this.props.index} onClick={this._handleClick} href="#">{this.props.item.menu_title}</NavItem>

        );
    },


});

module.exports = MenuItem;
