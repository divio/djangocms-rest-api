// Menu store


var AppDispatcher = require('../dispatcher/AppDispatcher');
var AppConstants = require('../constants/Constants');
var ServerApi = require('../api/ServerApi');
var ObjectAssign = require('object-assign');
var EventEmitter = require('events').EventEmitter;

var CHANGE_EVENT = 'change';

// Define the store as an empty object
var _store = {
    data: {},
};


var PlaceholderStore = ObjectAssign({}, EventEmitter.prototype, {

    addChangeListener: function (cb) {
        this.on(CHANGE_EVENT, cb);
    },

    removeChangeListener: function (cb) {
        this.removeListener(CHANGE_EVENT, cb);
    },

    loadPlaceholder: function (placeholderId) {
            ServerApi.getPlaceholder(placeholderId);
        return _store;
    },

    getPlaceholder: function (id) {
        return _store.data[id] || {};

    }

});


AppDispatcher.register(function (payload) {
    var action = payload;

    switch (action.actionType) {


        case AppConstants.GET_PLACEHOLDER:

            _store.data[action.response.id] = action.response;
            PlaceholderStore.emit(CHANGE_EVENT);
            break;

        default:
            return true;
    }
});

module.exports = PlaceholderStore;
