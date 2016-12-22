// Menu store


var AppDispatcher = require('../dispatcher/AppDispatcher');
var AppConstants = require('../constants/Constants');
var ServerApi = require('../api/ServerApi');
var ObjectAssign = require('object-assign');
var EventEmitter = require('events').EventEmitter;
var _ = require('lodash');

var CHANGE_EVENT = 'change';

// Define the store as an empty object
var _store = {
    data: {},
};


var PluginStore = ObjectAssign({}, EventEmitter.prototype, {

    addChangeListener: function (cb) {
        this.on(CHANGE_EVENT, cb);
    },

    removeChangeListener: function (cb) {
        this.removeListener(CHANGE_EVENT, cb);
    },

    loadPlugin: function (pluginId) {
            ServerApi.getPlugin(pluginId);
        return _store;
    },

    getPlugin: function (id) {
        return _store.data[id] || {};

    }

});


AppDispatcher.register(function (payload) {
    var action = payload;

    switch (action.actionType) {


        case AppConstants.GET_PLACEHOLDER:

            _store.data[action.response.id] = action.response;
            PluginStore.emit(CHANGE_EVENT);
            break;

        default:
            return true;
    }
});

module.exports = PluginStore;
