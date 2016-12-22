// Placeholder component
var React = require('react');
var PlaceholderStore = require('../stores/PlaceholderStore.js');
var Plugin = require('./Plugin.js');
var _ = require('lodash');

var Placeholder = React.createClass({

    getInitialState: function () {
        return PlaceholderStore.loadPlaceholder(this.props.placeholderId);
    },

    componentDidMount: function () {
        PlaceholderStore.addChangeListener(this._onChange);
    },

    componentWillUnmount: function () {
        PlaceholderStore.removeChangeListener(this._onChange);
    },

    _onChange: function () {
        this.setState(PlaceholderStore.getPlaceholder(this.props.placeholderId));
    },

    /**
     * @return {object}
     */
    render: function () {
        var plugins = [];
        if (this.state.plugins && this.state.plugins.length) {
            this.state.plugins.map(function (item, index) {
                plugins.push(<Plugin key={item} pluginId={item}/>);
                return true;
            });
        }
        return (
            <div className="placeholder">
                <h4>Placeholder info</h4>
                <ul>
                    <li>slot: {this.state.slot}</li>
                    <li>id: {this.state.id}</li>
                </ul>
                <h5>Plugins</h5>
                {plugins}
            </div>
        )
    },


});

module.exports = Placeholder;
