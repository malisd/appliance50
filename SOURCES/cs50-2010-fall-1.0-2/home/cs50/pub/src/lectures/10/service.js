/****************************************************************************
 * service.js
 *
 * Computer Science 50
 * Problem Set 8
 *
 * Implements a shuttle service.
 ***************************************************************************/


// default height
var HEIGHT = 0.8;

// default latitude
var LATITUDE = 42.3745615030193;

// default longitude
var LONGITUDE = -71.11803936751632;

// default heading
var HEADING = 1.757197490907891;

// default number of seats
var SEATS = 35;

// default velocity
var VELOCITY = 50;


// global reference to shuttle's marker on 2D map
var bus = null;

// global reference to 3D Earth
var earth = null;

// global reference to 2D map
var map = null;

// global reference to shuttle
var shuttle = null;


// load version 1 of the Google Earth API
google.load("earth", "1");

// load version 3 of the Google Maps API
google.load("maps", "3", {other_params: "sensor=false"});


/*
 * void
 * dropoff()
 *
 * Drops up passengers if their stop is nearby.
 */

function dropoff()
{
    alert("TODO");
}


/*
 * void
 * failureCB(errorCode)
 *
 * Called if Google Earth fails to load.
 */

function failureCB(errorCode) 
{
    // report error unless plugin simply isn't installed
    if (errorCode != ERR_CREATE_PLUGIN)
    {
        alert(errorCode);
    }
}


/*
 * void
 * frameend()
 *
 * Handler for Earth's frameend event.
 */

function frameend() 
{
    shuttle.update();
}


/*
 * void
 * initCB()
 *
 * Called once Google Earth has loaded.
 */

function initCB(instance) 
{
    // retain reference to GEPlugin instance
    earth = instance;

    // specify the speed at which the camera moves
    earth.getOptions().setFlyToSpeed(100);

    // show buildings
    earth.getLayerRoot().enableLayerById(earth.LAYER_BUILDINGS, true);

    // prevent mouse navigation in the plugin
    earth.getOptions().setMouseNavigationEnabled(false);

    // instantiate shuttle
    shuttle = new Shuttle({
     heading: HEADING,
     height: HEIGHT,
     latitude: LATITUDE,
     longitude: LONGITUDE,
     planet: earth,
     velocity: VELOCITY
    });

    // synchronize camera with Earth
    google.earth.addEventListener(earth, "frameend", frameend);

    // synchronize map with Earth
    google.earth.addEventListener(earth.getView(), "viewchange", viewchange);

    // update shuttle's camera
    shuttle.updateCamera();

    // show Earth
    earth.getWindow().setVisibility(true);

    // populate Earth with passengers and houses
    populate();
}


/*
 * boolean
 * keystroke(event, state)
 *
 * Handles keystrokes.
 */

function keystroke(event, state)
{
    // ensure we have event
    if (!event)
    {
        event = window.event;
    }

    // left arrow
    if (event.keyCode == 37)
    {
        shuttle.states.turningLeftward = state;
        return false;
    }

    // up arrow
    else if (event.keyCode == 38)
    {
        shuttle.states.tiltingUpward = state;
        return false;
    }

    // right arrow
    else if (event.keyCode == 39)
    {
        shuttle.states.turningRightward = state;
        return false;
    }

    // down arrow
    else if (event.keyCode == 40)
    {
        shuttle.states.tiltingDownward = state;
        return false;
    }

    // A, a
    else if (event.keyCode == 65 || event.keyCode == 97)
    {
        shuttle.states.slidingLeftward = state;
        return false;
    }

    // D, d
    else if (event.keyCode == 68 || event.keyCode == 100)
    {
        shuttle.states.slidingRightward = state;
        return false;
    }
  
    // S, s
    else if (event.keyCode == 83 || event.keyCode == 115)
    {
        shuttle.states.movingBackward = state;     
        return false;
    }

    // W, w
    else if (event.keyCode == 87 || event.keyCode == 119)
    {
        shuttle.states.movingForward = state;    
        return false;
    }
  
    return true;
}


/*
 * void
 * load()
 *
 * Loads application.
 */

function load()
{
    // embed 2D map in DOM
    var latlng = new google.maps.LatLng(LATITUDE, LONGITUDE);
    map = new google.maps.Map(document.getElementById("map"), {
     center: latlng,
     disableDefaultUI: true,
     mapTypeId: google.maps.MapTypeId.ROADMAP,
     navigationControl: true,
     scrollwheel: false,
     zoom: 17
    });

    // prepare shuttle's icon for map
    bus = new google.maps.Marker({
     icon: "http://maps.gstatic.com/intl/en_us/mapfiles/ms/micons/bus.png",
     map: map,
     title: "you are here"
    });

    // embed 3D Earth in DOM
    google.earth.createInstance("earth", initCB, failureCB);
}


/*
 * void
 * pickup()
 *
 * Picks up nearby passengers.
 */

function pickup()
{
    alert("TODO");
}


/*
 * void
 * populate()
 *
 * Populates Earth with passengers and houses.
 */

function populate()
{
    // mark houses
    for (var house in HOUSES)
    {
        // plant house on map
        new google.maps.Marker({
         icon: "http://google-maps-icons.googlecode.com/files/home.png",
         map: map,
         position: new google.maps.LatLng(HOUSES[house].lat, HOUSES[house].lng),
         title: house
        });
    }

    // get current URL, sans any filename
    var url = window.location.href.substring(0, (window.location.href.lastIndexOf("/")) + 1);

    // scatter passengers
    for (var i = 0; i < PASSENGERS.length; i++)
    {
        // pick a random building
        var building = BUILDINGS[Math.floor(Math.random() * BUILDINGS.length)];

        // prepare placemark
        var placemark = earth.createPlacemark("");
        placemark.setName(PASSENGERS[i].name + " to " + PASSENGERS[i].house);

        // prepare icon
        var icon = earth.createIcon("");
        icon.setHref(url + "/passengers/" + PASSENGERS[i].username + ".jpg");

        // prepare style
        var style = earth.createStyle("");
        style.getIconStyle().setIcon(icon);
        style.getIconStyle().setScale(5.0);

        // prepare stylemap
        var styleMap = earth.createStyleMap("");
        styleMap.setNormalStyle(style);
        styleMap.setHighlightStyle(style);

        // associate stylemap with placemark
        placemark.setStyleSelector(styleMap);

        // prepare point
        var point = earth.createPoint("");
        point.setAltitudeMode(earth.ALTITUDE_RELATIVE_TO_GROUND);
        point.setLatitude(building.lat);
        point.setLongitude(building.lng);
        point.setAltitude(2.0);

        // associate placemark with point
        placemark.setGeometry(point);

        // add placemark to Earth
        earth.getFeatures().appendChild(placemark);

        // add marker to map
        var marker = new google.maps.Marker({
         icon: "http://maps.gstatic.com/intl/en_us/mapfiles/ms/micons/man.png",
         map: map,
         position: new google.maps.LatLng(building.lat, building.lng),
         title: PASSENGERS[i].name + " at " + building.name
        });
    }
}


/*
 * void
 * viewchange()
 *
 * Handler for Earth's viewchange event.
 */

function viewchange() 
{
    // keep map centered on shuttle's marker
    var latlng = new google.maps.LatLng(shuttle.position.latitude, shuttle.position.longitude);
    map.setCenter(latlng);
    bus.setPosition(latlng);
}


/*
 * void
 * unload()
 *
 * Unloads Earth.
 */

function unload()
{
    google.earth.removeEventListener(earth.getView(), "viewchange", viewchange);
    google.earth.removeEventListener(earth, "frameend", frameend);
}
