var stationPks = {};
var map;

function getInfoWindow(element) {
  //if (element.)
  var htmlSource = "";
  if (element.station_type == "energy") {
    htmlSource +=
      "<p>Energy: " + element.gathered_energy + "</p>" +
      "<button onClick=collectEnergy(" + element.db_id + ",map)>" + 
        "Collect Energy" + 
      "</button><br>";
  }

  htmlSource +=
    "<button onClick=deleteStation(" + element.db_id + ")>" +
      "Delete" +
    "</button>";


  var infowindow = new google.maps.InfoWindow({
    content: htmlSource
  });
  return infowindow;
};

function renderStation (element, map) {
  var marker = new google.maps.Marker({
    position: element.position,
    map: map,
    icon: element.icon
  });

  // make an infowindow
  var infowindow = getInfoWindow(element);

  // attach listener
  marker.addListener('click', function () {
    infowindow.open(map, marker);
  });

  stationPks[element.db_id] = marker;
};

function collectEnergy(db_id, map) {
  $.post( "station_collect_energy/", 
    {
      'pk' : db_id,
      'latitude' : 44,
      'longitude' : 14
    }, function (reply) {
      var station_json = reply.station_json;
      stationPks[station_json.db_id].setMap(null);
      renderStation(station_json, map);
      //stationPks[station_json.db_id].click();
    }, 'json' );
};

function deleteStation(db_id) {
  // make api request
};

function initMap() {

  $.getJSON('station_locations/', function(myJsonObject) {
    //var myJson = '{"data": [{"position": {"lat": 37.424261, "lng": -122.200397}, "icon": "https://img.pokemondb.net/sprites/ruby-sapphire/normal/ditto.png"}, {"position": {"lat": 37.422808, "lng": -122.19906}, "icon": "https://img.pokemondb.net/sprites/ruby-sapphire/normal/ditto.png"}]}';
    //var myJsonObject = response
    map = new google.maps.Map(document.getElementById('map'), {
      zoom: 14,
      center: myJsonObject.data[0].position
    });
    
    myJsonObject.data.forEach( function(item) {
      renderStation(item, map);
    });
    
    function showPosition(position) {
      map.setCenter({lat: position.coords.latitude, lng: position.coords.longitude});
    };
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(showPosition);
    } else {
      map.setCenter({lat: 37.424261, lng: -122.200397});
    } 
    });
  
}