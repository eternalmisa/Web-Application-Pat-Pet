main = function(){
    var message_notification = $("span.badge");

    var check_notification = function(){
        $.ajax({url: "/getPendingChatRoom", success: function(result){
            if(result.length > 0){
                message_notification.html(result.length); 
            }else{
                message_notification.html(""); 
            }
        }});
    };
    check_notification()

    setInterval(check_notification, 5000);


}

$(document).ready(main);
