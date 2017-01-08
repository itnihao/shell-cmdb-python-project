;
$(document).ready(function(){
     $("#addbtn").click(function () {
            msgtips("");
            $($("#edit h4").get(0)).html("添加供应商");
            $("#name").val("");
            $("#short_name").val("");
            $("#content").val("");
            $("#primaryid").val("");
            $("#edit").foundation('reveal', 'open');
     });
     $("#doadd").click(function () {
            var name = $.trim($("#name").val());
            var short_name = $.trim($("#short_name").val());
            var content = $.trim($("#content").val());
            var primaryid = $.trim($("#primaryid").val());
            if (name.length <= 0) {
                msgtips("请输入供应商名称", 0);
                return false;
            } else {
                msgtips("");
            }
            if (short_name.length <= 0) {
                msgtips("请输入供应商昵称", 0);
                return false;
            } else {
                msgtips("");
            }
            if (primaryid && /^[1-9]\d*$/.test(primaryid)) {
                $.ajax({
                    'url': '/cmdb/supplier/modify/' + primaryid,
                    'type': 'post',
                    'dataType': 'json',
                    'data': {'name': name,'short_name': short_name, 'content': content},
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
                    'url': '/cmdb/supplier/add',
                    'type': 'post',
                    'dataType': 'json',
                    'data': {'name': name,'short_name': short_name, 'content': content},
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
     function getSupplierDetail(id){
         $("#msgtips").hide();
        $.ajax({
            'url': '/cmdb/supplier/' + id,
            'dataType': 'json',
            success: function (res) {
                if (res) {
                    $("#msgtips").hide();
                    $($("#edit h4").get(0)).html("修改供应商");
                    $("#name").val(res.name);
                    $("#short_name").val(res.short_name);
                    $("#content").val(res.content);
                    $("#primaryid").val(res.id);
                    $("#edit").foundation('reveal', 'open');
                }

            }
        });
    }
