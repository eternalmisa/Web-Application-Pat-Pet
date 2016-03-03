searchVisible = 0;
transparent = true;

$(document).ready(function(){
    jQuery.validator.setDefaults({
        debug: true,
        success: "valid"
    });
    $('#username').blur(function(){
       var username = $('#username').val();
       var csrf = getCookie("csrftoken");
       if(username){
          $.post("/checkuser",{name:username, csrfmiddlewaretoken:csrf},
          function(result){
             var ret = eval("("+result+")");
             //alert(ret.result)
             if(ret.result==false){
             $('.errors').html('<span>' + username + ' is already taken</span>');
             }else{
              $('.errors').html('<span></span>');
             }
             });}});
    $('#email').blur(function(){
       var email = $('#email').val();
       var csrf = getCookie("csrftoken");
       if(email){
          $.post("/checkemail",{name:email, csrfmiddlewaretoken:csrf},
          function(result){
             var ret = eval("("+result+")");
             //alert(ret.result)
             if(ret.result==false){
             $('.errors').html('<span>' + email + ' has already been registered</span>');
             }else{
              $('.errors').html('<span></span>');
             }
             });}});
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
        onNext: function(tab, navigation, index){
            if(index == 1){
                return validateFirstStep();
            }

        },
        onTabClick : function(tab, navigation, index){
            // Disable the posibility to click on tabs
            return false;
        }, 
        onTabShow: function(tab, navigation, index) {
            var $total = navigation.find('li').length;
            var $current = index+1;
            
            var wizard = navigation.closest('.wizard-card');
            
            // If it's the last tab then hide the last button and show the finish instead
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

    // Prepare the preview for profile picture
    $("#wizard-picture").change(function(){
        readURL(this);
    });
    
    $('[data-toggle="wizard-radio"]').click(function(){
        wizard = $(this).closest('.wizard-card');
        wizard.find('[data-toggle="wizard-radio"]').removeClass('active');
        $(this).addClass('active');
        $(wizard).find('[type="radio"]').removeAttr('checked');
        $(this).find('[type="radio"]').attr('checked','true');
    });
    
    $('[data-toggle="wizard-checkbox"]').click(function(){
        if( $(this).hasClass('active')){
            $(this).removeClass('active');
            $(this).find('[type="checkbox"]').removeAttr('checked');
        } else {
            $(this).addClass('active');
            $(this).find('[type="checkbox"]').attr('checked','true');
        }
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
			firstname: "required",
			lastname: "required",
			email: {
				required: true,
				email: true
			},username: {
				required: true,
				minlength: 2
			},
			password1: {
				required: true,
				minlength: 3
			},
			password2: {
				required: true,
				minlength: 3,
				equalTo: "#password1"
			},
            address:{
				required: true
			},
            city:{
				required: true
			},
            state:{
				required: true
			},
            zipcode: {
                required:true,
                zipcode: true
            }
		},
		messages: {
		   // username:"Please enter your username",
			firstname: "Please enter your First Name",
			lastname: "Please enter your Last Name",
			email: "Please enter a valid email address",
			username: {
				required: "Please enter a username",
				minlength: "Your username must consist of at least 2 characters"
			},
			password1: {
				required: "Please provide a password",
				minlength: "Your password must be at least 5 characters long"
			},
			password2: {
				required: "Please provide a password",
				minlength: "Your password must be at least 5 characters long",
				equalTo: "Please enter the same password as above"
			},
            address:{
				required: "Please provide an address"
			},
            city:{
				required: "Please provide the city name"
			},
            state:{
				required: "Please provide the state"
			},
            zipcode:{
				required: "Please provide the zip code"
			}
		},
        onfocusout: function(element) { $(element).valid(); }
	}); 
	
	if(!$(".wizard-card form").valid()){
    	//form is invalid
        console.log("not valid")
    	return false;
	}

	return true;
}

 //Function to show image before upload

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#wizardPicturePreview').attr('src', e.target.result).fadeIn('slow');
        }
        reader.readAsDataURL(input.files[0]);
    }
}
    

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) == 0) return c.substring(name.length,c.length);
    }
    return "";
}











