;
var common_ops = {
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
    },
    msgtips: function (msg, type) {
        if (msg) {
            if (type == 0) {
                $("#msgtips").removeClass("alert");
                $("#msgtips").addClass("success");
            } else if (type == 1) {
                $("#msgtips").removeClass("success");
                $("#msgtips").addClass("alert");
            }
            $("#msgtips").html(msg);
            $("#msgtips").show();
        } else {
            $("#msgtips").hide();
        }

    }
}