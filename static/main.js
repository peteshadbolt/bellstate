var myName;
var pollInterval;
var output;

window.onload = function () {
    output = $("#output");
}

String.prototype.capitalize = function() {
    return this.replace(/(?:^|\s)\S/g, function(a) { return a.toUpperCase(); });
};

function setName(name) {
    myName = name;
    $("#whoareyou").hide();
    $("#greeting").html("Hi <b>"+name.capitalize()+"</b>.");
    console.log("Set name to " + name);
    $("#coins").show();
    reset();
}

function reset() {
    $.ajax({
      url: "/reset",
      dataType: 'html',
      success: function () { },
      error: function () { }
    });
}

function setCoin(coin) {
    $.ajax({
      url: "/"+myName+"/"+coin,
      dataType: 'html',
      success: function () { },
      error: function () { }
    });
    clearInterval(pollInterval);
    pollInterval = setInterval(poll, 500);
    output.html("You used the \"<b>"+coin+"</b>\" optic...");
}

function onPoll(data) {
    if (data.ready=="true"){
        output.html("The <b>" + data.output[myName] + "</b> detector clicked.");
        console.log("Finished");
        clearInterval(pollInterval);
        setTimeout(reset, 1000);
    } else {
        output.html(output.html()+".");
    }
}

function poll() {
    $.ajax({
      url: "/poll",
      dataType: 'json',
      success: onPoll,
      error: function( data ) { console.log( "Page error"); }
    });
}


