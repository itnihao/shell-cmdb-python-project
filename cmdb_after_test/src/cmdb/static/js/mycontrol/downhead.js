(function($){
    jQuery.fn.Downhead = function(options) {

        var defaults ={
            header:'jinchao',
            background:'blue',
            lefticon:'glyphicon glyphicon-align-justify',
            divid:'mydownhead',
            childcontent:'<div>aaaaaaaaaaa</div>'
        }
        var options = $.extend(defaults,options);

        return this.each(function() {
             var o=options;
             var Obj=$(this);

            S='<div id="'+ o.divid+'"><div class="inline row" style="border-radius: 12px;background-color: '+ o.background+';margin-left: 1px;height: 40px;">'+
                    ' <i style="margin-left: 4px;font-size: 25px;margin-top: 5px" class="'+ o.lefticon+'"></i>&nbsp;&nbsp;&nbsp;&nbsp;'+
                  '<label class="label-important" style="margin-top: 5px"><font size="5" color="white">'+ o.header+'</font> </label>'+

                   '<button id="hide_detail'+o.divid+'" style="background-color: white;margin-top: 7px;margin-right: 2px" class="glyphicon glyphicon-chevron-down pull-right btn-xs hide_detail"></button>'+
                   '<button id="show_detail'+o.divid+'" style="background-color: white;margin-top: 7px;margin-right: 2px" class="glyphicon glyphicon-chevron-up pull-right btn-xs show_detail"></button>'+
               '</div></div>'
            Obj.html(S);
            Obj.find('#'+ o.divid).append(o.childcontent)
            $("#hide_detail"+o.divid).click(function () {

                $(Obj.find('#'+ o.divid).children("div")[1]).hide()
            })
            $("#show_detail"+o.divid).click(function () {

                $(Obj.find('#'+ o.divid).children("div")[1]).show()
            })
        })

    }
})(jQuery);
