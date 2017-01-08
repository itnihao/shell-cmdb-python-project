;
var partshistory_ops = {
    init: function () {
        partshistory_ops.sort();
        this.eventBind();
    },
    eventBind: function () {
        $(".list").each(function () {
            $(this).click(function () {
                var url = $(this).attr("data");
                window.location.href = url;
            });
        });
        $("#status_select").on("change",function(){
                $("#search").submit();
        });
        $("#model_select").on("change",function(){
                $("#search").submit();
        })
    },
    sort:function(){
        sortable('.table');
        partshistory_ops.tooltips();
    },
    tooltips:function(){
        $(document).foundation();
        $(".tooltip-display").each(function(){
          $(this).mouseout(function(){
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

$(document).ready(function(){
     partshistory_ops.init();
});
