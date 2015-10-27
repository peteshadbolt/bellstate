function update(argument) {
    ctx.clearRect(0, 0, gc.width, gc.height);

    // Draw the PBS
    ctx.drawImage(img.measure, 180, 37);

    // Draw the photon
    if (30+t*5<180){
        t += 1;
        drawPhoton(ctx, 30+t*5, beamY);
    }

    // Draw the waveplate
    ctx.drawImage(img.waveplate, wpX, beamY - img.waveplate.height/2);
}
