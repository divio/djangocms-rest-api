// MenuItem component
var React = require('react');
var Link = require('react-router').Link;

var MenuItem = React.createClass({

    /**
     * @return {object}
     */
    render: function () {

        return (
            <li role="presentation" className="">
                <Link to={`/page/${this.props.item.id}`} role="button">{this.props.item.menu_title}</Link>
            </li>

        );
    },


});

module.exports = MenuItem;
