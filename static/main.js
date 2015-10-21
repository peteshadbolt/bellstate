$(document).ready(main);

function main() {
    $("#heads").click(function () {
        $.ajax({
          url: "/heads",
          dataType: 'html',
          success: function () { },
          error: function () { }
        });
    });

    setInterval(poll, 500);
}

function poll() {
    $.ajax({
      url: "/poll",
      //dataType: 'html',
      success: onPoll,
      error: function( data ) { console.log( "Page error"); }
    });
}


function onPoll(data) {
    console.log(data);
}
