// Plugin component
var React = require('react');
var PluginStore = require('../stores/PluginStore.js');
var _ = require('lodash');


var Plugin = React.createClass({

    getInitialState: function () {
        return PluginStore.loadPlugin(this.props.pluginId);
    },

    componentDidMount: function () {
        PluginStore.addChangeListener(this._onChange);
    },

    componentWillUnmount: function () {
        PluginStore.removeChangeListener(this._onChange);
    },

    _onChange: function () {
        this.setState(PluginStore.getPlugin(this.props.pluginId));
    },

    /**
     * @return {object}
     */
    render: function () {
        var data = this.state.plugin_type === 'FilerImagePlugin'? this.state.image : this.state.plugin_data;

        return (
            <div className="plugin">
                <h5>Plugin info</h5>
                <ul>
                    <li>id: {this.state.id}</li>
                    <li>type: {this.state.plugin_type}</li>
                    <li>plugin data: {JSON.stringify(data)}</li>
                </ul>

            </div>
        )
    },


});

module.exports = Plugin;
