const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');


var cooldown = document.getElementById("cooldown").innerHTML;
var timer = parseInt(cooldown)*1000;

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

function loadDoc() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        var data = JSON.parse(this.responseText);
        var bitmap = data['bitmap'];
       document.getElementById("demo").innerHTML = this.responseText;
      }
    };
    xhttp.open("GET", "ajax_info.txt", true);
    xhttp.send();
  }

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
    if(x>0&&y>0&&x<real_canvas_width-1&&y<real_canvas_height-1){
        ctx.fillStyle = colour;
        ctx.fillRect(x*3, y*3,3,3);
    }
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

function createDrawingFromArray(){
    var roomName = document.getElementById("room_name_slug").innerHTML;
    var URL = window.location.protocol+ "//" +window.location.host+'/bitmap/'+roomName+'/';
    $.getJSON(URL, function(data){
        var imageArray = data['bitmap'];
        for(var x=0; x<imageArray.length;x++){
            for(var y=0; y<imageArray[x].length; y++){
                var colour_id = imageArray[x][y];
                drawPixel(x,y,colourIdToVal(colour_id));
            }
        }

    })
    //var imgData = ctx.createImageData(CANVAS_WIDTH, CANVAS_HEIGHT);
    //imgData.data = imageArray;
    //ctx.putImageData(imgData, 20, 30);
}



var testCanvasData = Uint8ClampedArray.from([200,100,150,50]);
//var imgData = ctx.createImageData(1,1);
//imgData.data = testCavnasData;

var clicks = 0;

function canvasClick(event){

    var bounds = event.target.getBoundingClientRect();
    var coordX = event.clientX-bounds.left;
    var coordY = event.clientY-bounds.top;

    if(timeLeft<=0){
        if(confirm("You are about to paint the canvas")){
            paintCanvas(coordX, coordY);
        }
    }
    else{
        alert("Still waiting for countdown...");
    }
}


ctx.lineWidth = 5;
ctx.strokeRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

var buttons = document.getElementsByClassName('button');

var button_colors = ['rgb(38, 180, 61)', 'rgb(0, 140, 186)'];

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

    $('.mt-5').css("widht","100%");

    $('#canvas_row').css("overflow","auto");
    $('#canvas_row').css("height",window.innerHeight);


    $('#div_canvas').css("transform", "matrix("+zoomScale+",0,0,"+zoomScale+","+move_x+","+move_y+")");
    window.scrollTo(clientX,clientY);
}

var highlight_x = -1;
var highlight_y = -1;
var highlight_color = "rgb(104,151,217)";
var old_colour = "rgb(255,255,255)";

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

    createDrawingFromArray();


    $("#div_canvas").mousemove(function(){

        var bounds = event.target.getBoundingClientRect();
        var x = event.clientX-bounds.left;
        var y = event.clientY-bounds.top;
        x = x/zoomScale;
        y = y/zoomScale;

        var old_x_mod = highlight_x-(highlight_x%3);
        var old_y_mod = highlight_y-(highlight_y%3);

        var new_x_mod = x-(x%3);
        var new_y_mod = y-(y%3);


        // check if inside border of canvas
        if(x>3&&y>3&&x<CANVAS_WIDTH-3&&y<CANVAS_HEIGHT-3){

            //if new position
            if(new_x_mod!=old_x_mod||new_y_mod!=old_y_mod){
                //get colour at current position
                colour_data = ctx.getImageData(new_x_mod, new_y_mod, 1, 1).data;

                //draw highlight over
                drawPixel(new_x_mod/3,new_y_mod/3,highlight_color);

                //draw old colour at old position
                if(highlight_x!=-1&&highlight_y!=-1){
                    my_data = ctx.getImageData(old_x_mod, old_y_mod, 1, 1).data;
                    colour_check = "rgb("+my_data[0]+","+my_data[1]+","+my_data[2]+")";
                    if(colour_check==highlight_color){
                        drawPixel(old_x_mod/3,old_y_mod/3,old_colour);
                    }
                }

                //update old_colour to be colour before current highlight
                old_colour = "rgb("+colour_data[0]+","+colour_data[1]+","+colour_data[2]+")";
                //alert(new_x_mod/3+", "+new_y_mod/3);
                //alert("x and y: "+x+", "+y);
                highlight_x = x;
                highlight_y = y;
            }
        }

    });

    $("#colour_string").css("background-color","transparent");
    $("#timer").css("background-color","transparent");

   });
//ctx.scale(2,2)
