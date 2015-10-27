function update(argument) {
    ctx.clearRect(0, 0, gc.width, gc.height);

    // Draw the PBS and waveplate
    ctx.drawImage(img.measure, measureX, beamY-img.measure.height/2);
    ctx.drawImage(img.waveplate, wpX, beamY - img.waveplate.height/2);

    // Draw the photon, spinning around
    t += 0.3;
    px = 20 + Math.cos(t)*10;
    py = 50 + Math.sin(t)*10;
    drawPhoton(ctx, px, py);
}

