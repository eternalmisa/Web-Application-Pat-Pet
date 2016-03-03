// JavaScript Document
main = function () {
    //load pets and owners pictures
    $(".pet").each(function () {
        var frame = $(this);
        var pet_id = $(this).find(".pet_id").html();
		var pet_image_url = "/media/"+$(this).find(".pet_image_url").html();
        var is_third = $(this).find(".is_third").html();
        if (is_third == "1") {
            var owner_image_url = $(this).find(".owner_image_url").html();
        } else {
            var owner_image_url = "/media/"+$(this).find(".owner_image_url").html();
        }


        //get pet image
        var img = $("<img />"	).attr('src', pet_image_url).addClass("pet-picture")
            .on('load', function () {
                //replace the old img
                if (!this.complete || typeof this.naturalWidth == "undefined" || this.naturalWidth == 0) {
                    alert('broken image!');
                } else {
                    frame.find(".pet-picture").replaceWith(img);
                }});

        //get owner image
        var img2 = $("<img />"	).attr('src', owner_image_url).addClass("img-circle").addClass("owner-picture")
            .on('load', function () {
                //replace the old img
                if (!this.complete || typeof this.naturalWidth == "undefined" || this.naturalWidth == 0) {
                    alert('broken image!');
                } else {
                    frame.find(".owner-picture").replaceWith(img2);
                }});
    });

}


// JavaScript Document
var map;
function createInfoWindowContent(name, image_url,id) {
    return "<div class='info_window'> Name: <a  href=/pet_profile/" + id +"> "+name + "<br><img class='small_pet_photo' src=/media/" + image_url + "></img></a></div>";
}
                                                                                                                                 
function addMark(lat, lng, name, img_url,id){
    var marker = new google.maps.Marker({
        position: {lat: lat, lng: lng},
        map: map,
        title: name
    });
                                                                                                                                 
    var coordInfoWindow = new google.maps.InfoWindow();
    coordInfoWindow.setContent(createInfoWindowContent(name,img_url,id));
    coordInfoWindow.open(map,marker);
                                                                                                                                 
    marker.addListener('click', function() {
        var currentZoom=map.getZoom();
        map.setZoom(currentZoom + 1);
        map.setCenter(marker.getPosition());
        coordInfoWindow.setContent(createInfoWindowContent(name,img_url,id));
        coordInfoWindow.open(map,marker);
    });
}
                                                                                                                                 
function initMap(){
    //init map
    var bounds = new google.maps.LatLngBounds();
    map = new google.maps.Map(document.getElementById('map'),{
        center:{lat:-34.397, lng:150.644},
        zoom: 8
    });
                                                                                                                                 
    //for each returned search result, add listener
    $('.pet').each(function(){
        //here add this pet to map
        var thismark = $(this);
        var lat = thismark.find('.lat').html();
        var lng = thismark.find('.lng').html();
        var id = thismark.find('.pet_id').html();/////////
        var img_url = thismark.find('.pet_image_url').html();
        var loc = new google.maps.LatLng(lat, lng);
        bounds.extend(loc)
        var name = thismark.find('.name').html();
        addMark(Number(lat), Number(lng), name, img_url,id);
    });
                                                                                                                                 
    //Adjust the bound
    map.fitBounds(bounds);
    map.panToBounds(bounds);
    autoLocation();
}

function autoLocation(){
    var locationInput = document.getElementById('location-input')
    var options = {
        types: ['(cities)'],
        componentRestrictions: {country: "us"}
    };
    var autocomplete = new google.maps.places.Autocomplete(locationInput, options);
}

$(document).ready(main);
                                                                                                                                 
