(function(exports) {

exports.URL = exports.URL || exports.webkitURL;

exports.requestAnimationFrame = exports.requestAnimationFrame ||
    exports.webkitRequestAnimationFrame || exports.mozRequestAnimationFrame ||
    exports.msRequestAnimationFrame || exports.oRequestAnimationFrame;

exports.cancelAnimationFrame = exports.cancelAnimationFrame ||
    exports.webkitCancelAnimationFrame || exports.mozCancelAnimationFrame ||
    exports.msCancelAnimationFrame || exports.oCancelAnimationFrame;

navigator.getUserMedia = navigator.getUserMedia ||
    navigator.webkitGetUserMedia || navigator.mozGetUserMedia ||
    navigator.msGetUserMedia;

var ORIGINAL_DOC_TITLE = document.title;
var video = $('#videos');
var canvas = document.createElement('canvas'); // offscreen canvas.
var rafId = null;
var startTime = null;
var endTime = null;
var frames = [];

function $(selector) {
  return document.querySelector(selector) || null;
}

function toggleActivateRecordButton() {
  var b = $('#record-me');
  var p = document.createElement('p');
  //$("#recording").style.display="block";

  //b.textContent = b.disabled ? 'Record' : '        Recording...';
  b.classList.toggle('recording');
  b.disabled = !b.disabled;
}

function turnOnCamera(e) {
  e.target.disabled = true;
  $('#open-camera').style.display = "none";
  $('#camera_display').style.display="block";
  $('#record-me').disabled = false;
  $('#close_record_btn').disabled = false;
  video.controls = false;
  var finishVideoSetup_ = function() {
    setTimeout(function() {
      video.width = 320;//video.clientWidth;
      video.height = 240;
      canvas.width = video.width;
      canvas.height = video.height;
    }, 1000);
  };

  navigator.getUserMedia({video: true}, function(stream) {
    video.src = window.URL.createObjectURL(stream);
    finishVideoSetup_();
  }, function(e) {
    alert('Your browser cannot support getUserMedia()!');
    finishVideoSetup_();
  });
};

function record() {
  var elapsedTime = $('#elasped-time');
  var ctx = canvas.getContext('2d');
  var CANVAS_HEIGHT = canvas.height;
  var CANVAS_WIDTH = canvas.width;

  frames = []; // clear existing frames;
  startTime = Date.now();

  toggleActivateRecordButton();
  $('#stop-me').disabled = false;
  $('#camera_display').style.display = "block";
  $('#video-preview').style.display = "none";
  $('#recording').style.display = "block";
  $('#close_record_btn').disabled = true;
  function drawVideoFrame_(time) {
    rafId = requestAnimationFrame(drawVideoFrame_);

    ctx.drawImage(video, 0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

    document.title = 'Recording...' + Math.round((Date.now() - startTime) / 1000) + 's';

    // Read back canvas as webp.
    //console.time('canvas.dataURL() took');
    var url = canvas.toDataURL('image/webp', 1);
    frames.push(url);

  };

  rafId = requestAnimationFrame(drawVideoFrame_);
};

function stop() {
  cancelAnimationFrame(rafId);
  endTime = Date.now();
  $('#stop-me').disabled = true;
  $("#recording").style.display="none";
  document.title = ORIGINAL_DOC_TITLE;

  toggleActivateRecordButton();

  console.log('frames captured: ' + frames.length + ' => ' +
              ((endTime - startTime) / 1000) + 's video');
  $('#camera_display').style.display = "none";
  $('#video-preview').style.display = "block";
  embedVideoPreview();
};

function embedVideoPreview(opt_url) {
  var url = opt_url || null;
  var video = $('#video-preview video') || null;
  var downloadLink = $('#video-preview a[download]') || null;

  if (!video) {
    video = document.createElement('video');
    video.autoplay = false;
    video.controls = true;
    video.loop = false;
    video.style.width = canvas.width + 'px';
    video.style.height = canvas.height + 'px';
    $('#video-preview').appendChild(video);

    downloadLink = document.createElement('a');
    downloadLink.download = 'capture.webm';
    downloadLink.textContent = '[ Download Video ]';
    downloadLink.title = 'Download your .webm video';
    var pp = document.createElement('br');
    $('#video-preview').appendChild(pp);
    var p = document.createElement('p');
    p.appendChild(downloadLink);

    $('#video-preview').appendChild(p);
  } else {
    window.URL.revokeObjectURL(video.src);
  }


  if (!url) {
    var webmBlob = Whammy.fromImageArray(frames, 1200 / 60);
    url = window.URL.createObjectURL(webmBlob);
  }

  video.src = url;
  downloadLink.href = url;
}

function initEvents() {
  $('#camera-me').addEventListener('click', turnOnCamera);
  $('#record-me').addEventListener('click', record);
  $('#stop-me').addEventListener('click', stop);
}
initEvents();

document.getElementById('close_record_btn').addEventListener('click', function(){
  $('#camera_display').style.display="none";
  $('#open-camera').style.display = "block";
  $('#camera-me').disabled = false;
}, false);

document.getElementById('close_preview_btn').addEventListener('click', function(){
  $('#video-preview').style.display = "none";
  $('#open-camera').style.display = "block";
  $('#camera-me').disabled = false;

}, false);

})(window);
