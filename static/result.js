var color;
var coin;
var outputdiv;

window.onload=function(){
    color = document.querySelector("#color").innerHTML;
    coin = document.querySelector("#coin").innerHTML;
    outputdiv = document.querySelector("#result");
    main();
};

function rotate(ctx, t){
    var angle = coin == "heads" ? 0 : t*Math.PI/4;
    console.log(angle);
    ctx.drawImage(img.measure, measureX, beamY-img.measure.height/2);
    drawRotatedImage(ctx, img.waveplate, angle, wpX, beamY);
    drawPhoton(ctx, 30, beamY);
}

function move(ctx, t){
    var angle = coin == "heads" ? 0 : Math.PI/4;
    var distance = measureX-30;
    ctx.drawImage(img.measure, measureX, beamY-img.measure.height/2);
    drawRotatedImage(ctx, img.waveplate, angle, wpX, beamY);
    drawPhoton(ctx, 30+t*distance, beamY);
}

function flash(ctx, show){
    var sign = color=="blue" ? 1 : -1;
    var angle = coin == "heads" ? 0 : Math.PI/4;
    ctx.drawImage(img.measure, measureX, beamY-img.measure.height/2);
    drawRotatedImage(ctx, img.waveplate, angle, wpX, beamY);
    if (show){
        drawRotatedImage(ctx, img.flash, 0, measureX+img.measure.width-5, beamY+19*sign);
    }
}

function update(argument) {
    ctx.clearRect(0, 0, gc.width, gc.height);

    if (t<1){
        rotate(ctx, t);
        t+=0.09;
    } else if (t>=1 && t<2){
        move(ctx, t-1);
        t+=0.05;
    } else if (t<3){
        flash(ctx, false);
        t+=0.05;
    } else {
        outputdiv.style.display = "inline";
        flash(ctx, true);
        clearInterval(updateInterval);
    }

}
