$(document).ready(function(){
    //判断浏览器
    if ( /MSIE 6.0/ig.test(navigator.appVersion) ) {alert("您的浏览器版本过低,建议您更换或升级浏览器");}
    else if ( /MSIE 7.0/ig.test(navigator.appVersion) ) {alert("您的浏览器版本过低,建议您更换或升级浏览器");}
    else if ( /MSIE 8.0/ig.test(navigator.appVersion) ) {alert("您的浏览器版本过低,建议您更换或升级浏览器");}
    else if ( /MSIE 9.0/ig.test(navigator.appVersion) ) {  }
    else{
           /*动画*/
            var arr = [];
            $(".animate_target").each(function (i) {
                arr.push($(this).offset().top);
            });
            addAnimation(arr);
            $(window).scroll(function () {
                addAnimation(arr);
            })
        }
})
function addAnimation(arr){
    var s_w=$(window).width();
    $.each(arr, function (i) {
        if(s_w>768){
            if ($(document).scrollTop() >= arr[i] - $(window).height() / 1.4) {
                $(".animate_target").eq(i).addClass("animation");
            }
        }else{
            if ($(document).scrollTop() >= arr[i] - $(window).height() / 1.2) {
                $(".animate_target").eq(i).addClass("animation");
            }
        }
    });
}
