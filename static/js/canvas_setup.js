const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

var timer = 2*60*1000;

var unlockTime = new Date().getTime();

real_canvas_height = 100;
real_canvas_width = 100;

var room_size = document.getElementById("room_size").innerHTML;

real_canvas_height = room_size;
real_canvas_width = room_size;

var CANVAS_HEIGHT = real_canvas_height*3;
var CANVAS_WIDTH  = real_canvas_width*3;

var ZOOM_IN = 20;
var ZOOM_OUT = 2;

var zoomScale = 2;

var waiting = false;


function findScales(){
    var scale_1 = (window.innerWidth)/CANVAS_WIDTH;
    var scale_2 = (window.innerHeight)/CANVAS_HEIGHT;

    if(scale_1>scale_2){
        ZOOM_OUT = scale_2*0.8;
    }
    else{
        ZOOM_OUT = scale_1*0.8;
    }
    ZOOM_IN = 10*ZOOM_OUT;

    zoomScale = ZOOM_OUT;
}
var timeLeft = 0;


canvas.height = CANVAS_HEIGHT;
canvas.width = CANVAS_WIDTH;

ctx.height = CANVAS_HEIGHT;
ctx.width = CANVAS_WIDTH;

var colour_value = "rgb(0, 0, 0)";
var colour_id = 16;


function setupTimer(){
    
    var x = setInterval(function(){
        var now = new Date().getTime();
        timeLeft = unlockTime - now;
    
        var minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);
    
        document.getElementById("timer").innerHTML = minutes+"m "+seconds + "s ";
    
        if (timeLeft <= 0) {
            //clearInterval(x);
            document.getElementById("timer").innerHTML = "0m 0s";
    
        }
    
    }, 1000);
}

function resetTimer(){
    unlockTime = new Date();
    unlockTime.setTime(unlockTime.getTime()+timer);
}

document.getElementById("timer").innerHTML = "0m 0s";



var zoomedIn = false;

function changeZoom(event){
    if(zoomedIn){
        zoomScale = ZOOM_OUT;
        zoomedIn = false;
    }
    else{
        zoomScale = ZOOM_IN;
        zoomedIn = true;
    }
    canvasZoom();
}

function drawUserPixel(x, y, colour){
    drawPixel(x,y,colour);
    SendUpdate(x,y,colour_id)
    resetTimer();
}

function drawUpdatePixel(x, y, colour_id){
    var colour = colourIdToVal(colour_id);
    drawPixel(x,y, colour);
}

function drawPixel(x, y, colour){
    ctx.fillStyle = colour;
    ctx.fillRect(x*3, y*3,3,3);
}

function colourIdToVal(id){
    var btn = document.getElementById(id);
    return btn.style.backgroundColor;
}

function paintCanvas(x, y){
    x = x/zoomScale;
    y = y/zoomScale;

    // check if inside border of canvas
    if(x>3&&y>3&&x<CANVAS_WIDTH-3&&y<CANVAS_HEIGHT-3){
        drawUserPixel((x-(x%3))/3,(y-(y%3))/3,colour_value);
    }
}

function testCanvasDrawing(){
    var imgData = ctx.createImageData(CANVAS_WIDTH, CANVAS_HEIGHT);
    for (var i = 0; i < imgData.data.length; i += 4) {
        imgData.data[i+0] = 255;
        imgData.data[i+1] = 255;
        imgData.data[i+2] = 255;
        imgData.data[i+3] = 255;
    }
    ctx.putImageData(imgData, 0, 0);
}

function createDrawingFromArray(imageArray, x, y){
    var roomName = document.getElementById("room_name").innerHTML;
    var URL = "http://"+window.location.host+'/bitmap/'+roomName+'/';
    $.getJSON(URL, function(data){
        alert("We got stuff! :"+data['bitmap'][0]);
    })
    var imgData = ctx.createImageData(x, y);
    imgData.data = imageArray;
    ctx.putImageData(imgData, 20, 30);
}



var testCanvasData = Uint8ClampedArray.from([200,100,150,50]);
//var imgData = ctx.createImageData(1,1);
//imgData.data = testCavnasData;

var clicks = 0;

function canvasClick(event){

    var bounds = event.target.getBoundingClientRect();
    var coordX = event.clientX-bounds.left;
    var coordY = event.clientY-bounds.top;
    var x = event.pageX-div_canvas.offsetLeft;
    var y = event.pageY-div_canvas.offsetTop;

    if(timeLeft<=0){
        if(confirm("You are about to paint the canvas")){
            paintCanvas(coordX, coordY);
        }
    }
    else{
        alert("Still waiting for countdown...");
    }
}



testCanvasDrawing();


ctx.lineWidth = 5;
ctx.strokeRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

var buttons = document.getElementsByClassName('button');

var button_colors = ['rgb(38, 180, 61)', 'rgb(0, 140, 186)'];

//canvas.addEventListener('dblclick', changeZoom);
var canvasDiv = document.getElementById('div_canvas');
canvasDiv.addEventListener('click', canvasClick);

canvasDiv.addEventListener('contextmenu', function(ev) {
    ev.preventDefault();
    changeZoom();
    return false;
}, false);

function canvasZoom(){
    var new_width = CANVAS_WIDTH*zoomScale;
    var new_height = CANVAS_HEIGHT*zoomScale;

    var move_x = (new_width-CANVAS_WIDTH)/2;
    var move_y = (new_height-CANVAS_HEIGHT)/2;

    $('#div_canvas').css("transform", "matrix("+zoomScale+",0,0,"+zoomScale+","+move_x+","+move_y+")");
}



$(document).ready(function(){
    $('#div_canvas').css("height", CANVAS_HEIGHT);
    $('#div_canvas').css("widt", CANVAS_WIDTH);

    //$('#div_canvas').click(paintCanvas);


    $('button').click(function(){
        colour_id =$(this).attr('id');
        colour_value = $(this).css('backgroundColor');
        $('#selected_colour').css("background-color", colour_value);

    });
    setupTimer();

    findScales();
    canvasZoom();
    

    $("#colour_box").click(function(){
        $("#div_buttons").slideToggle("slow");
    });



    $(function() {
        $("#colour_box").draggable({containment: "window", scroll: false });
     });



   });
//ctx.scale(2,2)