// Menu store


var AppDispatcher = require('../dispatcher/AppDispatcher');
var AppConstants = require('../constants/Constants');
var ServerApi = require('../api/ServerApi');
var ObjectAssign = require('object-assign');
var EventEmitter = require('events').EventEmitter;

var CHANGE_EVENT = 'change';

// Define the store as an empty array
var _store = {
    items: [],
};


var MenuStore = ObjectAssign({}, EventEmitter.prototype, {

    addChangeListener: function (cb) {
        this.on(CHANGE_EVENT, cb);
    },

    removeChangeListener: function (cb) {
        this.removeListener(CHANGE_EVENT, cb);
    },

    getItems: function () {
        if (!_store.items.length) {
            ServerApi.getMenuItems()
        }
        return _store;
    }

});


AppDispatcher.register(function (payload) {
    var action = payload;

    switch (action.actionType) {


        case AppConstants.GET_MENU_ITEMS:

            _store.items = action.response;
            MenuStore.emit(CHANGE_EVENT);
            break;

        default:
            return true;
    }
});

module.exports = MenuStore;
