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
    $("#greeting").html(name.capitalize());
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
      success: onPoll,
      error: function () { }
    });
}

function onPoll(data) {
    output.html(data);
}
