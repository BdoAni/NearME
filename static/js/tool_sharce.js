'use strict'

let directionsRenderer;
let geocoder;
let directionsService;


function showToolNavigation(addresses) {
    let map;
    if (!navigator.geolocation) {
        console.error('You mast turn on your location ');
    }
    navigator.geolocation.getCurrentPosition((position) => {
        const userLocation = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
        };
        map = new google.maps.Map(document.getElementById('map'), {
            center: userLocation,
            zoom: 12,
            mapTypeControl: false,
        });
        geocoder = new google.maps.Geocoder();
        for (let toolAddress of toolAddresses) {
            createToolMarkerOnMap(map, toolAddress, geocoder)
        }
    });
}


function createToolMarkerOnMap(map, address, geocoder) {
    geocoder.geocode({ 'address': address })
        .then((result) => {
            const location = result.results[0].geometry.location
            console.log(location)
            // making markers my changes suppose to go here: 
           var marker = new google.maps.Marker({
                position: location,
                map: map,
                title: address
            });

            const contentString = ` 
            <p>  <a href="http://maps.google.com/maps?q=${address}" >${address} </a> </p>
        `;
            const infoWindow = new google.maps.InfoWindow({
                content: contentString
            });

            marker.addListener('click', () => {
                calcRoute(address, map)
                infoWindow.open({
                    anchor: marker,
                    map: map
                });

            });
        });
}

function calcRoute(address, map) {
    console.log('calculating route')
    directionsService = new google.maps.DirectionsService();
    if (directionsRenderer){
        directionsRenderer.setMap(null)
    }
    directionsRenderer = new google.maps.DirectionsRenderer();
    directionsRenderer.setMap(map)
    var request = {
        origin: userAddress,
        destination: address,
        travelMode: "DRIVING",

    };
    directionsService
        .route(request)
        .then((response) => {
            console.log('rendoring directions')
            directionsRenderer.setDirections(response);
        })
}




window.addEventListener('load', showToolNavigation)
window.showToolNavigation = showToolNavigation;