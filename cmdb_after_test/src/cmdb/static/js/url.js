;
$(document).ready(function(){
    $("#addbtn").click(function () {
            msgtips();
            $($("#edit h4").get(0)).html("添加URL");
            $("#url").val("");
            $("#method").val(0);
            $("#tag").val("");
            $("#content").val("");
            $("#type").val("");
            $("#edit").foundation('reveal', 'open');
     });
    $("#doadd").click(function () {
        var type = $.trim($("#type").val());
        var url = $.trim($("#url").val());
        var method = $.trim($("#method").val());
        var tag = $.trim($("#tag").val());
        var content = $.trim($("#content").val());
        if (url.length == 0)
        {
            msgtips("请输入URL", 0);
            return false;
        }
        if(!(/^\/\w/.test(url)))
        {
            msgtips("URL必须已/开头", 0);
            return false;
        }
        if(/[1-9]$/.test(url))
        {
            msgtips("URL不能已数字结尾", 0);
            return false;
        }
        if(/\/$/.test(url))
        {
            msgtips("URL不能已/结尾", 0);
            return false;
        }
        if (method == 0)
        {
            msgtips("请选择URL对应的方法");
            return false
        }
        else {
                msgtips("");
            }
        if (tag.length == 0)
        {
            msgtips("请输入此URL对应的业务")
            return false
        }
        else {
                msgtips("");
            }

        if (type && /^[1-9]\d*$/.test(type)) {
            $.ajax({
                'url': '/user/permission/url/modify',
                'type': 'post',
                'dataType': 'json',
                'data': {'id':type,'url': url,'method':method,'tag':tag,'content':content},
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
                'url': '/user/permission/url/add',
                'type': 'post',
                'dataType': 'json',
                'data': {'url': url,'method':method,'tag':tag,'content':content},
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
function getUrlDetail(id){
    $("#msgtips").hide();
    $.ajax({
        'url': '/user/permission/url/' + id,
        'dataType': 'json',
        success: function (res) {
            if (res) {
                $($("#edit h4").get(0)).html("修改URL");
                $("#url").val(res.url);
                $("#method").val(res.method);
                $("#tag").val(res.tag);
                $("#content").val(res.content);
                $("#type").val(res.type);
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
function DeleteUrl (id) {
        if (confirm("操作提醒\r\n删除数据后不可恢复")) {
            $.ajax({
                'url': '/user/permission/url/delete/' + id,
                'type': 'post',
                'dataType': 'json',
                success: function (res) {
                    window.location.href = window.location.href;
                }
            });
        }
    }