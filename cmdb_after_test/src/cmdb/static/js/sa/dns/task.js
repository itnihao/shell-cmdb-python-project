;
var dns_task_ops = {
    init: function () {
        this.eventBind();
        this.tooltips();
    },
    eventBind: function () {
        $(".pass").each(function() {
            $(this).click(function () {
                apply_pass_reject($(this).attr("data"),1);
            });
        });
        $(".reject").each(function() {
            $(this).click(function () {
                apply_pass_reject($(this).attr("data"),0);
            });
        });
        function apply_pass_reject(id,flag) {
            $.ajax({
                'url': '/sa/dns/task/add/' + id,
                'dataType': 'json',
                'type': 'post',
                'data':{'flag':flag},
                success: function () {
                    window.location.href = window.location.href
                }
            });
        }
    },
    tooltips:function(){
        $(document).foundation();
        $(".tooltip-display").each(function(){
            $(this).mouseleave(function(){
                $(".tooltip-display-wrap").css('visibility', 'hidden').hide();
            });
            $(this).mouseenter(function(){
               var target = $(this);
               var top = target.offset().top +26;
               var left = target.offset().left;
               var content = target.attr("data");
               $(".tooltip-display-wrap .content").html(content);
               $(".tooltip-display-wrap").css('visibility', 'visible').show();
               $(".tooltip-display-wrap").css({
                    'top' : (top) ? top : 'auto',
                    'bottom' : 'auto',
                    'left' : (left) ? left : 'auto',
                    'right' : 'auto'
               });
            });
        });
    }
};

$(document).ready(function () {
    dns_task_ops.init();
});
