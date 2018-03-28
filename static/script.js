$(function(){
    flg = true;
    $("#menu-trigger").on('click', function(){
        if(flg){
            $("#nav").slideDown();
            flg = false;
        }else{
            $("#nav").slideUp();
            flg = true;
        }
    });

})
