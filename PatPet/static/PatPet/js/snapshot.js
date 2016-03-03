document.getElementById('takephoto').addEventListener('click', function(){
    var capture = document.getElementById('capture');
    capture.style.display = "block";
    (function(){
        function userMedia(){
            return navigator.getUserMedia = navigator.getUserMedia ||
            navigator.webkitGetUserMedia ||
            navigator.mozGetUserMedia ||
            navigator.msGetUserMedia || null;
        }

        // Now we can use it
        if( userMedia() ){
            document.getElementById('takephoto').style.display = "none";
            var videoPlaying = false;
            var constraints = {
                video: true,
                audio:false
            };
            var video = document.getElementById('snapshot');
            var media = navigator.getUserMedia(constraints, function(stream){

                // URL Object is different in WebKit
                var url = window.URL || window.webkitURL;

                // create the url and set the source of the video element
                video.src = url ? url.createObjectURL(stream) : stream;

                // Start the video
                video.play();
                videoPlaying  = true;
            }, function(error){
                console.log("ERROR");
                console.log(error);
            });


            // Listen for user click on the "take a photo" button
            document.getElementById('take').addEventListener('click', function(){
                if (videoPlaying){
                    capture.style.display = "none";

                    var canvas = document.getElementById('canvas');
                    canvas.width = video.videoWidth;
                    canvas.height = video.videoHeight;
                    canvas.getContext('2d').drawImage(video, 0, 0);
                    //console.log(canvas.getContext('2d').drawImage(video, 0, 0));
                    var data = canvas.toDataURL('image/webp');

                    var avatar = document.getElementById('wizardPicturePreview')
                    if (avatar != null) {
                        document.getElementById('wizardPicturePreview').setAttribute('src', data);
                    } else {
                        document.getElementById('wizardPicturePreview2').setAttribute('src', data);
                    }
                }
            }, false);
            document.getElementById('cancel').addEventListener('click', function(){
                capture.style.display = "none";
            }, false);

        } else {
            console.log("KO");
        }
        document.getElementById('takephoto').style.display = "block";
    })(window);

}, false);