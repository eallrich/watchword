/* Init */

log.setDefaultLevel('info');
log.info("Initializing watchword.js");

/* Mapping from Watch states to Bootstrap styles */
var vtable_status_label = {
    'fresh': 'info',
    'quiet': 'success',
    'alert': 'warning',
    'alarm': 'danger',
    'sleep': 'default'
};

/* Represents routes known to the client. Information necessary for view
updates (e.g. the new title for the page) are also defined. The format is
    URL hash => {View config object}
*/
var controller = {
    'watches': {
        'url': '/api/watches/',
        'title': 'Watches',
        'menu_id': '#navbar-watches',
        'decorators': [_decorate_status]
    },
    'pings': {
        'url': '/api/pings/',
        'title': 'Pings',
        'menu_id': '#navbar-pings',
        'decorators': undefined
    },
    'flares': {
        'url': '/api/flares/',
        'title': 'Flares',
        'menu_id': '#navbar-flares',
        'decorators': undefined
    },
    'launches': {
        'url': '/api/launches/',
        'title': 'Launches',
        'menu_id': '#navbar-launches',
        'decorators': [_decorate_status]
    }
};

/* Returns a pretty string representation of the given object */
var dump = function(object) {
    return JSON.stringify(object, null, 4);
};

$(function () {
    $(window).on('hashchange', event_hashchange);
    /* By default we don't have anything to show, so let's take this chance
    to start initializing the view with a default (if nothing else is set) */
    event_hashchange();
});

function event_hashchange() {
    var hash = location.hash.replace(/^#/, '');
    log.info("Observed hashchange, now at '" + hash + "'");
    var config = controller['watches']; // the default view
    if (hash in controller) {
        config = controller[hash];
    }
    update_view(config);
}

/* Performs common actions needed for view updates and then passes control
to the data retrieval function, providing the configured parameters as
available. */
function update_view(config) {
    /* Reset the current navbar 'active' flag */
    $('#navbar ul li').removeClass('active');
    $(config['menu_id']).addClass('active');
    $('#content-title').empty();
    $('#content-title').append(config['title']);
    _list(config['url'], config['decorators']);
}

/* Tries to only modify fields which convey the status of a Watch. For now,
this is accomplished by checking to see if the state is present in the vtable
defined for mapping watch states to bootstrap styles. */
function _decorate_status(field) {
    if (field in vtable_status_label) {
        var style = vtable_status_label[field];
        field = field.charAt(0).toUpperCase() + field.slice(1);
        return "<span class=\"label label-" + style + "\">" + field + "</span>";
    } else {
        return field;
    }
}

/* Retrieves data (columns + records) from the given URL and calls decorators
(if any are defined) on each field value as they are wrapped in <tr> and <td>
tags */
function _list(url, decorators) {
    log.info("_list(" + url + ")");
    $.getJSON(url, function(data) {
        var table_columns = _unpack_columns(data['columns']);
        var table_records = "";
        for (var record of data['records']) {
            table_records += "<tr>";
            for (var i = 0; i < record.length; i++) {
                var field = record[i];
                if (decorators !== undefined) {
                    for (var decorator of decorators) {
                        field = decorator(field);
                    }
                }
                table_records += "<td>" + field + "</td>";
            }
            table_records += "</tr>";
        }
        _update_table(table_columns, table_records);
    });
}

/* Wraps column names in <th> tags, all inside a pair of <tr> tags */
function _unpack_columns(columns) {
    var table_columns = "<tr>";
    for (var column of columns) {
        table_columns += "<th>" + column + "</th>";
    }
    table_columns += "</tr>"
    return table_columns
}

function _update_table(columns, records) {
    $("#ww-columns").empty();
    $("#ww-columns").append(columns);
    $("#ww-records").empty();
    $("#ww-records").append(records);
}
