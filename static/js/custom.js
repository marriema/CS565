n =  new Date();
y = n.getFullYear();
m = n.getMonth() + 1;
d = n.getDate();
document.getElementById("date").innerHTML = m + " / " + d + " / " + y;


$(document).ready(function(){
    
    $.ajax({
        url: "{{url_for('pastPeriods')}}",
        type: 'GET',
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        success: function(response){
            if(response.lastPeriod == 'none')
            {
                $("#pastPeriods").text("Shark week starts? Record it here")
                $("#endToggle").hide()
                $("#startToggle").show()
            }
            else
            {
                $("#pastPeriods").text("It seems that your current cycle started on " + response.lastPeriod + "\n" +"Does it end?")
                $("#endToggle").show()
                $("#startToggle").hide()
            }
        },
        error: function(error){
            console.log(error);
        }
    });
});

$("#start").click(function (e) {
    if($(this).prop("checked") == true)
    {
        $.ajax({
        type: "POST",
        url: "{{url_for('pastPeriods')}}",
        data: JSON.stringify({ "action" : "start" } ),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (data) {
            $.ajax({
                url: "{{url_for('pastPeriods')}}",
                type: 'GET',
                dataType: 'json',
                contentType: 'application/json; charset=utf-8',
                success: function(response){
                        $("#pastPeriods").text("It seems that your current cycle started on " + response.lastPeriod + "\n" +"Does it end?")
                        $("#endToggle").show()
                        $("#startToggle").hide()
                    },
                error: function(error){
                    console.log(error);
                }
            });
         }
        });
    }
});

$("#end").click(function (e) {

    if($(this).prop("checked") == true)
    {
        $.ajax({
        type: "POST",
        url: "{{url_for('pastPeriods')}}",
        data: JSON.stringify({ "action" : "end" } ),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (data) {
            $("#pastPeriods").text("Shark week starts? Record it here")
            $("#endToggle").hide()
            $("#startToggle").show()
        }
     });
    }
});
