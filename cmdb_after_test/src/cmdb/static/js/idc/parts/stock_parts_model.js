;
var partsmodel_ops = {
    init: function () {
        partsmodel_ops.sort();
        this.eventBind();
    },
    eventBind: function () {
        $(".list").each(function () {
            $(this).click(function () {
                var url = $(this).attr("data");
                window.location.href = url;
            });
        });
        $("#add_mem").click(function () {
            partsmodel_ops.msgtips("");
            $("#mem_storage").val(0);
            $("#model").val(0);
            $("#frequency").val(0);
            $("#add_mem_model").foundation('reveal', 'open');
        });
        $("#add_disk").click(function () {
            partsmodel_ops.msgtips("");
            $("#size").val(0);
            $("#disk_storage").val(0);
            $("#interface").val(0);
            $("#speed").val(0);
            $("#if_rate").val(0);
            $("#add_disk_model").foundation('reveal', 'open');
        });
        $("#doadd_mem").click(function(){
            var type = $.trim($("#memorytype").val());
            var storage = $.trim($("#mem_storage").val());
            var model = $.trim($("#model").val());
            var frequency = $.trim($("#frequency").val());
            var memoryid = $.trim($("#memoryid").val());
            if(!(partsmodel_ops.display_tips(storage,"请选择内存容量"))){
                return false;
            }
            if(!(partsmodel_ops.display_tips(model,"请选择内存类型"))){
                return false;
            }
            if(!(partsmodel_ops.display_tips(frequency,"请选择内存频率"))){
                return false;
            }
            if (memoryid && /^[1-9]\d*$/.test(memoryid)) {
                $.ajax({
                    'url': '/cmdb/parts/modify_model/' + memoryid,
                    'type': 'post',
                    'dataType': 'json',
                    'data': {'storage': storage, 'model': model, 'frequency': frequency,'type':type},
                    success: function (res) {
                        if (res.code == 1) {
                            partsmodel_ops.msgtips(res.msg, 0);
                        } else {
                            $("#doadd_mem").css("display","none");
                            $("#gray_1").css("display","block");
                            partsmodel_ops.msgtips(res.msg, 1);
                            $("#add_mem_model").foundation('reveal', 'close');
                            window.location.href = window.location.href;
                        }
                    }
                });
            }
            else{
                $.ajax({
                    'url': '/cmdb/parts/add_model',
                    'type': 'post',
                    'dataType': 'json',
                    'data': {'storage': storage, 'model': model, 'frequency': frequency,'type':type},
                    success: function (res) {
                        if (res.code == 1) {
                            partsmodel_ops.msgtips(res.msg, 0);
                        } else {
                            $("#doadd_mem").css("display","none");
                            $("#gray_1").css("display","block");
                            partsmodel_ops.msgtips(res.msg, 1);
                            $("#add_mem_model").foundation('reveal', 'close');
                            window.location.href = window.location.href;
                        }
                    }
                });
            }

        });

        $("#interface").change(function(){
            var in_fc = $.trim($("#interface").val());
            if (in_fc == "SSD"){
                $("#speed").hide();
            }
            else{
                $("#speed").show();
                $("#speed").val("0");
            }
        });

        $("#doadd_disk").click(function(){
            var type = $.trim($("#disktype").val());
            var storage = $.trim($("#disk_storage").val());
            var size = $.trim($("#size").val());
            var in_fc = $.trim($("#interface").val());
            if(in_fc == "SSD"){
                var speed = "无";
            }else {
                var speed = $.trim($("#speed").val());
            }
            var if_rate = $.trim($("#if_rate").val());
            var diskid = $.trim($("#diskid").val());
            if(!(partsmodel_ops.display_tips(size,"请选择硬盘尺寸"))){
                return false;
            }
            if(!(partsmodel_ops.display_tips(storage,"请选择硬盘容量"))){
                return false;
            }
            if(!(partsmodel_ops.display_tips(in_fc,"请选择接口"))){
                return false;
            }
            if(!(partsmodel_ops.display_tips(speed,"请选择转速"))){
                return false;
            }
            if(!(partsmodel_ops.display_tips(if_rate,"请选择接口速率"))){
                return false;
            }
            if (diskid && /^[1-9]\d*$/.test(diskid)) {
                $.ajax({
                    'url': '/cmdb/parts/modify_model/' + diskid,
                    'type': 'post',
                    'dataType': 'json',
                    'data': {'storage': storage, 'size': size, 'in_fc': in_fc, 'speed': speed, 'if_rate': if_rate, 'type': type},
                    success: function (res) {
                        if (res.code == 1) {
                            partsmodel_ops.msgtips(res.msg, 0);
                        } else {
                            $("#doadd_disk").css("display","none");
                            $("#gray_2").css("display","block");
                            partsmodel_ops.msgtips(res.msg, 1);
                            $("#add_disk_model").foundation('reveal', 'close');
                            window.location.href = window.location.href;
                        }
                    }
                });
            }
            else {
                $.ajax({
                    'url': '/cmdb/parts/add_model',
                    'type': 'post',
                    'dataType': 'json',
                    'data': {'storage': storage, 'size': size, 'in_fc': in_fc, 'speed': speed, 'if_rate': if_rate, 'type': type},
                    success: function (res) {
                        if (res.code == 1) {
                            partsmodel_ops.msgtips(res.msg, 0);
                        } else {
                            $("#doadd_disk").css("display","none");
                            $("#gray_2").css("display","block");
                            partsmodel_ops.msgtips(res.msg, 1);
                            $("#add_disk_model").foundation('reveal', 'close');
                            window.location.href = window.location.href;
                        }
                    }
                });
            }
        });
        $(".modify").click(function(){
            $("[name=msgtips]").hide();
            var id = $(this).attr("data");
            $.ajax({
                'url': '/cmdb/parts/model/' + id,
                'dataType': 'json',
                success: function (res) {
                    if (res) {
                        if(res.type == 1){
                            $($("#edit_mem").get(0)).html("修改内存型号");
                            $("#frequency").val(res.frequency);
                            $("#model").val(res.model);
                            $("#mem_storage").val(res.storage);
                            $("#memoryid").val(res.id);
                            $("#add_mem_model").foundation('reveal', 'open');
                        }
                        else{
                            $($("#edit_disk").get(0)).html("修改硬盘型号");
                            $("#if_rate").val(res.if_rate);
                            $("#interface").val(res.interface);
                            var in_fc = $.trim($("#interface").val());
                            $("#speed").val(res.speed);
                            if(in_fc == "SSD"){
                                $("#speed").hide();
                            }
                            $("#disk_storage").val(res.storage);
                            $("#size").val(res.size);
                            $("#type").val(res.type);
                            $("#diskid").val(res.id);
                            $("#add_disk_model").foundation('reveal', 'open');
                        }
                    }
                }
            });

        })
    },
    sort:function(){
        sortable('.table');
        partsmodel_ops.tooltips();
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

    display_tips:function(value,msg){
        if (value.length <= 0 || value == 0) {
            partsmodel_ops.msgtips(msg, 0);
            return false;
        } else {
            partsmodel_ops.msgtips("");
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
     partsmodel_ops.init();
});











