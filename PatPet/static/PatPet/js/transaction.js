// JavaScript Document



$('.radio_pet').change(function(){ 
	var tmp1 = document.getElementById("input_hidden1");
    tmp1.value = this.value;   
	$('.choice').text( this.value + ' stars' );  
} )

$('.radio_owner').change(function(){ 
	var tmp2 = document.getElementById("input_hidden2");
    tmp2.value = this.value;   
	$('.choice').text( this.value + ' stars' );  
} )
$('.radio_renter').change(function(){
    var tmp3 =  document.getElementById("input_hidden3");
    tmp3.value = this.value;
    $('.choice').text( this.value + ' stars' );
})
$('#myTabs a[href="#pet-review"]').click(function (e) {
  e.preventDefault()
  $(this).tab('show')
})
  $('#myTabs a[href="#owner-review"]').click(function (e) {
  e.preventDefault()
  $(this).tab('show')
})
main = function(){
	

}
$(document).ready(main);
  $('.photo_frame').each(function(){
    var url = $(".photo_pets").html();
    var frame = $(this);
    var img = $("< img />"  ).attr('src', url).on('load', function () {
		frame.find("img").remove();
		if (!this.complete || typeof this.naturalWidth == "undefined" || this.naturalWidth == 0) {
		} else {
			frame.prepend(img);
		}});
  });
function openbox(){
  replyarea=$('#moment_area');
  replyarea.slideToggle();
}
//<button class="delete_photo_btn" style="padding-right:10%" onclick="deletemoment({{activity.id}},{{content.id}})"></button>
function showmomentbox(tid){
   $.get('/getmoments/'+tid,function(data){
   //moment-list-{{activity.id}}
       var momentlist = $("#moment-list-"+tid+"");
       momentlist.empty();
       var moments=data['moments'];
       for (m_num in moments){
          var moment = moments[m_num];
          mid=moment.mid;
          //<button class="delete_photo_btn" style="padding-right:10%" onclick="location.href='{% url 'delete_moment' content.id %}';"></button>
          //id="moment-{{content.id}}
          var html="<li class='list-group-item list-group-item-warning' id='moment-"+mid+"'>";
          html=html+"<button class='delete_photo_btn' style='padding-right:10%' onclick='deletemoment("+tid+","+mid+")'></button><br/>"
          html=html+moment.timestamp+"<br/>"+moment.content+"</li>";
          momentlist.append(html);
       }

   });
}
function addmoment(tid){
  var content=$('#moment_text').val();
  var csrf=getCookie("csrftoken");
  $.post("/upload_moment_content/"+tid,{'content':content,'tid':tid,'csrfmiddlewaretoken':csrf},function(data){
      if (data=="success"){
          showmomentbox(tid);
          $('#moment_text').val("");
          $("#moment-err").hide();
      }else{
      	   $("#moment-err").html('<span class="glyphicon glyphicon-exclamation-sign"></span> ' + data);
		   $("#moment-err").show();
      }


  })

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

function deletemoment(tid,cid){
    $.get("/delete_moment/"+cid);
    moment=$("#moment-"+cid);
    moment.remove();
}