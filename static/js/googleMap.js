'use strict'
// alert( "this is map" )
// TODO rename file for searching tools 

// Note: This example requires that you consent to location sharing when
// prompted by your browser. If you see the error "The Geolocation service
// failed.", it means you probably did not give permission for the browser to
// locate you.

let map, infoWindow;


function showToolsOnMap() {
    if ( !navigator.geolocation) {
        console.error('You mast turn on your location ');
    }
    navigator.geolocation.getCurrentPosition((position) => {
        const userLocation = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
        };
        map = new google.maps.Map(document.getElementById("map"), {
            center: userLocation,
            zoom: 11,
            mapTypeControl: false,
        });
        const searchToolName = document.querySelector("#search_tool_name").value;
        // .then(())
        fetch(`/search?searched=${searchToolName}`)
        .then((toolResults) => toolResults.json())
        .then((toolResults)=>{
            console.log(toolResults);
            // const geocoder = new google.maps.Geocoder();
            // geocoder.geocode( { 'address': searchToolName })
        })
        // .then((result)=>{
        //     console.log(result)
        //     const location = result[0].geometry.location
        //     console.log(location)
        // })
    })
}

document.querySelector('#search_tool_submit').addEventListener('click', showToolsOnMap)

window.showToolsOnMap = showToolsOnMap;
