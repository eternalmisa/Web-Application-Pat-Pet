    function init() {
        var button = document.getElementById('upload');
        var canvas = document.getElementById('canvas');
        var form = document.getElementById("submitForm");
        var ctx = canvas.getContext('2d');
        drawDemo(ctx);
        initUpload(canvas, button,form);
    }
    function drawDemo(ctx) {
        ctx.fillRect(25,25,100,100);
        ctx.clearRect(45,45,60,60);
        ctx.strokeRect(50,50,50,50);
    }
    function initUpload(canvas, button, form) {
        button.onclick = function() {
            console.log("click");
            console.log(form);
            var xhr = new XMLHttpRequest();
            var formData = new FormData(form);
            var dataURI = canvas.toDataURL();
            console.log(dataURI);
            if (dataURI != "data:image/png;base64,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") {
                console.log("bushi");
                var blob = dataURItoBlob(dataURI);
                console.log(blob);
                var parts = [blob, new ArrayBuffer()]
                var myFile = new File(parts, 'upload.jpg', {
                            type: "image/png"
                });
                formData.append('upload', myFile);
            }
            console.log(formData);
            var csrftoken = getCookie('csrftoken');
            var url = form.getAttribute('action');
            if (validateSignUpForm()) {
                xhr.open('POST', url, true);
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                xhr.onload = function(e) {
                console.log(xhr.status);
                console.log(xhr.readyState);
                console.log("hi");
                console.log("ruirui"+xhr.responseText);
                if (xhr.responseText == "True") {
                    window.location.replace("/login/go_active");
                } else if (xhr.responseText == "EditSuccess") {
                    window.location.replace("/myprofile");
                }else {
                    $("#sign-err").html('<span class="glyphicon glyphicon-exclamation-sign"></span> ' + xhr.responseText);
				    $("#sign-err").show();
                }
            };

            console.log(formData);
            xhr.send(formData);
            }
            return false;

        }
    }
    function dataURItoBlob(dataURI) {
        // convert base64 to raw binary data held in a string
        // doesn't handle URLEncoded DataURIs - see SO answer #6850276 for code that does this
        var byteString = atob(dataURI.split(',')[1]);
        // separate out the mime component
        var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
        // write the bytes of the string to an ArrayBuffer
        var ab = new ArrayBuffer(byteString.length);
        var dw = new DataView(ab);
        for (var i = 0; i < byteString.length; i++) {
            dw.setUint8(i, byteString.charCodeAt(i));
        }
        // write the ArrayBuffer to a blob, and you're done
        return new Blob([ab], {type: mimeString});
    }

    // CSRF set-up copied from Django docs
      function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
      }

    function validateSignUpForm(){
    console.log("validate1Step");
    jQuery.validator.addMethod("zipcode", function(value, element) {
            return this.optional(element) || /\d{5}-\d{4}$|^\d{5}$/.test(value)
        }, "The specified US ZIP Code is invalid");
    jQuery.validator.addMethod("phoneNum",function(a,b){
        return a=a.replace(/\s+/g,""),this.optional(b)||a.length>9&&a.match(/^(\+?1-?)?(\([2-9]([02-9]\d|1[02-9])\)|[2-9]([02-9]\d|1[02-9]))-?[2-9]([02-9]\d|1[02-9])-?\d{4}$/)},
        "Please specify a valid phone number");

    $("#submitForm").validate({
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
            },
            phoneNum: {
                required: false,
                phoneNum: true
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

	if(!$("#submitForm").valid()){
    	//form is invalid
        console.log("not valid")
    	return false;
	}

	return true;
}

    $(document).ready(init());
