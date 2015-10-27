var gc, gd;

var img = {};
img.measure = new Image();
img.measure.src = '/static/measure.png';
img.waveplate = new Image();
img.waveplate.src = '/static/waveplate.png';

var t=0;
var px=0;
var py=0;

var beamY;
var wpX=120;

function drawPhoton(ctx, px, py) {
    ctx.beginPath();
    ctx.arc(px, py, 5, 0, 2*Math.PI, false);
    ctx.fillStyle = "black";
    ctx.fill();
}

function drawRotatedImage (ctx, image, angle, x, y) {
    var ax = image.width/2;
    var ay = image.height/2;
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(angle);
    ctx.drawImage(image, -ax, -ay);
    ctx.restore();
}

// Run on startup
window.onload=main;

function main() {
    gc=document.getElementById('canvas');
    ctx=gc.getContext('2d');
    setInterval(update, 30);
    beamY=gc.height/2;
}

