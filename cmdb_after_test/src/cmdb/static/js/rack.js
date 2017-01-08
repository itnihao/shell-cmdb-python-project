;
$(document).ready(function(){
     $("#addbtn").click(function () {
            msgtips();
            $($("#edit h4").get(0)).html("添加机柜");
            $("#name").val("");
            $("#height").val("");
            $("#dc_id").val(0);
            $("#content").val("");
            $("#primaryid").val("");
            $("#edit").foundation('reveal', 'open');
     });
     $("#doadd").click(function () {
            var name = $.trim($("#name").val());
            var height = $.trim($("#height").val());
            var dc_id = $.trim($("#dc_id").val());
            var content = $.trim($("#content").val());
            var primaryid = $.trim($("#primaryid").val());
            if (name.length <= 0) {
                msgtips("请输入机柜名称", 0);
                return false;
            } else {
                msgtips("");
            }
            if (height.length <= 0) {
                msgtips("请输入机柜高度", 0);
                return false;
            } else {
                msgtips("");
            }
            if (dc_id.length <= 0 || dc_id <= 0) {
                msgtips("请选择所属机房", 0);
                return false;
            } else {
                msgtips("");
            }
            if (primaryid && /^[1-9]\d*$/.test(primaryid)) {
                $.ajax({
                    'url': '/cmdb/rack/modify/' + primaryid,
                    'type': 'post',
                    'dataType': 'json',
                    'data': {'name': name, 'height': height, 'dc_id': dc_id, 'content': content},
                    success: function (res) {
                        if (res.code == 1) {
                            msgtips(res.msg, 0);
                        } else {
                            msgtips(res.msg, 1);
                            $("#edit").foundation('reveal', 'close');
                            window.location.href = window.location.href;
                        }
                    }
                })
            } else {
                $.ajax({
                    'url': '/cmdb/rack/add',
                    'type': 'post',
                    'dataType': 'json',
                    'data': {'name': name, 'height': height, 'dc_id': dc_id, 'content': content},
                    success: function (res) {
                        if (res.code == 1) {
                            msgtips(res.msg, 0);
                        } else {
                            msgtips(res.msg, 1);
                            $("#edit").foundation('reveal', 'close');
                            window.location.href = window.location.href;
                        }
                    }
                })
            }
     });
     function msgtips(msg, type){
            if (msg) {
                if (type == 0) {
                    $("#msgtips").removeClass("success");
                    $("#msgtips").addClass("alert");
                } else if (type == 1) {
                    $("#msgtips").removeClass("alert");
                    $("#msgtips").addClass("success");
                }
                $("#msgtips").html(msg);
                $("#msgtips").show();
            } else {
                $("#msgtips").hide();
            }
     }

});
     function getRackDetail(id,dc_name){
         $("#msgtips").hide();
        $.ajax({
            'url': '/cmdb/rack/' + id,
            'dataType': 'json',
            success: function (res) {
                if (res) {
                    $($("#edit h4").get(0)).html("修改机柜");
                    $("#name").val(res.name);
                    $("#height").val(res.height);
                    $("#dc_id").val(dc_name);
                    $("#content").val(res.content);
                    $("#primaryid").val(res.id);
                    $("#edit").foundation('reveal', 'open');
                }

            }
        });
    }
    function deleterack (id) {
        if (confirm("操作提醒\r\n数据删除之后不可恢复")) {
            $.ajax({
                'url': '/cmdb/rack/delete/' + id,
                'type': 'post',
                'dataType': 'json',
                success: function (res) {
                    window.location.href = window.location.href;
                }
            });
        }
    }
