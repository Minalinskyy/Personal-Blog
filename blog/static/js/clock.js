    $(document).ready(function(){
        var timer = setInterval(clock, 1)
        function clock(){
            var today = new Date();
            var h = today.getHours();
            var m = today.getMinutes();
            var s = today.getSeconds();
            if (m < 10) {m = "0" + m};  // add zero in front of numbers < 10
            if (s < 10) {s = "0" + s};  // add zero in front of numbers < 10
            if (h < 10) {h = "0" + h};  // add zero in front of numbers < 10
            $("#clock").html(h+":"+m+":"+s);
        }
    });