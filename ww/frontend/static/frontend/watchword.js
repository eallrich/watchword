/* Init */

log.setDefaultLevel('info');
log.info("Initializing watchword.js");

/* Returns a pretty string representation of the given object */
var dump = function(object) {
    return JSON.stringify(object, null, 4);
};

$(function () {
    var vtable_status_label = {
        'fresh': 'info',
        'quiet': 'success',
        'alert': 'warning',
        'alarm': 'danger',
        'sleep': 'default'
    };
    $.getJSON('/api/watches/', function(data) {
        log.info(dump(data));
        var table_columns = "<tr>";
        for(var column of data['columns']) {
            table_columns += "<th>" + column + "</th>";
        }
        table_columns += "</tr>"
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
        $("#ww-records").append(table_records);
    });
});
