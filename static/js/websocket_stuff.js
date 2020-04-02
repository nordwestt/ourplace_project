
var roomName =  document.getElementById("room_name_slug").innerHTML;
testAddr = "ws://echo.websocket.org";

var ws_protocol;

if (window.location.protocol == "https:") {
  ws_protocol = "wss://";
} else {
  ws_protocol = "ws://";
}

realAddr = ws_protocol + window.location.host + '/ws/place/' + roomName + '/';

const canvasSocket = new WebSocket(realAddr);

canvasSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    var x = data['x'];
    var y = data['y'];
    var colour_id = data['colour'];
    drawUpdatePixel(x,y,colour_id);
};

canvasSocket.onclose = function(e) {
    console.error('Canvas socket closed unexpectedly');
};

function SendUpdate(x, y, colour){
    canvasSocket.send(JSON.stringify({
        'x':x,
        'y':y,
        'colour':colour
    }));
}
