//Map related js helper function
var map;
var autocomplete;


function initMap(){
    //init map
    if(document.getElementById('map')){
        map = new google.maps.Map(document.getElementById('map'),{
            center:{lat:-34.397, lng:150.644},
            zoom: 10
        });
    }
    if(document.getElementById("street_address") && document.getElementById("locality")
            && document.getElementById("administrative_area_level_1") && document.getElementById("postal_code")){
        autoLocation();
    }

}

//auto complete related js helper function

var componentForm = {
    street_number: 'short_name',
    route: 'long_name',
    locality: 'long_name',
    administrative_area_level_1: 'short_name',
    postal_code: 'short_name'
};

function autoLocation(){
    
    var locationInput = document.getElementById('street_address')
    var options = {
        types: ['geocode'],
        componentRestrictions: {country: "us"}
    };
    autocomplete = new google.maps.places.Autocomplete(locationInput, options);
    autocomplete.addListener('place_changed', fillInAddress);
}


function fillInAddress(){
    var place = autocomplete.getPlace()
    //clean 
    document.getElementById("street_address").value = '';
    document.getElementById("street_address").disabled= false;
    document.getElementById("locality").value=''; 
    document.getElementById("locality").disabled = false;
    document.getElementById("administrative_area_level_1").value='' 
    document.getElementById("administrative_area_level_1").disabled = false
    document.getElementById("postal_code").value=''
    document.getElementById("postal_code").disabled = false

    //set
    var street_address = "";
    for(var i = 0; i < place.address_components.length; i ++){
        var addressType = place.address_components[i].types[0];
        if(componentForm[addressType]){
            if(addressType === 'street_number' || addressType === 'route'){
                var val = place.address_components[i][componentForm[addressType]];
                street_address += val + " ";
            }else{
                var val = place.address_components[i][componentForm[addressType]];
                document.getElementById(addressType).value = val;
            }
        }
    }
    document.getElementById('street_address').value = street_address;
    
}

                                                                                                                                 
