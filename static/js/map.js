var initMap = function initMap() {

    var map = new L.Map('map');
    var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    var osmAttrib='Map data OpenStreetMap contributors';
    var osm = new L.TileLayer(osmUrl, {minZoom: 0, maxZoom: 18, attribution: osmAttrib});

    // start the map in South-East England
    map.setView(new L.LatLng(52.52, 13.41),13);
    map.addLayer(osm);

    $.getJSON('./api/stops?asGeoJSON=true&bbox=13.0882097323,52.3418234221,13.7606105539,52.6697240587', function(featureCollection){
        L.geoJson(featureCollection).addTo(map);
    });
};
