/*
 * Tara O'Kelly - G00322214.
 * Forth Year, Emerging Technologies, Software Development.
 */

// ----- Variables And Set Up -----

// Lets web applications asynchronously read the contents of files. Adapted from: https://developer.mozilla.org/en-US/docs/Web/API/FileReader/readAsDataURL
var reader  = new FileReader();
// Get canvas.
var canvas = document.getElementById("paint");
var ctx = canvas.getContext("2d");
// Configure canvas.
var width = canvas.width, height = canvas.height;
ctx.fillStyle = "#000";
ctx.fillRect(0, 0, width, height);
ctx.lineWidth=4;
ctx.strokeStyle="#fff";
var hold = false;
// Get the hidden blank canvas for comparison. Adapted from: http://jsfiddle.net/amaan/rX572/
var blank_canvas = document.getElementById("blank");
var b_ctx = blank_canvas.getContext("2d");
// Configure blank canvas.
b_ctx.fillStyle = "black";
b_ctx.fillRect(0, 0, blank_canvas.width, blank_canvas.height);

// ----- Canvas Handlers -----

// Pencil tool. Adapted from: https://nidhinp.wordpress.com/2014/02/19/paint-app-in-flask/      
// On mouse clicked get co-ordinates, get hold and begin path.
canvas.onmousedown = function (e){
    curX = e.clientX - canvas.offsetLeft;
    curY = e.clientY - canvas.offsetTop;
    hold = true;  
    prevX = curX;
    prevY = curY;
    ctx.beginPath();
    ctx.moveTo(prevX, prevY);
};
// Get co-ordinates and draw if hold is still true.    
canvas.onmousemove = function (e){
    if(hold){
        curX = e.clientX - canvas.offsetLeft;
        curY = e.clientY - canvas.offsetTop;
        draw();
    }
};
// Release hold on mouse button is released.    
canvas.onmouseup = function (e){
    hold = false;
};
// Release hold on mouse out of canvas.   
canvas.onmouseout = function (e){
    hold = false;
};
// Draw line   
function draw (){
    ctx.lineTo(curX, curY);
    ctx.stroke();
}
// Reset tool. Adapted from: https://stackoverflow.com/questions/2142535/how-to-clear-the-canvas-for-redrawing
function reset(){
    ctx.clearRect(0, 0, width, height);
    ctx.fillRect(0, 0, width, height);
}

// ----- Uploader Functions -----

function upload_file(){
    // Adapted from: https://stackoverflow.com/questions/651700/how-to-have-jquery-restrict-file-types-on-upload
    var file_name = $('#input_file');
    var ext = file_name.val().split('.').pop().toLowerCase();
    if ($(file_name).get(0).files.length === 0) {
        alert("No files selected.");
        return;
    }
    else if($.inArray(ext, ['gif','png','jpg','jpeg']) == -1) {
        alert('Must be .jpg, .png or .gif format.');
        return;
    }
    //https://developer.mozilla.org/en-US/docs/Web/API/FileReader/readAsDataURL
    var file = document.querySelector('input[type=file]').files[0];
    var data = reader.readAsDataURL(file);
}
function upload_drawing(){
    if(blank_canvas.toDataURL() == canvas.toDataURL()){
        alert('Please draw digit before uploading.');
        return;
    }
    alert('Going to send to server.');
    // https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toDataURL
    // https://stackoverflow.com/questions/10673122/how-to-save-canvas-as-an-image-with-canvas-todataurl
    // Returns a png representation of the image.
    var img = canvas.toDataURL("image/png");
    // append result image src attribute to the uploaded image
    $("#res_image").attr("src",img);
}

// ----- Event Listeners -----

$(document).ready(function(){
    $('#nav-icon').click(function(){
    $('#nav-icon,.side_nav,#main_content').toggleClass('open');
    });
});
reader.addEventListener("load", function () {
        $("#res_image").attr("src",reader.result);
        data = { image: reader.result }
        $.post("/upload", data);
    }, false);