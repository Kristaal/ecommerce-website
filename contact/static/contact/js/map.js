function initMap() {
  var map = new google.maps.Map(document.getElementById("map"), {
      zoom: 12,
      center: {
          lat: 52.2713,
          lng: -9.6999
      }
  });

  var labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

  var locations = [
      { lat: 52.269674, lng: -9.705988 },
  ];

  var markers = locations.map(function(location, i) {
      return new google.maps.Marker({
          position: location,
          label: labels[i % labels.length]
      });
  });

  var markerCluster = new MarkerClusterer(map, markers, { imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m' });
}