searchVisible = 0;
transparent = true;

$(document).ready(function(){
    /*  Activate the tooltips      */
    $('[rel="tooltip"]').tooltip();     
    $('.wizard-card').bootstrapWizard({
        'tabClass': 'nav nav-pills',
        'nextSelector': '.btn-next',
        'previousSelector': '.btn-previous',        
         onInit : function(tab, navigation, index){         
           //check number of tabs and fill the entire row
           var $total = navigation.find('li').length;
           $width = 100/$total;        
           $display_width = $(document).width();           
           if($display_width < 600 && $total > 3){
               $width = 50;
           }           
           navigation.find('li').css('width',$width + '%');          
        },
		/* Validation */
		onNext: function(tab, navigation, index){
            if(index == 1){
                return validateFirstStep();
            }
        },
        onTabClick : function(tab, navigation, index){
            return false;
        }, 
        onTabShow: function(tab, navigation, index) {
            var $total = navigation.find('li').length;
            var $current = index+1;          
            var wizard = navigation.closest('.wizard-card');           
            if($current >= $total) {
                $(wizard).find('.btn-next').hide();
                $(wizard).find('.btn-finish').show();
                $(wizard).find('.btn-backlogin').hide();
            } else {
                $(wizard).find('.btn-next').show();
                $(wizard).find('.btn-finish').hide();
                $(wizard).find('.btn-backlogin').show();
            }
        }
    });

    $("#wizard-picture").change(function(){
        readURL(this);
    });
    $height = $(document).height();
    $('.set-full-height').css('height',$height);


});

function validateFirstStep(){
    console.log("validate1Step");
    jQuery.validator.addMethod("zipcode", function(value, element) {
            return this.optional(element) || /\d{5}-\d{4}$|^\d{5}$/.test(value)
        }, "The specified US ZIP Code is invalid");
    $(".wizard-card form").validate({
		rules: {
			name: "required",
			age: {
                required: true,
                number: true,
                range: [0, 20]
            },
			gender: "required",
			breed: "required",
			color: "required",
			pet_address: "required",
			pet_city: "required",
			pet_state: "required",
			pet_zipcode: {
                required:true,
                zipcode: true
            },
			pet_bio: "required"
		},
		messages: {
			name: "Please enter your pet's name!",
			age:  {
				required: "Please enter your pet's age!",
				number: "Pet age must be a number",
                range: "The age cannot be larger than 20"
			},
			gender: "Please enter your pet's gender!",
			breed: "Please enter your pet's breed!",
			color: "Please enter your pet's color!",
			pet_address: "Please enter the specific address!",
			pet_city: "Please enter the city!",
			pet_state: "Please enter the state!",
			pet_zipcode: {
				required: "Please provide the zip code"
			},
			pet_bio: "Please enter the biography!"
		}
	}); 	
	if(!$(".wizard-card form").valid()){
    	return false;
	}
	return true;
}


function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#wizardPicturePreview').attr('src', e.target.result).fadeIn('slow');
        }
        reader.readAsDataURL(input.files[0]);
    }
}