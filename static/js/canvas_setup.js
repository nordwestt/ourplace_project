const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

var timer = 2*60*1000;

var unlockTime = new Date().getTime();

var CANVAS_HEIGHT = 300;
var CANVAS_WIDTH  = 300;

var ZOOM_IN = 20;
var ZOOM_OUT = 2;

var zoomScale = 2;


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

var selectedColor = "rgb(38, 180, 61)";


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



function setColor(button){
    var btn = document.getElementById(button.id);
    selectedColor = "'"+btn.style.backgroundColor+"'";
}

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


function drawPixel(x, y, color){
    if(timeLeft<=0){
        resetTimer();
        ctx.fillStyle = color;
        ctx.fillRect(x-(x%3), y-(y%3),3,3);
    }
}

function paintCanvas(x, y){

    x = x/zoomScale;
    y = y/zoomScale;

    if(x>3&&y>3&&x<CANVAS_WIDTH-3&&y<CANVAS_HEIGHT-3){
        drawPixel(x,y,selectedColor);
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
    var imgData = ctx.createImageData(x, y);
    imgData.data = imageArray;
    ctx.putImageData(imgData, 20, 30);
}



var testCanvasData = Uint8ClampedArray.from([200,100,150,50]);
//var imgData = ctx.createImageData(1,1);
//imgData.data = testCavnasData;

var waiting = false;
var clicks = 0;

function canvasClick(event){
    var x = event.pageX-this.offsetLeft;
    var y = event.pageY-this.offsetTop;

    if(confirm("You are about to paint the canvas")){
        paintCanvas(x, y);
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
        var x = $(this).css('backgroundColor');
        selectedColor = x;
        $('#selected_colour').css("background-color", selectedColor);

        $('#txt1').val("Button clicked");

    });
    setupTimer();

    findScales();
    //setupGrid();
    canvasZoom();
    

    $("#colour_box").click(function(){
        $("#div_buttons").slideToggle("slow");
    });

    //$("#colour_box").css("transform","scale(1,1)")


    $(function() {
        $("#colour_box").draggable({containment: "window", scroll: false });
     });



   });
//ctx.scale(2,2)