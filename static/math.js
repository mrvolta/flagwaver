var audio1 = new Audio('/static/sounds/ambient.ogg');
var audio2 = new Audio('/static/sounds/intro.mp3');
var audio3 = new Audio('/static/sounds/2.mp3');
var audio4 = new Audio('/static/sounds/wind1.mp3');
var audio5 = new Audio('/static/sounds/flapping.mp3');


$(function() {
/*    $.ajax({
        url: '/api/info',
        success: function(data) {
            console.log('get info');
            $('#info').html(JSON.stringify(data, null, '   '));
            $('#description').html(data['description']);
        }
    });*/

/*    $.ajax({
        url : '/api/calc' , //+ '&b=' + document.getElementById('b').value
        success: function(data) {
/*          $('#add').html(data['a'] + ' + ' + data['b'] + ' = ' + data['add']);
            $('#subtract').html(data['a'] + ' - ' + data['b'] + ' = ' + data['subtract']);
            $('#multiply').html(data['a'] + ' * ' + data['b'] + ' = ' + data['multiply']);
            $('#divide').html(data['a'] + ' / ' + data['b'] + ' = ' + data['divide']);*//*
            $.each(data['b'], function(key, value) {   
                 $('#set-top-edge')
                     .append($("<option></option>")
                                .attr("value",key)
                                .text(value)); 
            });
            $("#serial").html(window.document.getElementById('serial').innerHTML + "<br>" + "Available ports : " + data['b']);
            //$("#serial").html(data['Serial']);
            //callWind(0, data['Serial']);
            startaudio();
            setTimeout(function(){audio2.play();}, 3000);
            setTimeout(function(){audio3.play();}, 20000);

            var tid = setTimeout(mycode, 1000);
        }
    });*/ 

            startaudio();
            setTimeout(function(){audio2.play();}, 3000);
            setTimeout(function(){audio3.play();}, 20000);
 
    $('#calc').click(function() {
        $('#info').css('display', "none");
        $('#description').css('display', "none");
        //console.log(url);
        $.ajax({
            url : '/api/calc?a=100', //+ document.getElementById('a').value , //+ '&b=' + document.getElementById('b').value
            success: function(data) {
/*                $('#add').html(data['a'] + ' + ' + data['b'] + ' = ' + data['add']);
                $('#subtract').html(data['a'] + ' - ' + data['b'] + ' = ' + data['subtract']);
                $('#multiply').html(data['a'] + ' * ' + data['b'] + ' = ' + data['multiply']);
                $('#divide').html(data['a'] + ' / ' + data['b'] + ' = ' + data['divide']);*/
                console.log(data['b']);
                $.each(data['b'], function(key, value) {   
                     $('#set-top-edge')
                         .append($("<option></option>")
                                    .attr("value",key)
                                    .text(value)); 
                });
                $("#serial").html(window.document.getElementById('serial').innerHTML + "<br>" + "Available ports : " + data['b']);
                //callWind(0, data['Serial']);
            }
        });
    });
})

function callWind(angle, speed) {

    //window.flagWaver.setWindDetails(angle,speed);
}


function startaudio() {
    audio1.addEventListener('ended', function() {
        this.currentTime = 0;
        this.play();
    }, false);
    var playPromise = audio1.play();

      if (playPromise !== undefined) {
    playPromise.then(_ => {
      // Automatic playback started!
      // Show playing UI.
    })
    .catch(error => {
      // Auto-play was prevented
      // Show paused UI.
      //location.reload();
    });
  }
    audio4.addEventListener('ended', function() {
        this.currentTime = 0;
        this.play();
    }, false);
  audio4.play();
  audio5.play();
}
var audio_flag = true;
function stopallaudio() {
    if(audio_flag){
        audio1.pause();
        audio_flag = false;
    }else
    {
        audio1.play();
        audio_flag = true;
    }

    // audio2.pause();
    // audio3.pause();

}

// set timeout
flag_speed = 0;
function mycode() {
  // do some stuff...
  $.ajax({
    url : '/api/calc?a=100', //+ document.getElementById('a').value , //+ '&b=' + document.getElementById('b').value
    success: function(data) {
/*                $('#add').html(data['a'] + ' + ' + data['b'] + ' = ' + data['add']);
        $('#subtract').html(data['a'] + ' - ' + data['b'] + ' = ' + data['subtract']);
        $('#multiply').html(data['a'] + ' * ' + data['b'] + ' = ' + data['multiply']);
        $('#divide').html(data['a'] + ' / ' + data['b'] + ' = ' + data['divide']);*/
        $("#serial").html(window.document.getElementById('serial').innerHTML + "<br>" + data['Serial']);
        //callWind(0, data['Serial']);

        //var txt = data['Serial'].substring(data['Serial'].length - 3, data['Serial'].length);
        var txt = data['Serial'].substring(0,1);
        //console.log(txt);
        //window.flagWaver.setWindDetails(0,120 * parseInt(txt));
        flag_angle = 0;
        flag_direction = "";
        wind_speeds = JSON.parse(data['Serial'].substring(1,data['Serial'].length));
        
        switch(txt) {
          case "F":
            // code block
            flag_angle = 180.7;
            flag_direction = "Forward";
            flag_speed = wind_speeds[0];
            break;
          case "B":
            // code block
            flag_angle = 190;
            flag_direction = "Backwards";
            flag_speed = wind_speeds[1];
            break;
            case "L":
            // code block
            flag_angle = 40.7;
            flag_direction = "Left";
            flag_speed = wind_speeds[2];
            break;
            case "R":
            // code block
            flag_angle = 0;
            flag_direction = "Right";
            flag_speed = wind_speeds[3];
            break;
          default:
            // code block
        }
        //console.log("Angle: " + flag_angle);
        //console.log("Direction :" + flag_direction);
        //console.log("Speed :" + flag_speed);
        window.flagWaver.setWindDetails(flag_angle,130);

        var objDiv = document.getElementById("serial");
        objDiv.scrollTop = objDiv.scrollHeight;
    }
});
  //tid = setTimeout(mycode, 1000); // repeat myself
}

google.charts.load('current', {'packages':['gauge']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {

        var data = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Speed', 300]
/*          ['CPU', 55],
          ['Network', 68],
          ['Network2', 68]*/
        ]);

        var options = {
          width: 400, height: 120,
          redFrom: 290, redTo: 300,
          yellowFrom:250, yellowTo: 290,
          minorTicks: 5, min: 0, max: 300
        };

        var chart = new google.visualization.Gauge(document.getElementById('chart_div'));

        chart.draw(data, options);

        setInterval(function() {
          //data.setValue(0, 1, 40 + Math.round(60 * Math.random()));
          data.setValue(0,1,flag_speed);
          chart.draw(data, options);
        }, 500);
/*        setInterval(function() {
          data.setValue(1, 1, 40 + Math.round(60 * Math.random()));
          chart.draw(data, options);
        }, 5000);
        setInterval(function() {
          data.setValue(2, 1, 60 + Math.round(20 * Math.random()));
          chart.draw(data, options);
        }, 26000);*/
      }