var onLoad = function onLoad() {

    $.getJSON('./api/agencies', function(data) {
        var agencies = data.agencies;

        table = d3.select("table");

        var thead = table.select('thead');
        var tbody = table.select('tbody');

        thead.selectAll("th")
            .data(_.keys(agencies[0])).enter().append("th")
            .text(function(d){ return d; })
            .attr("onclick", function(d, i) {
                return "orderByColumn(table, '" + d +  "')";
            });

        var rows = tbody.selectAll("tr")
            .data(agencies).enter().append("tr");

        var cells = rows.selectAll("td").data(function(row){
            return _.keys(agencies[0]).map(function(column){
                return { column: column, value: row[column] };
            });
        }).enter().append("td")
            .text(function(d){ return d.value; });

        orderByColumn(table, "id");
    });

    orderByColumn = function orderByColumn(table, column) {
        table.selectAll("tbody tr").sort(function(a, b) {
            return d3.ascending(a[column], b[column]);
        });
    };
};
