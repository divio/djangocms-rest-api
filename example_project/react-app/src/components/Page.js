// Page component
var React = require('react');
var PageStore = require('../stores/PageStore.js');
var Placeholder = require('./Placeholder.js');
var _ = require('lodash');

var Page = React.createClass({

    getInitialState: function () {
        return PageStore.loadPage(this.props.params.pageId);
    },

    componentDidMount: function () {
        PageStore.addChangeListener(this._onChange);
    },

    componentWillReceiveProps: function (nextProps) {
        this.setState(PageStore.loadPage(nextProps.params.pageId));
    },

    componentWillUnmount: function () {
        PageStore.removeChangeListener(this._onChange);
    },

    _onChange: function () {
        this.setState(PageStore.getPage());
    },

    /**
     * @return {object}
     */
    render: function () {

        var placeholders = [];
        if (this.state.data.placeholders && this.state.data.placeholders.length) {
            this.state.data.placeholders.map(function (item, index) {
                placeholders.push(<Placeholder key={item} placeholderId={item}/>);
                return true;
            });
        }
        return (
            <div className="content">
                <h3>Page info</h3>
                <ul>
                    <li>title: {this.state.data.title}</li>
                    <li>page_title: {this.state.data.page_title}</li>
                    <li>menu_title: {this.state.data.menu_title}</li>
                    <li>meta_description: {this.state.data.meta_description}</li>
                    <li>slug: {this.state.data.slug}</li>
                    <li>path: {this.state.data.path}</li>
                </ul>
                <h4>Placeholders</h4>
                {placeholders}
            </div>
        )
    },


});

module.exports = Page;
