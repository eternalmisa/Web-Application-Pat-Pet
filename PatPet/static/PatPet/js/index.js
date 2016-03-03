// JavaScript Document
var Autocomplete = function(options) {
    this.form_selector = options.form_selector
    this.url = options.url || '/search/autocomplete/'
    this.delay = parseInt(options.delay || 300)
    this.minimum_length = parseInt(options.minimum_length || 3)
    this.form_elem = null
    this.query_box = null
}

Autocomplete.prototype.setup = function() {
    var self = this

    this.form_elem = $(this.form_selector)
    this.query_box = this.form_elem.find('input[name=q]')

    // Watch the input box.
    this.query_box.on('keyup', function() {
        var query = self.query_box.val()

        if(query.length < self.minimum_length) {
            return false
        }
        self.fetch(query)
    })

    // On selecting a result, populate the search field.
    this.form_elem.on('click', '.ac-result', function(ev) {
        self.query_box.val($(this).text())
        $('.ac-results').remove()
        return false
    })
}

Autocomplete.prototype.fetch = function(query) {
    var self = this

    $.ajax({
        url: this.url
        , data: {
            'q': query
        }
        , success: function(data) {
            self.show_results(data)
        }
    })
}

Autocomplete.prototype.show_results = function(data) {
    // Remove any existing results.
    $('.ac-results').remove()

    var results = data.results || []
    var results_wrapper = $('<div class="ac-results"></div>')
    var base_elem = $('<div class="result-wrapper"><a href="#" class="ac-result"></a></div>')

    if(results.length > 0) {
        for(var res_offset in results) {
            var elem = base_elem.clone()
            // Don't use .html(...) here, as you open yourself to XSS.
            // Really, you should use some form of templating.
            elem.find('.ac-result').text(results[res_offset])
            results_wrapper.append(elem)
        }
    }
    else {
        var elem = base_elem.clone()
        elem.text("No results found.")
        results_wrapper.append(elem)
    }
    this.query_box.after(results_wrapper)
}



main = function () {

    /*
    $('.input-daterange input').datepicker({
        todayBtn: "linked"
    });
    */

    //load rec pets pictures
    $(".rec_pet").each(function () {
        var frame = $(this);
        //get url
        var url = $(this).find(".hidden").html();
        //get image
        var img = $("<img />").attr('src', url).addClass("img-circle").addClass("picture")
            .on('load', function () {
                frame.find("img").remove();
                //replace the old img
                if (!this.complete || typeof this.naturalWidth == "undefined" || this.naturalWidth == 0) {
                    alert('broken image!');
                } else {
                    frame.prepend(img);
                }
            });
    });

    //load pop pets pictures
    $(".pop_pet").each(function () {
        var frame = $(this);
        //get url
        var url = $(this).find(".hidden").html();
        //get image
        var img = $("<img />").attr('src', url).addClass("img-circle").addClass("picture")
            .on('load', function () {
                frame.find("img").remove();
                //replace the old img
                if (!this.complete || typeof this.naturalWidth == "undefined" || this.naturalWidth == 0) {
                    alert('broken image!');
                } else {
                    frame.prepend(img);
                }
            });
    });

    //load videos

    //Search Bar
    var search_breed = $(".search_input_breed");
    //var search_enddate = $(".search_enddate");
    var search_location = $("#location-input");

    var search_btn = $(".search_btn");


    var search_input_valid = function () {
        if (search_breed.val().length == 0
                || search_location.val().length==0){ 
            $(".search_btn").attr("disabled", "disabled");
        } else {
            $(".search_btn").removeAttr("disabled");
        }
    };
    search_input_valid()
    search_breed.on("input", search_input_valid);
    search_location.on("input", search_input_valid);

}

function autoLocation(){
    var locationInput = document.getElementById('location-input')
    var autocomplete = new google.maps.places.Autocomplete(locationInput);
    autocomplete.setTypes(['(cities)']);
}


$(document).ready(main);
