var gc, gd;

var img = {};
img.measure = new Image();
img.measure.src = '/static/measure.png';
img.waveplate = new Image();
img.waveplate.src = '/static/waveplate.png';

var t=0;
var px=0;
var py=0;

var beamY = 50;
var wpX=80;

// Run on startup
window.onload=main;

function main() {
    gc=document.getElementById('canvas');
    ctx=gc.getContext('2d');
    setInterval(update, 30);
}

function drawPhoton(ctx, px, py) {
    ctx.beginPath();
    ctx.arc(px, py, 5, 0, 2*Math.PI, false);
    ctx.fillStyle = "black";
    ctx.fill();
}
