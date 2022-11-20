$(document).ready(function(){
    $("#pax").css("display","none");
        $(".registration").click(function(){
        if ($('input[name="register"]:checked').val() == "Y" ) {
            $("#pax").slideDown("fast"); //Slide Down Effect
        } else {
            $("#pax").slideUp("fast");  //Slide Up Effect
        }
     });
});
