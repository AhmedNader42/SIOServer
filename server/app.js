var express = require('express');
var app = express();
var server = require('http').createServer(app);
var io = require('socket.io')(server, {pingTimeout: 0, pingInterval: 500, origins: '*:*'});

app.use(express.static(__dirname + '/node_modules'));
app.get('/', function(req, res,next) {
    res.sendFile(__dirname + '/index.html');
});


state = {"error_mode" : false}
io.on('connection', function(client) {
    console.log('Client connected...');

    client.emit('state', state)

    client.on('state', function(data) {
       console.log(data);
       error_mode = data["error_mode"]
       client.broadcast.emit('state', data);
    });
    
    client.on('location', function(data) {
        console.log(data["lat"], " , ", data["lon"])
        client.broadcast.emit('location', data)
    })
    client.on('speed', function(data) {
        console.log(data)
        client.broadcast.emit('speed', data)
    })
    client.on('video', function(data) {
        image = data["image"].toString("base64")
        // console.log("Recieving Video Feed")
        // console.log(image)

        client.broadcast.emit('video', image);
    })


    client.on('error', function(data) {
        console.log(data)
        client.broadcast.emit('clienterror', data)
    })

    client.on('movement', function(data) {
        console.log(data)
        client.broadcast.emit('movement', data)
    })
});




port = process.env.PORT || 4200
server.listen(port);