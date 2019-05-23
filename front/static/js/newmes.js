"use strict";
(function ()
{

function get_len() {
$.ajax({
    type: "POST",
    url: "/get_len",
    data: $('form').serialize(),
    success: function(response) {
        var json = jQuery.parseJSON(response);
        $('#len').html(json.len);
        var mgs = json.len.mess_ch;
        $(".wd").empty();
        mgs.forEach( function(v) {
            if(v.st == "in") {
                var d1 = $("<div class='incoming_msg'></div>");
                var d2 = $("<div class='incoming_msg_img'></div>");
                var im = $("<img class='incoming_msg'></img>");
                im.attr("src", v.ava);
                var d3 = $("<div class='received_msg'></div>");
                var d4 = $("<div class='received_withd_msg'></div>");
                var p = $("<p></p>");
                var a = $("<a href=''></a>");
                a.attr("href", v.url);
                a.append(v.name);
                var br = $("<br>");
                var sp = $("<span class='time_date'></span>");
                sp.append(v.time);
                d2.appendTo(d1);
                im.appendTo(d2);
                d3.appendTo(d1);
                d4.appendTo(d3);
                p.appendTo(d4);
                a.appendTo(p);
                br.appendTo(p);
                p.append(" ");
                p.append(v.text);
                sp.appendTo(d4);
                d1.appendTo('.wd');
            }
            else
            {
                var d1 = $("<div class='outgoing_msg'></div>");
                var d2 = $("<div class='sent_msg'></div>");
                var p = $("<p></p>");
                p.append(v.text);
                //var br = $("<br>");
                var sp = $("<span class='time_date'></span>");
                sp.append(v.time);
                d2.appendTo(d1);
                p.appendTo(d2);
                sp.appendTo(d2);
                d1.appendTo('.wd');
            }
        } );
        //console.log(mgs);
    },
    error: function(error) {
        console.log(error);
    }
    });

var div = $(".msg_history");
div.scrollTop(div.prop('scrollHeight'));
}


var div1 = $(".msg_history");
div1.scrollTop(div1.prop('scrollHeight'));
    setInterval(get_len, 5000);
}());



function sm() {
$.ajax({
    type: "POST",
    url: "/sm",
    data: $('form').serialize(),
    success: function(response) {
        var json = jQuery.parseJSON(response);
        $('#len').html(json.len);
        var mgs = json.len.mess_ch;
        $(".wd").empty();
        mgs.forEach( function(v) {
            if(v.st == "in") {
                var d1 = $("<div class='incoming_msg'></div>");
                var d2 = $("<div class='incoming_msg_img'></div>");
                var im = $("<img class='incoming_msg'></img>");
                im.attr("src", v.ava);
                var d3 = $("<div class='received_msg'></div>");
                var d4 = $("<div class='received_withd_msg'></div>");
                var p = $("<p></p>");
                var a = $("<a href=''></a>");
                a.attr("href", v.url);
                a.append(v.name);
                var br = $("<br>");
                var sp = $("<span class='time_date'></span>");
                sp.append(v.time);
                d2.appendTo(d1);
                im.appendTo(d2);
                d3.appendTo(d1);
                d4.appendTo(d3);
                p.appendTo(d4);
                a.appendTo(p);
                br.appendTo(p);
                p.append(" ");
                p.append(v.text);
                sp.appendTo(d4);
                d1.appendTo('.wd');
            }
            else
            {
                var d1 = $("<div class='outgoing_msg'></div>");
                var d2 = $("<div class='sent_msg'></div>");
                var p = $("<p></p>");
                p.append(v.text);
                //var br = $("<br>");
                var sp = $("<span class='time_date'></span>");
                sp.append(v.time);
                d2.appendTo(d1);
                p.appendTo(d2);
                sp.appendTo(d2);
                d1.appendTo('.wd');
            }
        } );
        //console.log(mgs);
    },
    error: function(error) {
        console.log(error);
    }

    });
$(".semd").val("");
$(".write_msg").val("");
$('.semd').each(function () {
    this.reset();
});
var div = $(".msg_history");
div.scrollTop(div.prop('scrollHeight'));
return false;

}

function selectdial(id) {
console.log(id)

    $.ajax({
    type: "POST",
    url: "/dailm",
    data: id,
    success: function(response) {
        var json = jQuery.parseJSON(response);
        $('#len').html(json.len);
        var mgs = json.len.mess_ch;
        $(".wd").empty();
        mgs.forEach( function(v) {
            if(v.st == "in") {
                var d1 = $("<div class='incoming_msg'></div>");
                var d2 = $("<div class='incoming_msg_img'></div>");
                var im = $("<img class='incoming_msg'></img>");
                im.attr("src", v.ava);
                var d3 = $("<div class='received_msg'></div>");
                var d4 = $("<div class='received_withd_msg'></div>");
                var p = $("<p></p>");
                var a = $("<a href=''></a>");
                a.attr("href", v.url);
                a.append(v.name);
                var br = $("<br>");
                var sp = $("<span class='time_date'></span>");
                sp.append(v.time);
                d2.appendTo(d1);
                im.appendTo(d2);
                d3.appendTo(d1);
                d4.appendTo(d3);
                p.appendTo(d4);
                a.appendTo(p);
                br.appendTo(p);
                p.append(" ");
                p.append(v.text);
                sp.appendTo(d4);
                d1.appendTo('.wd');
            }
            else
            {
                var d1 = $("<div class='outgoing_msg'></div>");
                var d2 = $("<div class='sent_msg'></div>");
                var p = $("<p></p>");
                p.append(v.text);
                //var br = $("<br>");
                var sp = $("<span class='time_date'></span>");
                sp.append(v.time);
                d2.appendTo(d1);
                p.appendTo(d2);
                sp.appendTo(d2);
                d1.appendTo('.wd');
            }
        } );
        //console.log(mgs);
    },
    error: function(error) {
        console.log(error);
    }
    });

var div = $(".msg_history");
div.scrollTop(div.prop('scrollHeight'));
}