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

/* Hashes => Functions */
var controller = {
    'watches': watches_list,
    'pings': pings_list,
    /* Default */
    '': watches_list
};

/* Returns a pretty string representation of the given object */
var dump = function(object) {
    return JSON.stringify(object, null, 4);
};

$(function () {
    $(window).on('hashchange', update_view);
    update_view();
});

function update_view() {
    var hash = location.hash.replace(/^#/, '');
    log.info("Observed hashchange, now at '" + hash + "'");
    if(hash in controller) {
        /* Reset the current navbar 'active' flag */
        $('#navbar ul li').removeClass('active');
        controller[hash]();
    }
}

function watches_list() {
    log.info("watches_list()");
    $('#navbar-watches').addClass('active');
    $('#content-title').empty();
    $('#content-title').append('Watches');
    $.getJSON('/api/watches/', function(data) {
        var table_columns = "<tr>";
        for(var column of data['columns']) {
            table_columns += "<th>" + column + "</th>";
        }
        table_columns += "</tr>"
        $("#ww-columns").empty();
        $("#ww-columns").append(table_columns);
        var table_records = "";
        for(var record of data['records']) {
            table_records += "<tr>";
            for(var i = 0; i < record.length; i++) {
                var field = record[i];
                if(i == 5) {
                    // Decorate the watch word
                    table_records += "<td><a href=\"#\">" + field + "</a></td>";
                } else if(i == 6) {
                    var label_style = vtable_status_label[field];
                    table_records += "<td style=\"text-transform: capitalize\"><span class=\"label label-" + label_style + "\">" + field + "</span></td>";
                } else {
                    table_records += "<td>" + field + "</td>";
                }
            }
            table_records += "</tr>";
        }
        $("#ww-records").empty();
        $("#ww-records").append(table_records);
    });
}

function pings_list() {
    log.info("pings_list()");
    var MAX_FIELD_LENGTH = 50;
    $('#navbar-pings').addClass('active');
    $('#content-title').empty();
    $('#content-title').append('Pings');
    $.getJSON('/api/pings/', function(data) {
        var table_columns = "<tr>";
        for(var column of data['columns']) {
            table_columns += "<th>" + column + "</th>";
        }
        table_columns += "</tr>"
        $("#ww-columns").empty();
        $("#ww-columns").append(table_columns);
        var table_records = "";
        for(var record of data['records']) {
            table_records += "<tr>";
            for(var i = 0; i < record.length; i++) {
                var field = record[i];
                if(field.length > MAX_FIELD_LENGTH) {
                    field = field.slice(0, MAX_FIELD_LENGTH);
                    field += ' ...';
                }
                table_records += "<td>" + field + "</td>";
            }
            table_records += "</tr>";
        }
        $("#ww-records").empty();
        $("#ww-records").append(table_records);
    });
}
