// JavaScript Document
searchVisible = 0;
transparent = true;

$(document).ready(function(){
    $("#wizard-picture").change(function(){
        readURL(this);
    });
    $('#username').blur(function(){
       var username = $('#username').val();
       var csrf = getCookie("csrftoken");
       if(username){
          $.post("/checkuserForEdit",{name:username, csrfmiddlewaretoken:csrf},
          function(result){
             var ret = eval("("+result+")");
             //alert(ret.result)
             if(ret.result==false){
             $('.errors').html('<span>' + username + ' is already taken</span>');
             }else{
              $('.errors').html('<span></span>');
             }
             });
       }});
    
});
function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#wizardPicturePreview').attr('src', e.target.result).fadeIn('slow');
            $('#wizardPicturePreview2').attr('src', e.target.result).fadeIn('slow');
        }
        reader.readAsDataURL(input.files[0]);
    }
}
    












