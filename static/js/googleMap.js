'use strict'
// alert( "this is map" )

// Note: This example requires that you consent to location sharing when
// prompted by your browser. If you see the error "The Geolocation service
// failed.", it means you probably did not give permission for the browser to
// locate you.

let map, infoWindow;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 47.6062, lng: -122.335167 },
    zoom: 8,
    mapTypeControl: false,
  });
  

  
}



window.initMap = initMap;
