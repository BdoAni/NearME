'use strict'
// alert( "this is map" )
// TODO rename file for searching tools 

// Note: This example requires that you consent to location sharing when
// prompted by your browser. If you see the error "The Geolocation service
// failed.", it means you probably did not give permission for the browser to
// locate you.

let map;


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
            const geocoder = new google.maps.Geocoder();
            for(let tool of toolResults){
                createToolMarkerOnMap(map, tool, geocoder)
            }
        })
    })
};

function createToolMarkerOnMap(map, tool, geocoder){
    geocoder.geocode( { 'address': tool.user_address })
    .then((result)=>{
        const location = result.results[0].geometry.location
        console.log(location)

        new google.maps.Marker({
            position: location,
            map: map,
            title: tool.tool_name
        })
    })


}

document.querySelector('#search_tool_submit').addEventListener('click', showToolsOnMap)

window.showToolsOnMap = showToolsOnMap;
