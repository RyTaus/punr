function initMap() {
  var keck = {lat: 33.9694738, lng: -118.4144247};
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 15,
    center: keck
  });
  var marker = new google.maps.Marker({
    position: keck,
    map: map
  });
}
