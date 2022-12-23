'use strict'

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
        const geocoder = new google.maps.Geocoder();
        for (let toolAddress of toolAddresses) {
            createToolMarkerOnMap(map, toolAddress, geocoder)
        }
        calcRoute()
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
                infoWindow.open({
                    anchor: marker,
                    map: map
                });
            });
        });
}

function calcRoute() {
    const directionService = new google.maps.directionService();
    const directionsRendere = new google.maps.directionsRendere();
    var start = document.getElementById('from').value;
    var end = document.getElementById('to').value;
    var request = {
        origin: start,
        destination: end,
        travelMode: "DRIVING",
    };
    directionsService
        .route(request)
        .then((response) => {
            directionsRenderer.setDirections(response);
            const mapOptions = {
                zoom: 7
            };

        })
        
}
// // Allow each marker to have an info window
// google.maps.event.addListener(marker, 'click', (function(marker, i) {
//     return function() {
//         infoWindow.setContent(infoWindowContent[i][0]);
//         infoWindow.open(map, marker);
//         latit = marker.getPosition().lat();
//         longit = marker.getPosition().lng();
//         // console.log("lat: " + latit);
//         // console.log("lng: " + longit);
//     }
// })(marker, i));
// marker.addListener('click', function() {
//     directionsService.route({
//         // origin: document.getElementById('start').value,
//         origin: myLatLng,

//         // destination: marker.getPosition(),
//         destination: {
//             lat: latit,
//             lng: longit
//         },
//         travelMode: 'DRIVING'
//     }, function(response, status) {
//         if (status === 'OK') {
//             directionsDisplay.setDirections(response);
//         } else {
//             window.alert('Directions request failed due to ' + status);
//         }
//     });

// });



window.addEventListener('load', showToolNavigation)
window.showToolNavigation = showToolNavigation;