// JavaScript Document
var main = function() {
    $(".edit_basic_btn").click(function() {
        $(".pet_basic_info").animate({opacity: '0.0'});
        $(".edit_pet_basic_info").animate({opacity: '1',top: "90"});
    });

    if($("#error_flag:empty").length == 0){
        $(".edit_pet_basic_info").css({opacity:'0.0'});
        $(".pet_basic_info").css({"opacity": '1'});
    }

	$(".edit_location_btn").click(function() {
        $(".pet_location_info").animate({opacity: '0.0'});
		var distance = $(".pet_location_info").outerHeight() + $("#map").outerHeight();
        $(".edit_location_info").animate({opacity: '1',top: "" + (-distance-140)+"px"});
    });

    if($("#error_flag2:empty").length == 0){
        $(".pet_location_info").css({opacity:'0.0'});
		var distance = $(".pet_location_info").outerHeight() + $("#map").outerHeight();
        $(".edit_location_info").css({"opacity": '1',top: "" + (-distance-140)+"px"});
    }

	$("#upload_picture").change(function(){
        readURL(this);
    });
}
$(document).ready(main)


$.fn.smartFloat = function smartFloat() {
	var position = function(element) {
		var top = element.position().top, pos = element.css("position");
		$(window).scroll(function() {
			var scrolls = $(this).scrollTop();
			if (scrolls > top) {
				if (window.XMLHttpRequest) {
					element.css({
						position: "fixed",
						top: 0
					});	
				} else {
					element.css({
						top: scrolls
					});	
				}
			}else {
				element.css({
					position: pos,
					top: top
				});	
			}
		});
	};
	return $(this).each(function() {
		position($(this));						 
	});
};
$.fn.display = function() {
	var position = function(element) {
		$(window).scroll(function() {
			var scrolls = $(this).scrollTop();
			if (scrolls > 400) {
				if (window.XMLHttpRequest) {
					element.css({
						position: "fixed",
						top: 0,
						display:"block"
					});


				} else {
					element.css({
						display:"none"
					});	
				}
			}else {
				element.css({
					display:"none"
				});	
			}
		});
	};
	return $(this).each(function() {
		position($(this));						 
	});
};
$("#float").smartFloat();
$("#bar2").display();
$(document).ready(function () {			
	$('#request-form input').datepicker({
		todayBtn: "linked"
	});

	$("#edit_basic_form").validate({
		rules: {
			breed: "required",
			gender: "required",
			color: "required",
			age: {
				required: true,
				number: true,
				range: [0, 20]
			},
			pet_bio: "required"
		},
		messages: {
			gender: "Please enter your pet's gender!",
			breed: "Please enter your pet's breed!",
			color: "Please enter your pet's color!",
			age:  {
				required: "Please enter your pet's age!",
				number: "Pet age must be a number",
				range: "The age cannot be larger than 20"
			},
			pet_bio:{
				pet_bio: "Please enter the biography!"
			}
		}
	});
	jQuery.validator.addMethod("zipcode", function(value, element) {
            return this.optional(element) || /\d{5}-\d{4}$|^\d{5}$/.test(value)
        }, "The specified US ZIP Code is invalid");
	$("#edit_location_form").validate({
		rules: {
			pet_address: "required",
			pet_city: "required",
			pet_state: "required",
			pet_zipcode: {
                required:true,
                zipcode: true
            }
		},
		messages: {
			pet_address: "Please enter the specific address!",
			pet_city: "Please enter the city!",
			pet_state: "Please enter the state!",
			pet_zipcode: {
				required: "Please provide the zip code"
			}
		}
	});
});

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#pet_avatar').attr('src', e.target.result).fadeIn('slow');
        }
        reader.readAsDataURL(input.files[0]);
    }
}
