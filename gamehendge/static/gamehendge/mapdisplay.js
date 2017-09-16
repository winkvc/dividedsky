function initMap() {

  $.getJSON('station_locations/', function(myJsonObject) {
    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 14,
      center: myJsonObject.data[0].position
    });
    
    myJsonObject.data.forEach( function (element) {
      var marker = new google.maps.Marker({
        position: element.position,
        map: map,
        icon: element.icon
      });
    });
    
    function showPosition(position) {
      map.setCenter({lat: position.coords.latitude, lng: position.coords.longitude});
    };
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(showPosition);
    } else {
      alert("Geolocation not supported");
    } 
    });
  
}