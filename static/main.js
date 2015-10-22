var myName;
var pollInterval;

String.prototype.capitalize = function() {
    return this.replace(/(?:^|\s)\S/g, function(a) { return a.toUpperCase(); });
};

function setName(name) {
    myName = name;
    $("#whoareyou").hide();
    $("#greeting").html("Hi <b>"+name.capitalize()+"</b>!");
    $("#greeting").show();
    console.log("Set name to " + name);
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
    console.log("Set coin state to " + coin);
}

function onPoll(data) {
    console.log(data);
}

function poll() {
    $.ajax({
      url: "/poll",
      dataType: 'json',
      success: onPoll,
      error: function( data ) { console.log( "Page error"); }
    });
}


