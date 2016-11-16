// MenuItem component
var React = require('react');

var NavItem = require('react-bootstrap/lib/NavItem');
var BootstrapMenuItem = require('react-bootstrap/lib/MenuItem');
var NavDropdown = require('react-bootstrap/lib/NavDropdown');

var MenuItem = React.createClass({

    _handleClick: function () {
        alert(this.props.item.id);
    },

    /**
     * @return {object}
     */
    render: function () {
        var descendants = [];
        if (this.props.item.descendants.length) {

            var pindex = this.props.index + '.';
            this.props.item.descendants.map(function (item, index) {
                descendants.push(<MenuItem key={index} parent={pindex} index={index} item={item}/>);
                return true;
            });
            return (
                <NavDropdown eventKey={this.props.index} title={this.props.item.title}
                             id={this.props.index + "nav-dropdown"}>
                    {descendants}
                </NavDropdown>
            )
        }
        if (this.props.parent) {
            return (
                <BootstrapMenuItem eventKey={this.props.parent + this.props.index}
                                   onClick={this._handleClick}>{this.props.item.title}</BootstrapMenuItem>


            );
        }
        return (
            <NavItem eventKey={this.props.index} onClick={this._handleClick} href="#">{this.props.item.title}</NavItem>

        );
    },


});

module.exports = MenuItem;
