;
var layout = {
    init:function(){
        var nav = $("#side_nav li");
        nav.click(function(){
            //e.preventDefault();
            $(this).addClass("active").siblings().removeClass("active");
        });

        var path = location.pathname;

        $(".left_nav >li >a").each(function(){
            if((/\/orders\/order_claim/).test(path)){
                $(".left_nav >li").find("a[href='/cmdb/orders/order_claim']").parent().addClass("active");
                return false;
            }
            if((/\/orders\/handling/).test(path)){
                $(".left_nav >li").find("a[href='/cmdb/orders/handling']").parent().addClass("active");
                return false;
            }
            if((/\/orders\/my/).test(path)){
                $(".left_nav >li").find("a[href='/cmdb/orders/my']").parent().addClass("active");
                return false;
            }
            if((/\/orders\/list/).test(path)){
                $(".left_nav >li").find("a[href='/cmdb/orders/list']").parent().addClass("active");
                return false;
            }
        })
    }
};






$(document).ready(function () {
    layout.init();
    $.ajax({
        'url':'/cmdb/orders/numbers',
        'type':'POST',
        'dataType':'json',
        'success':function(res){
            if (res) {
                $("#wait_claim").html(res.wait_claim_number);
                $("#wait_do").html(res.wait_do_number);
            }
        }
    });

});