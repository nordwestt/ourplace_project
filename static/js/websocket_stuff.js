


var canvasSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/canvas/' + roomName + '/');

canvasSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);

    var x = data['x'];
    var y = data['y'];
    var colour = data['colour'];

    drawPixel(x,y,colour);
};

canvasSocket.onclose = function(e) {
    console.error('Canvas socket closed unexpectedly');
};

function SendUpdate(event){
    canvasSocket.send(JSON.stringify({
        'x': x,
        'y': y,
        'colour':colour
    }));
}
