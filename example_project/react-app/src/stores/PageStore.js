// Menu store


var AppDispatcher = require('../dispatcher/AppDispatcher');
var AppConstants = require('../constants/Constants');
var ServerApi = require('../api/ServerApi');
var ObjectAssign = require('object-assign');
var EventEmitter = require('events').EventEmitter;
var _ = require('lodash');

var CHANGE_EVENT = 'change';


var _store = {
    data: {},
};


var PageStore = ObjectAssign({}, EventEmitter.prototype, {

    addChangeListener: function (cb) {
        this.on(CHANGE_EVENT, cb);
    },

    removeChangeListener: function (cb) {
        this.removeListener(CHANGE_EVENT, cb);
    },

    loadPage: function (pageId) {
        ServerApi.getPage(pageId);
        return _store;
    },

    getPage: function () {
        return _store;
    }

});


AppDispatcher.register(function (payload) {
    var action = payload;

    switch (action.actionType) {


        case AppConstants.GET_PAGE:

            _store.data = action.response;
            PageStore.emit(CHANGE_EVENT);
            break;

        default:
            return true;
    }
});

module.exports = PageStore;
