var gc, gd;

var t=0;
var px=0;
var py=0;

// Run on startup
window.onload=main;

function main() {
    // Set up the drawing environment and fit to window
    gc=document.getElementById('canvas');
    ctx=gc.getContext('2d');
    setInterval(update, 30);
}

function update(argument) {
    t += 0.5;
    px = 20 + Math.cos(t)*10;
    py = 50 + Math.sin(t)*10;
    ctx.clearRect(0, 0, gc.width, gc.height);
    ctx.beginPath();
    ctx.arc(px, py, 5, 0, 2*Math.PI, false);
    ctx.fillStyle = "red";
    ctx.fill();
}
