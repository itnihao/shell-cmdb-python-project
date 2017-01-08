;
var parts_ops = {
    init: function () {
        parts_ops.sort();
        this.autofix();
        this.eventBind();
    },
    eventBind: function () {
        $(".list").each(function () {
            $(this).click(function () {
                var url = $(this).attr("data");
                window.location.href = url;
            });
        });

        $("#add").click(function () {
            parts_ops.msgtips("");
            if($("#type").val()=="mem"){
                $($("#title").get(0)).html("添加内存");
            }
            else{
                $($("#title").get(0)).html("添加硬盘");
            }
            $("#model").show();
            $(".device").hide();
            $("#in_out").val("in");
            $(".ids").val(0);
            $("#btn").val(1);
            $("#edit").foundation('reveal', 'open');
        });
        $("#discard").click(function(){

            parts_ops.msgtips("");
            if($("#type").val()=="mem"){
                $($("#title").get(0)).html("添加报废内存");
            }
            else{
                $($("#title").get(0)).html("添加报废硬盘");
            }
            $("#model").show();
            $(".device").show();
            $("#in_out").val("in");
            $(".ids").val(0);
            $("#status").val(1);
            $("#btn").val(2);
            $("#edit").foundation('reveal', 'open');
        });
        $(".out").click(function(){
            parts_ops.msgtips("");
            $($("#title").get(0)).html("出库");
            $(".device").show();
            var out_id = $(this).attr("data");
            $(".ids").val(out_id);
            var data1 = $(this).attr("data1");
            $("#select_model").val(data1);
            $("#btn").val(3);
            $("#edit").foundation('reveal', 'open');
        });
        $(".modify").click(function(){
            parts_ops.msgtips("");
            var data2 = $(this).attr("data2");
            if(data2==0){
                $($("#title").get(0)).html("入库");
                $(".device").hide();
                $("#btn").val(4);
            }
            else{
                $($("#title").get(0)).html("报废");
                $(".device").show();
                $("#status").val(1);
                $("#btn").val(5);
            }
            var target_id = $(this).attr("data");
            $(".ids").val(target_id);
            var data1 = $(this).attr("data1");
            $("#select_model").val(data1);
            $("#in_out").val("in");
            $("#edit").foundation('reveal', 'open');
        });
        $("#doadd").click(function(){
            var type = $.trim($("#type").val());
            var model = $.trim($("#select_model").val());
            var num = $.trim($("#num").val());
            var content = $.trim($("#content").val());
            var m_id = parseInt($(".ids").val());
            var d_id = parseInt($(".device_id").val());
            var in_out = $("#in_out").val();
            var btn = parseInt($("#btn").val());
            var status = parseInt($("#status").val());
            if(m_id == 0) {
                if (!(parts_ops.display_tips(model, "请选择型号"))) {
                    return false;
                }
            }
            if (!(parts_ops.display_tips(num, "请输入数量"))) {
                return false;
            }
            /*关联设备可以不做强制关联,但是备注一定要写清楚了*/

            if(content.length <5){
                parts_ops.msgtips("请填写详细备注(PS:如果主机名称没有填写请写明使用原因)", 0);
                return false;
            }
            $("#doadd").css("display","none");
            $("#gray").css("display","block");
            $.ajax({
                'url': '/cmdb/parts/add_parts',
                'type': 'post',
                'dataType': 'json',
                'data': {'model': model, 'num': num, 'content':content, 'm_id':m_id, 'd_id':d_id, 'in_out':in_out, 'type':type, 'btn':btn, 'status':status},
                success: function (res) {
                    if (res.code == 1) {
                        parts_ops.msgtips(res.msg, 0);
                    } else {
                        parts_ops.msgtips(res.msg, 1);
                        $("#edit").foundation('reveal', 'close');
                        window.location.href = window.location.href;
                    }
                }
            });
        });

        $("#status_select").on("change",function(){
                $("#search").submit();
        });
        $("#model_select").on("change",function(){
                $("#search").submit();
        });
    },
    sort:function(){
        sortable('.table');
        parts_ops.tooltips();
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
    },

    autofix: function () {
        options = {
            source: function (request, response) {
                $.ajax({
                    url: "/cmdb/parts/autocomplete",
                    type: 'POST',
                    dataType: "json",
                    data: {maxRows: 12,keyword: request.term },
                    success: function (data) {
                        response($.map(data, function (item) {
                            return {
                                label: item[1],
                                value: item[0]

                            };

                        }));
                    }
                });
            },
            minChars: 1,
            max: 5,
            scroll: true,
            autoFill: true,
            mustMatch: true,
            matchContains: false,
            scrollHeight: 50,
            select: function (event, ui) {
                $(".device_id").val(ui.item.value);
                $(".device").val(ui.item.label);
                return false;
            }
        };
        //添加autocomplete
        $(".device").autocomplete(options);
    },

    display_tips:function(value,msg){
        if (value.length <= 0 || value <= "0") {
            parts_ops.msgtips(msg, 0);
            return false;
        } else {
            parts_ops.msgtips("");
            return true
        }
    },
    msgtips: function (msg, type){
        if (msg) {
            if (type == 0) {
                $("[name=msgtips]").removeClass("success");
                $("[name=msgtips]").addClass("alert");
            } else if (type == 1) {
                $("[name=msgtips]").removeClass("alert");
                $("[name=msgtips]").addClass("success");
            }
            $("[name=msgtips]").html(msg);
            $("[name=msgtips]").show();
        } else {
            $("[name=msgtips]").hide();
        }
    }

};

$(document).ready(function(){
     parts_ops.init();

});
