var stationPks = {};
var map;
var userPosition;
var directionsDisplay;
var directionsService;

function displayEnergyValue(energyValue) {
  $("#energy").html('Energy: ' + energyValue);
}

function clearStationPath() {
  directionsDisplay.setDirections({routes: []});
}

function renderStationPath(element) {
  // also call the current request
  if (element.target !== undefined) {
    var start = {lat : +element.position.lat, lng : +element.position.lng};
    var end = {lat : +element.target.lat, lng : +element.target.lng}
    directionsService.route({
      origin: start,
      destination: end,
      travelMode: 'DRIVING'
    }, function(response, status) {
      if (status === 'OK') {
        directionsDisplay.setDirections(response);
      } else {
        window.alert('Directions request failed due to ' + status);
      }
    });
  }
}

function getInfoWindow(element) {
  //if (element.)
  var htmlSource = "";
  if (element.station_type === "energy") {
    htmlSource +=
      "<p>Energy: " + element.gathered_energy + "</p>" +
      "<button onClick=collectEnergy(" + element.db_id + ",map,userPosition)>" + 
        "Collect Energy" + 
      "</button><br>";
  }
  else {
    htmlSource +=
      //"<p id='loading-text-" + element.db_id + "'>Loading path...</p>" +
      "<button id='button-" + element.db_id + 
      "' onClick=changeTargetButtonPress(" + element.db_id + ",map,userPosition)>" + 
        "Change Target" + 
      "</button><br>";

    
  }

  htmlSource +=
    "<button onClick=deleteStation(" + element.db_id + ")>" +
      "Delete" +
    "</button>";


  var infowindow = new google.maps.InfoWindow({
    content: htmlSource
  });
  google.maps.event.addListener(infowindow, 'closeclick', function(){
    clearStationPath();
  });

  return infowindow;
};

function renderStation (element, map) {
  var marker = new google.maps.Marker({
    position: {lat : +element.position.lat, lng : +element.position.lng},
    map: map,
    icon: element.icon
  });

  // make an infowindow
  var infowindow = getInfoWindow(element);

  // attach listener
  marker.addListener('click', function () {
    infowindow.open(map, marker);
    renderStationPath(element);
  });

  stationPks[element.db_id] = marker;
};

function initMap() {

  $.getJSON('station_locations/', function(myJsonObject) {
    
    directionsDisplay = new google.maps.DirectionsRenderer({
      markerOptions: {
        visible : false,
      }
    });
    directionsService = new google.maps.DirectionsService;

    map = new google.maps.Map(document.getElementById('map'), {
      zoom: 14,
      // TODO: unhardcode the center data??
      center: {lat: 37.424261, lng: -122.200397}
    });

    directionsDisplay.setMap(map);
    
    myJsonObject.data.forEach( function(item) {
      renderStation(item, map);
    });

    function setPosition(position) {
      userPosition = {lat: position.coords.latitude, lng: position.coords.longitude};
    };

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        function(position) {
          setPosition(position);
          map.setCenter({lat: position.coords.latitude, lng: position.coords.longitude});
        });
    } else {
      map.setCenter({lat: 37.424261, lng: -122.200397});
    } 
  });
};

function collectEnergy(db_id, map, userPosition) {

  $.post( "station_collect_energy/", 
    {
      'pk' : db_id,
      'latitude' : userPosition.lat,
      'longitude' : userPosition.lng
    }, function (reply) {
      if (reply.error) {
        alert(reply.error);
      } else {
        var station_json = reply.station_json;
        stationPks[station_json.db_id].setMap(null);
        renderStation(station_json, map);
        google.maps.event.trigger(stationPks[station_json.db_id], 'click');
        displayEnergyValue(reply.energy);
      }
    }, 'json' );
};

function changeTargetButtonPress(db_id, map, userPosition) {
  // make a note that the next tower selected should be chosen

};

function deleteStation(db_id) {
  $.post( "delete_station/", 
    {
      'pk' : db_id
    }, function (reply) {
      if (reply.error) {
        alert(reply.error);
      } else {
        stationPks[db_id].setMap(null);
        delete stationPks[db_id];
        displayEnergyValue(reply.energy);
      }
    }, 'json' );
};

function sendBuildTowerRequest(kind, map, userPosition) {
  $.post( "build_station/", 
    {
      'kind' : kind,
      'latitude' : userPosition.lat,
      'longitude' : userPosition.lng
    }, function (reply) {
      if (reply.error) {
        alert(reply.error);
      } else {
        var station_json = reply.station_json;
        renderStation(station_json, map);
        displayEnergyValue(reply.energy);
      }
    }, 'json' );
};

function buildEnergyTower(map, userPosition) {
  sendBuildTowerRequest('energy', map, userPosition);
};

function buildBulletTower(map, userPosition) {
  sendBuildTowerRequest('shooters', map, userPosition);
};

function buildLightningTower(map, userPosition) {
  sendBuildTowerRequest('lightning', map, userPosition);
};

function buildTower(map) {
  // show menu,
  // each option should make an API request

  // TODO: unstub user's position

  // make a marker
  var marker = new google.maps.Marker({
    position: userPosition,
    map: map,
  });

  // make the infowindow and show it
  var htmlSource =
      "<p>Energy Tower: 10 energy, get 1 energy per hour.</p>" +
      "<button onClick='buildEnergyTower(map, userPosition)'>" + 
        "Energy Tower" + 
      "</button><br>" + 
      "<p>Bullet Tower: 10 energy, spawns a bullet mook every thirty minutes.</p>" +
      "<button onClick='buildBulletTower(map, userPosition)'>" + 
        "Bullet Tower" + 
      "</button><br>" + 
      "<p>Lightning Tower: 15 energy, spawns a lightning mook every thirty minutes.</p>" +
      "<button onClick='buildLightningTower(map, userPosition)'>" + 
        "Lightning Tower" + 
      "</button><br>";
  var infowindow = new google.maps.InfoWindow({
    content: htmlSource
  });
  infowindow.open(map, marker);

  // add a callback when the infowindow is closed to delete the marker as well.
  infowindow.addListener('closeclick', function() {
    marker.setMap(null);
  });
};

initMap();