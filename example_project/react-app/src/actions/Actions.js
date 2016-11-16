// App actions
var AppDispatcher = require('../dispatcher/AppDispatcher');
var Constants = require('../constants/Constants');
var ServerApi = require('../api/ServerApi');

module.exports = {

    getMenuItems: function () {
        AppDispatcher.dispatch({
            actionType: Constants.GET_RANDOM
        });

        ServerApi.getMenuItems();
    }

};
