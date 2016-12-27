// server actions
var AppDispatcher = require('../dispatcher/AppDispatcher');
var Constants = require('../constants/Constants');

module.exports = {

    receiveMenuItems: function (response) {
        AppDispatcher.dispatch({
            actionType: Constants.GET_MENU_ITEMS,
            response: response
        });
    },
    receivePage: function (response) {
        AppDispatcher.dispatch({
            actionType: Constants.GET_PAGE,
            response: response
        });
    },
    receivePlaceholder: function (response) {
        AppDispatcher.dispatch({
            actionType: Constants.GET_PLACEHOLDER,
            response: response
        });
    },
    receivePlugin: function (response) {
        AppDispatcher.dispatch({
            actionType: Constants.GET_PLACEHOLDER,
            response: response
        });
    },
};
