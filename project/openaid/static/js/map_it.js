/**
 * Created by guglielmo on 29/09/13.
 */

var map = L.map('map', {
    minZoom: 2,
    maxZoom: 5,
    scrollWheelZoom: false,
    maxBounds: [[90.0,-220.0],[-70.0,220.0]]
}).setView([0.0, 0.0], 2);

// proxied tiles
var cloudmade = L.tileLayer('http://tilestache.openpolis.it/cm_109537/{z}/{x}/{y}.png', {
//    attribution: 'Mappa &copy; 2011 OpenStreetMap contributors e CloudMade | Dati &copy; <a href="http://http://stats.oecd.org/">OECD</a>',
    attribution: 'Mappa &copy; 2014 OpenStreetMap contributors e CloudMade',
    noWrap: true,
    continuousWorld: false
}).addTo(map);

map.attributionControl.setPrefix('powered by <a href="http://leafletjs.com">Leaflet</a>');

// control that shows state info on hover
var info = L.control();

info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info');
    this.update();
    return this._div;
};

info.update = function (props) {
    var html = '<h4 class="popover-title">Fondi impegnati</h4><div class="popover-content">';
    if (props) {
        html += '<span class="highlight"><b>' + (props.label ? props.label : props.name) + '</b><br />';
        if (props.value) {
            html += (Humanize.intcomma(props.value).replace(/,/g, '.') + ' euro</span>');
        }
        else {
            html += 'Nessun dato OCSE';
        }
    }
    else {
        html += 'Passa con il mouse sopra a un paese';
    }
    html += '</div>';
    this._div.innerHTML = html;
};

info.addTo(map);


// get color depending on population density value
function getColor(d) {
    return d > 100000000  ? '#901800' :
           d > 10000000  ? '#a64633' :
           d > 1000000   ? '#bc7466' :
           d > 100000   ? '#d3a399' :
           d > 0   ?   '#e9d1cc' :
                      '#D4CFB9';
}

function style(feature) {
    return {
        weight: 1,
        opacity: 0.50,
        color: 'white',
        fillOpacity: 1.0,
        fillColor: getColor(feature.properties.value)
    };
}

function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 3,
        opacity: 1,
        color: '#ffffff',
        fillOpacity: 1.0
    });

    if (!L.Browser.ie && !L.Browser.opera) {
        layer.bringToFront();
    }

    info.update(layer.feature.properties);
}

var geojson;

function resetHighlight(e) {
    geojson.resetStyle(e.target);
    info.update();
}

function zoomToFeature(e) {
    map.fitBounds(e.target.getBounds());
}

function navigateToFeatureURL(e) {
    if (window.is_widget) {
        window.open(e.target.feature.properties.url, '_blank');
    } else {
        window.location = e.target.feature.properties.url;
    }
}

function onEachFeature(feature, layer) {
    if (feature.properties.url)
    {
        layer.on({
            mouseover: highlightFeature,
            mouseout: resetHighlight,
            click: navigateToFeatureURL
        });
    } else {
        layer.on({
            mouseover: highlightFeature,
            mouseout: resetHighlight
        });
    }
}

geojson = L.geoJson(states, {
    style: style,
    onEachFeature: onEachFeature
}).addTo(map);


var legend = L.control({position: 'bottomright'});

legend.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'info legend'),
        grades = [0, 100000, 1000000, 10000000, 100000000],
        labels = [],
        grades_labels = [
            'fino a 100 mila',
            'da 100 mila a 1 milione',
            'da 1 a 10 milioni',
            'da 10 a 100 milioni',
            'oltre 100 milioni'
        ],
        from, to;

    labels.push(
        '<i style="background:' + getColor(0) + '"></i> ' +
        'Nessun dato OCSE'
    );
    for (var i = 0; i < grades.length; i++) {
        from = grades[i];
        to = grades[i + 1];

        labels.push(
            '<i style="background:' + getColor(from + 1) + '"></i> ' + grades_labels[i]
        );
    }

    div.innerHTML = '<div class"popover-content">' + labels.join('<br>') + '</div>';
    return div;
};

legend.addTo(map);


/* Function to get the internal leaflet ID from an alpha3 code*/
var geojson_layer_from_alpha3 = function(key) {
    var ret;
    geojson.eachLayer(function(layer){
        if (layer.feature.id == key)
            ret = layer;
    });
    return ret;
};
