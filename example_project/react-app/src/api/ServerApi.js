// Server API logic
var ServerActions = require('../actions/ServerActions');
var Constants = require('../constants/Constants');

module.exports = {

    getMenuItems: function () {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                ServerActions.receiveMenuItems(JSON.parse(this.responseText))
            }
        };
        xhttp.open("GET", Constants.API_ENDPOINT + 'pages/', true);
        xhttp.send();


    }
};
