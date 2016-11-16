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
};
