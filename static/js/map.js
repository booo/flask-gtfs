var initMap = function initMap() {

    var map = new L.Map('map');
    var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    var osmAttrib='Map data OpenStreetMap contributors';
    var osm = new L.TileLayer(osmUrl, {minZoom: 0, maxZoom: 18, attribution: osmAttrib});

    // start the map in South-East England
    map.setView(new L.LatLng(52.52, 13.41),13);
    map.addLayer(osm);

    $.getJSON('./api/stops?asGeoJSON=true', function(featureCollection){
        console.log(featureCollection);
        featureCollection.features.forEach(function(feature){ 
            console.log(feature.geometry.coordinates);
        });
        L.geoJson(featureCollection).addTo(map);
    });
};
