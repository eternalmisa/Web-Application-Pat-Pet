var flag = true;
var fetch_history_flag = true;
var test
var username = $("#username").val(); 
var started = false;
var socket;
var chatId;
addMessage = function(message, type){
    var text = message
    //make up a new bubble, append it to 
    var clear = $("<div>").addClass("clear");                    
    var conv = $("<div>").addClass("conversation");
    if(type === 2){
        var bubble = $("<div>").addClass("conversation_bubble2");
    }else{
        var bubble = $("<div>").addClass("conversation_bubble1");
    }

    var li = $("<li>");
    bubble.html(text);
    conv.append(bubble);
    conv.append(clear);
    li.append(conv);

    var chat_history = $(".mess_content");
    var chat_history_list = $(".mess_content ul");
    chat_history_list.append(li);
    $("textarea").val(""); 
}                                                                     

launchChatWith = function(pendingUser){
        //first open the window~
        var messenger = $(".mess_bound");
        messenger.removeClass("hide");  
        messenger.hide();
        messenger.fadeIn();

        //get the launch chat url
        var launch_chat_url = "/launchChat/" + pendingUser 
        $.ajax({url: launch_chat_url, success: function(result){
            chatId = result['chatId'];

            //add video button
            var video_btn = $(".send_videorequest_btn");
            video_btn.on("click", function(){
                //make up a new bubble, append it to 
                text = username + " send a video chat request";
                addVideoRequestMessage(text , username, pendingUser,2, true);
                var chat_history = $(".mess_content");
                var chat_history_list = $(".mess_content ul");                                                                  
                //open video chat window
                var videourl = getRootUrl();
                videourl = videourl.replace(/^http:\/\//i, 'https://');
                var videoindow = window.open(videourl+"video/?roomid="+chatId, "", "width=500, height=375");
                                                                                                                                 
                //scroll down
                chat_history.animate({ scrollTop: chat_history_list.height() }, 1000);
                socket.send({room: chatId, action:'videorequest', message:text, user:username, user2:pendingUser});
                send_btn.attr("disabled", "disabled");
                                                                                                                                 
            });

            //socket configuration
            if(!started){
                socket = socket_config(chatId);
                                                                                          
                //fetch history chat
                if(fetch_history_flag){
                    var get_history_chat_url= "/getHistoryChats/"+chatId;
                                                                                              
                    $.ajax({url: get_history_chat_url, success: function(result){
                        //alert(typeof(result))
                        for (i = 0; i < result.length; i++){
                            var data = JSON.parse(result[i][0]);
                            var ifexpire = Boolean(result[i][1]);
                            var message = data['message'];

                            var type; 
                            if(data['user'] === username){
                                type = 2;
                            }else{
                                type = 1;
                            }
                            if(data['action'] == 'message'){
                                addMessage(message, type);
                            }else if(data['action'] == 'invitation'){
                                addInvitationMessage(data['message'], data['start'], data['end'], data['user'],data['petowner'],data['petname'],data['petid'],type, ifexpire);
                            }else if(data['action'] == 'accept'){
                                addAcceptMessage(data['message'], data['start'], data['end'], data['user'],data['petowner'],data['petname'],data['petid'],data['url'], type);
                            }else if(data['action'] == 'reject'){
                                addRejectMessage(data['message'], data['start'], data['end'], data['user'],data['petowner'],data['petname'],data['petid'], type);
                            }else if(data['action'] == 'videorequest'){
                                addVideoRequestMessage(data['message'], data['user'], data['user2'], type, ifexpire);
                            }else if(data['action'] == 'rejectvideo'){
                                addRejectVideoRequestMessage(data['message'], data['user'], data['user2'], type);
                            }else if(data['action'] == 'acceptvideo'){
                                addAcceptVideoRequestMessage(data['message'], data['user'], data['user2'], type);
                            }

                        }
                        var chat_history = $(".mess_content");
                        var chat_history_list = $(".mess_content ul");
                        chat_history.animate({ scrollTop: chat_history_list.height() }, 100);
                        fetch_history_flag = false; 
                    }});
                }
            }
        }});

        //find the button
        var send_btn = $(".send_mess_btn");
                                                                                                                                     
        send_btn.on("click", function(){
            //get content from text_area
            var text = $("textarea").val();
            
            //make up a new bubble, append it to 
            addMessage(text,2);
            var chat_history = $(".mess_content");
            var chat_history_list = $(".mess_content ul");                                                                  
            
            var chat_history = $(".mess_content");
            var chat_history_list = $(".mess_content ul");
                                                                                                                                     
            //scroll down
            chat_history.animate({ scrollTop: chat_history_list.height() }, 1000);
            socket.send({room: chatId, action:'message', message:text, user:username });
            flag = false;
                                                                                                                                     
        });
                                                                                                                                     
        //Some cute js for message window
        var ta = $(".mess_panel textarea");
        ta.on("keyup",  function(e){
                var text = $("textarea").val();
                if(text.trim().length > 0){
                    send_btn.removeAttr("disabled");
                }else{
                    send_btn.attr("disabled", "disabled");
                    return true;
                }
                e = e || event;
                if (e.keyCode === 13) {
                    //make up a new bubble, append it to 
                    addMessage(text, 2);
                    var chat_history = $(".mess_content");
                    var chat_history_list = $(".mess_content ul");                                                                  
                    //scroll down
                    chat_history.animate({ scrollTop: chat_history_list.height() }, 1000);
                    socket.send({room:chatId, action:'message', message:text, user:username});
                    flag = false;
                    send_btn.attr("disabled", "disabled");
                }
                return true;

        });

        
}


addMessageInDashboard = function(type, pendingUser){
    var pendingMessageDiv = $("<div>").addClass(type)
        .append(
            $("<div>").addClass("title").addClass("hide").html("Pending Message")
        ).append(
            $("<div>").addClass("message-box")
                .append(
                    $("<span>").html("New message from ")
                ).append(
                    $("<a>").attr("href", "/person_profile/1").html(pendingUser)
                ).append(
                    $("<div>").addClass("buttons")
                        .append(
                            $("<button>").attr("type", "button").addClass("btn")
                                .addClass("btn-sm").addClass("btn-info")
                                .html("Chat with " + pendingUser)
                        ).append(" ")
                        .append(
                            $("<button>").attr("type", "button")
                                .addClass("btn")
                                .addClass("btn-sm").addClass("btn-warning")
                                .html("Reject")
                    )

                )
        ).append(
            $("<div>").addClass("line")
        );
    
    pendingMessageDiv.find(".btn-info").on('click', function(){
            launchChatWith(pendingUser)
            $.get("/setPendingChatRoomUnPending/" +pendingUser, function(){
                pendingMessageDiv.fadeOut();
            });
    });

    pendingMessageDiv.find(".btn-warning").on('click', function(){
            $.get("/setPendingChatRoomUnPending/"+pendingUser, function(result){
                pendingMessageDiv.fadeOut();
            });
    });

    $(".pending-message.panel-body").append(pendingMessageDiv);

}

addMessageInDashboard2 = function(type, pendingUser){
    var pendingMessageDiv = $("<div>").addClass(type)
        .append(
            $("<div>").addClass("title").addClass("hide").html("Pending Message")
        ).append(
            $("<div>").addClass("message-box")
                .append(
                    $("<span>").html("Chat with ")
                ).append(
                    $("<a>").attr("href", "/person_profile/1").html(pendingUser)
                ).append(
                    $("<div>").addClass("buttons")
                        .append(
                            $("<button>").attr("type", "button").addClass("btn")
                                .addClass("btn-sm").addClass("btn-info")
                                .html("Chat with " + pendingUser)
                        )
                )
        ).append(
            $("<div>").addClass("line")
        );
    
    pendingMessageDiv.find(".btn-info").on('click', function(){
            launchChatWith(pendingUser)
    });

    $(".all-message.panel-body").append(pendingMessageDiv);

}
//scroll down
main = function(){

    var fetchPendingChatRoom = function(){
        $.ajax({url: "/getPendingChatRoom", success: function(result){
            $(".pending-message.panel-body").html("");
            for(i = 0;  i < result.length; i ++){
                if(result[i] != username)
                    addMessageInDashboard("pending", result[i]);
            }
        }});
    }

    var fetchAllChatRoom = function(){
        $.ajax({url: "/getAllRelatedChatRoom", success: function(result){
            $(".all-message.panel-body").html("");
            for(i = 0;  i < result.length; i ++){
                if(result[i] != username)
                    addMessageInDashboard2("all", result[i]);
            }
        }});
    }

    fetchPendingChatRoom();
    fetchAllChatRoom();
    setInterval(fetchPendingChatRoom, 5000);
    setInterval(fetchAllChatRoom, 5000);
    //some fansy effect
    $(".draggable").draggable();
    $(".mess_topbar .close_btn").on('click', function(){
        var messenger = $(".mess_bound");
        messenger.fadeOut();
        messenger.addClass("hide");  
    });


}

var socket_config = function(chatId){

    //js for socket io.... I hate it ...seriously...
    var socket;

    var connected = function() {
        socket.subscribe(chatId);
        started = true;
    };
                                                                           
    var disconnected = function() {
        setTimeout(socketstart, 1000);
    };
                                                                           

    var messaged = function(data) {
        switch (data.action) {
            case 'in-use':
                alert('Name is in use, please choose another');
                break;
            case 'accept':
                if(data['user'] != username){
                    addAcceptMessage(data['message'], data['start'], data['end'], data['user'],data['petowner'],data['petname'],data['petid'],data['url'], 1);
                }else{
                    addAcceptMessage(data['message'], data['start'], data['end'], data['user'],data['petowner'],data['petname'],data['petid'],data['url'], 2);
                }
                var chat_history = $(".mess_content");
                var chat_history_list = $(".mess_content ul");
                chat_history.animate({ scrollTop: chat_history_list.height() }, 100);
                break;

            case 'acceptvideo':
                if(data['user'] != username){
                    addAcceptVideoRequestMessage(data['message'], data['user'],data['user2'], 1);
                }else{
                    addAcceptVideoRequestMessage(data['message'], data['user'],data['user2'], 2);
                }
                var chat_history = $(".mess_content");
                var chat_history_list = $(".mess_content ul");
                chat_history.animate({ scrollTop: chat_history_list.height() }, 100);
                break;

            case 'reject':
                if(data['user'] != username){
                    addRejectMessage(data['message'], data['start'], data['end'], data['user'],data['petowner'],data['petname'],data['petid'],1);
                }else{
                    addRejectMessage(data['message'], data['start'], data['end'], data['user'],data['petowner'],data['petname'],data['petid'],2);
                }
                var chat_history = $(".mess_content");
                var chat_history_list = $(".mess_content ul");
                chat_history.animate({ scrollTop: chat_history_list.height() }, 100);
                break;

            case 'rejectvideo':
                if(data['user'] != username){
                    addRejectVideoRequestMessage(data['message'], data['user'],data['user2'], 1);
                }else{
                    addRejectRequestMessage(data['message'], data['user'],data['user2'], 2);
                }
                var chat_history = $(".mess_content");
                var chat_history_list = $(".mess_content ul");
                chat_history.animate({ scrollTop: chat_history_list.height() }, 100);
                break;

            case 'invitation':
                if(data['user'] != username){
                    addInvitationMessage(data['message'], data['start'], data['end'], data['user'],data['petowner'],data['petname'],data['petid'],1, false);
                    var chat_history = $(".mess_content");
                    var chat_history_list = $(".mess_content ul");
                    chat_history.animate({ scrollTop: chat_history_list.height() }, 100);
                }
                break;
            case 'videorequest':
                if(data['user'] != username){
                    addVideoRequestMessage(data['message'], data['user'], data['user2'], 1, false);
                    var chat_history = $(".mess_content");
                    var chat_history_list = $(".mess_content ul");
                    chat_history.animate({ scrollTop: chat_history_list.height() }, 100);
                }
                break;

            case 'message':
                if(flag){
                    addMessage(data['message'], 1);
                    var chat_history = $(".mess_content");
                    var chat_history_list = $(".mess_content ul");
                    chat_history.animate({ scrollTop: chat_history_list.height() }, 100);
                }
                flag = true;
                break;
        }
    };


    var socketstart = function(){
        socket = new io.Socket();
        socket.connect();
        socket.on('connect', connected);
        socket.on('disconnect', disconnected);
        socket.on('message', messaged);
    };
    socketstart();
    return socket; 
}

$(document).ready(main);

var addAcceptMessage = function(text, start_date, end_date, username, petownername, petname, petid, url, type){
    var clear = $("<div>").addClass("clear");                    
    var conv = $("<div>").addClass("conversation");
    if(type === 2){
        var bubble = $("<div>").addClass("conversation_bubble2");
    }else{
        var bubble = $("<div>").addClass("conversation_bubble1");
    }
    var li = $("<li>");
    bubble.html(text);
    bubble.append(
        $("<div>").css('color','#9e9e9e').html(
            "Request on " + petname + " accepted! Check the following URL:"
        )
    ).append(
        $("<a>").css('color','#03A9F4').attr("href", url).html("Click here to check")
    ).append(
        $("<div>").css('color','#9e9e9e').html(
            "From: " + start_date + " To: " + end_date
        ) 
    );
    conv.append(bubble);
    conv.append(clear);
    li.append(conv);
                                                                  
    var chat_history = $(".mess_content");
    var chat_history_list = $(".mess_content ul");
    chat_history_list.append(li);
    $("textarea").val(""); 

}

var addRejectMessage = function(text, start_date, end_date, username, petownername, petname, petid, type){
    var clear = $("<div>").addClass("clear");                    
    var conv = $("<div>").addClass("conversation");
    if(type === 2){
        var bubble = $("<div>").addClass("conversation_bubble2");
    }else{
        var bubble = $("<div>").addClass("conversation_bubble1");
    }
    var li = $("<li>");
    bubble.html(text);
    bubble.append(
        $("<div>").css('color','#9e9e9e').html(
            "Request on " + petname + " rejected"
        )
    ).append(
        $("<div>").css('color','#9e9e9e').html(
            "From: " + start_date + " To: " + end_date
        ) 
    );
    conv.append(bubble);
    conv.append(clear);
    li.append(conv);
                                                                  
    var chat_history = $(".mess_content");
    var chat_history_list = $(".mess_content ul");
    chat_history_list.append(li);
    $("textarea").val(""); 

}

var addInvitationMessage = function(text, start_date, end_date, username, petownername, petname, petid, type, ifexpire){
    //make up a new bubble, append it to 
    var clear = $("<div>").addClass("clear");                    
    var conv = $("<div>").addClass("conversation");
    if(type === 2){
        var bubble = $("<div>").addClass("conversation_bubble2");
    }else{
        var bubble = $("<div>").addClass("conversation_bubble1");
    }
                                                                  
    var li = $("<li>");
    bubble.html(text);
    bubble.append(
        $("<div>").css('color','#9e9e9e').html(
            "From: " + start_date + " To: " + end_date
        ) 
    );

    if(type === 1){
        if(ifexpire){
            //do nothing
        }else{
             bubble.append(
                $("<div>").addClass("ac-rej-btns")
                .append(
                 $("<button>")
                     .addClass("btn-info")
                     .addClass("message-btn")
                     .html("Accept")
                     .on("click", function(){
                         socket.send({room:chatId, user:username, petid:petid, action:"accept", message: "I'm glald to accept your request!", start: start_date, end: end_date, petname: petname, user: petownername}); 
                        $(this).parent(".ac-rej-btns").fadeOut();
                     })
                ).append(
                    $("<button>")
                     .addClass("btn-warning")
                     .addClass("message-btn")
                     .html("Reject")
                     .on("click", function(){
                         socket.send({room:chatId, user:username, petid:petid, action:"reject", message: "Sry, maybe next time.", start: start_date, end: end_date, petname: petname, user: petownername}); 
                        $(this).parent(".ac-rej-btns").fadeOut();
 
                    })
                )
             )
        }
    }

    conv.append(bubble);
    conv.append(clear);
    li.append(conv);
                                                                  
    var chat_history = $(".mess_content");
    var chat_history_list = $(".mess_content ul");
    chat_history_list.append(li);
    $("textarea").val(""); 
}


var addVideoRequestMessage= function(text, username, petownername, type, ifexpire){
    //make up a new bubble, append it to messenger window
    var clear = $("<div>").addClass("clear");                    
    var conv = $("<div>").addClass("conversation");
    if(type === 2){
        var bubble = $("<div>").addClass("conversation_bubble2");
    }else{
        var bubble = $("<div>").addClass("conversation_bubble1");
    }
                                                                  
    var li = $("<li>");
    bubble.html(text);

    if(type === 1){
        if(ifexpire){
            //do nothing
        }else{
            bubble.append(
                $("<div>").addClass("ac-rej-btns")
                .append(
                    $("<button>").addClass("btn-info")
                        .addClass("message-btn")
                        .html("Start Chatting")
                        .on("click", function(){
                            socket.send({room:chatId, user:username, user2: username, action:"acceptvideo", message: "Let's Start Chat!", user: petownername}); 
                            var videourl = getRootUrl();
                            videourl = videourl.replace(/^http:\/\//i, 'https://');
                            var videoindow = window.open(videourl + "video/?roomid="+chatId, "", "width=500, height=375");
                            $(this).parent(".ac-rej-btns").fadeOut();
                        })
                ).append(
                    $("<button>")
                        .addClass("btn-warning")
                        .addClass("message-btn")
                        .html("Reject")
                        .on("click", function(){
                            socket.send({room:chatId, user:username, user2: username,action:"rejectvideo", message: "Video chat request rejected.",  user: petownername}); 
                            $(this).parent(".ac-rej-btns").fadeOut();
                    })
                )
            )
        }
    }

    conv.append(bubble);
    conv.append(clear);
    li.append(conv);
                                                                  
    var chat_history = $(".mess_content");
    var chat_history_list = $(".mess_content ul");
    chat_history_list.append(li);                                                 
    $("textarea").val(""); 
 }
 
var addAcceptVideoRequestMessage= function(text, username, petownername, type){
    var clear = $("<div>").addClass("clear");                    
    var conv = $("<div>").addClass("conversation");
    if(type === 2){
        var bubble = $("<div>").addClass("conversation_bubble2");
    }else{
        var bubble = $("<div>").addClass("conversation_bubble1");
    }
    var li = $("<li>");
    bubble.html(text);
    bubble.append(
        $("<div>").css('color','#9e9e9e').html(
            "Video Chat Accepted:)"
        )
    );

    conv.append(bubble);
    conv.append(clear);
    li.append(conv);
                                                                  
    var chat_history = $(".mess_content");
    var chat_history_list = $(".mess_content ul");
    chat_history_list.append(li);
    $("textarea").val(""); 
}

var addRejectVideoRequestMessage= function(text, username, petownername, type){
    var clear = $("<div>").addClass("clear");                    
    var conv = $("<div>").addClass("conversation");
    if(type === 2){
        var bubble = $("<div>").addClass("conversation_bubble2");
    }else{
        var bubble = $("<div>").addClass("conversation_bubble1");
    }
    var li = $("<li>");
    bubble.html(text);
    bubble.append(
        $("<div>").css('color','#9e9e9e').html(
            "Video Chat Rejected:("
        )
    );
    conv.append(bubble);
    conv.append(clear);
    li.append(conv);
                                                                  
    var chat_history = $(".mess_content");
    var chat_history_list = $(".mess_content ul");
    chat_history_list.append(li);
    $("textarea").val(""); 
}
function getRootUrl() {
    return window.location.origin?window.location.origin+'/':window.location.protocol+'/'+window.location.host+'/';
}
