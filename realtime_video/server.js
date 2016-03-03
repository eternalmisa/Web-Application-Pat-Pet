var static = require('node-static');
var path = require("path");
var http = require('http');
var https = require('https');
var fs = require('fs');
var qs = require('querystring');
var options = {
        key: fs.readFileSync(path.join(__dirname,'/server.key')),
        cert: fs.readFileSync(path.join(__dirname, 'server.crt'))
}

var HTTPSPORT = 443;


//var file = new(static.Server)({'Access-Control-Allow-Origin':'kuoxindeMBP.wv.cc.cmu.edu'});
var file = new(static.Server)(__dirname, {'Access-Control-Allow-Origin':'mujingz.wv.cc.cmu.edu'});

var app = http.createServer(function (req, res) {
    file.serve(req, res);
}).listen(80);


var secureserver = https.createServer(options, function(req, res){
    file.serve(req, res);
});


secureserver.listen(HTTPSPORT, function(){
        console.log("Server listening on : https://localhost:" + HTTPSPORT);
});


var io = require('socket.io').listen(secureserver);
io.sockets.on('connection', function (socket){
	function log(){
		var array = [">>> Message from server: "];
	  for (var i = 0; i < arguments.length; i++) {
	  	array.push(arguments[i]);
	  }
	    socket.emit('log', array);
	}

	socket.on('message', function (message) {
		log('Got message: ', message);
    // For a real app, should be room only (not broadcast)
		socket.broadcast.emit('message', message);
	});

	socket.on('create or join', function (room) {
		var numClients = io.sockets.clients(room).length;

		log('Room ' + room + ' has ' + numClients + ' client(s)');
		log('Request to create or join room', room);

		if (numClients == 0){
			socket.join(room);
			socket.emit('created', room);
		} else if (numClients == 1) {
			io.sockets.in(room).emit('join', room);
			socket.join(room);
			socket.emit('joined', room);
		} else { // max two clients
			socket.emit('full', room);
		}
		socket.emit('emit(): client ' + socket.id + ' joined room ' + room);
		socket.broadcast.emit('broadcast(): client ' + socket.id + ' joined room ' + room);

	});

});

