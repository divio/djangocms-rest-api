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


    },

    getPage : function (pageId) {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                ServerActions.receivePage(JSON.parse(this.responseText))
            }
        };
        xhttp.open("GET", Constants.API_ENDPOINT + 'pages/' + pageId, true);
        xhttp.send();


    },

    getPlaceholder : function (placeholderId) {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                ServerActions.receivePlaceholder(JSON.parse(this.responseText))
            }
        };
        xhttp.open("GET", Constants.API_ENDPOINT + 'placeholders/' + placeholderId, true);
        xhttp.send();
    },

    getPlugin : function (pluginId) {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                ServerActions.receivePlugin(JSON.parse(this.responseText))
            }
        };
        xhttp.open("GET", Constants.API_ENDPOINT + 'plugins/' + pluginId, true);
        xhttp.send();
    }
};
