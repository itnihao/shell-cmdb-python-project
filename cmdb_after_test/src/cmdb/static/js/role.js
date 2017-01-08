;
$(document).ready(function(){
    $("#addbtn").click(function () {
            msgtips();
            $($("#edit h4").get(0)).html("添加角色");
            $("#role").val("");
            $("#roleid").val("");
            $("#flag").val("");
            $("#edit").foundation('reveal', 'open');
     });
    $("#doadd").click(function () {
        var flag = $.trim($("#flag").val());
        var role = $.trim($("#role").val());
        if (role.length == 0)
        {
            msgtips("请输入角色名称", 0);
            return false;
        }
        if (flag && /^[1-9]\d*$/.test(flag)) {
            $.ajax({
                'url': '/user/permission/role/update',
                'type': 'post',
                'dataType': 'json',
                'data': {'role': role,'roleid':flag},
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
        }else{
            $.ajax({
                'url': '/user/permission/role/add',
                'type': 'post',
                'dataType': 'json',
                'data': {'role': role},
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
});
function getRoleDetail(id){
    $("#msgtips").hide();
    $.ajax({
        'url': '/user/permission/role/' + id,
        'dataType': 'json',
        success: function (res) {
            if (res) {
                $($("#edit h4").get(0)).html("修改角色");
                $("#role").val(res.name);
                $("#roleid").val(res.id);
                $("#flag").val(res.flag);
                $("#edit").foundation('reveal', 'open');
            }

        }
    });
}
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
function DeleteRole (id) {
        if (confirm("操作提醒\r\n删除数据后同时也将删除用户拥有的这个角色")) {
            $.ajax({
                'url': '/user/permission/role/delete/' + id,
                'type': 'post',
                'dataType': 'json',
                success: function (res) {
                    window.location.href = window.location.href;
                }
            });
        }
    }