'use strict'

function showToolNavigation(addresses){
    let map;
    if ( !navigator.geolocation) {
        console.error('You mast turn on your location ');
    }
    navigator.geolocation.getCurrentPosition((position) => {
        const userLocation = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
        };
        map = new google.maps.Map(document.getElementById('map'), {
            center: userLocation,
            zoom: 11,
            mapTypeControl: false,
        });
        const geocoder = new google.maps.Geocoder();
        for(let address of addresses){
            createToolMarkerOnMap(map, address, geocoder)
        }
    });
}

function createToolMarkerOnMap(map, address, geocoder){
    geocoder.geocode( { 'address': address })
    .then((result)=>{
        const location = result.results[0].geometry.location
        console.log(location)

        new google.maps.Marker({
            position: location,
            map: map,
            title: address
        })
    })
}
