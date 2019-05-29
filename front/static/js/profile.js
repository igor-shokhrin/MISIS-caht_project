"use strict";
function rm()
{
    if($(".sendmes").hasClass("d-none"))
        $( ".sendmes" ).removeClass("d-none")
    else
        $( ".sendmes" ).addClass("d-none")
}
function add()
{
   $( ".sendmes" ).addClass("d-none")
   $( ".tem" ).text(" ")
}
