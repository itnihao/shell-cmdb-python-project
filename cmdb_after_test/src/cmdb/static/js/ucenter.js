;
var ucenter_ops = {
    init:function(){
        if ($('#alert')){
            setTimeout("$('.close').click()",2000);
        }
    },
    eventBind:function(){
        $(".pubkey").each(function(){
           $(this).click(function(){
               $('#pubkey pre').html($(this).attr("data_key"));
               $('#pubkey').foundation('reveal', 'open');
           });
        });
    }
};
$(document).ready(function(){
     $("#addbtn").click(function () {
            var primaryid = $.trim($("#primaryid").val());
            msgtips();
            $("#name").val("");
            $("#content").val("");
            $("#edit").foundation('reveal', 'open');
     });
     $("#doadd").click(function () {
            var name = $.trim($("#name").val());
            var content = $.trim($("#content").val());
            if (name.length <= 0) {
                msgtips("请输入名称", 0);
                return false;
            } else {
                msgtips("");
            }
            if (content.length <= 0) {
                msgtips("请输入公钥", 0);
                return false;
            } else {
                msgtips("");
            }
            $.ajax({
                'url': '/user/ucenter/sshkey/add',
                'type': 'post',
                'dataType': 'json',
                'data': {'name': name, 'content': content},
                success: function (res) {
                    if (res.code == 1) {
                        msgtips(res.msg, 0);
                        return false;
                    } else {
                        msgtips(res.msg, 1);
                        $("#edit").foundation('reveal', 'close');
                    }
                    var re =/(.*)?type=sshkey$/;
                    var url = window.location.href;
                    if (re.test(url)){
                        window.location.reload();
                    }
                    else{
                        window.location.href = window.location.href+"?type=sshkey";
                    }
                }
            });
     });
    $("#save").click(function () {
        var email = $.trim($("#email").val());
        if (email.length <= 0) {
                msgtips("请输入接警邮箱", 0);
                return false;
            } else {
                msgtips("");
            }
    });
     function msgtips(msg, type){
            if (msg) {
                if (type == 0) {
                    $("#msgtip").removeClass("success");
                    $("#msgtip").addClass("alert");
                } else if (type == 1) {
                    $("#msgtip").removeClass("alert");
                    $("#msgtip").addClass("success");
                }
                $("#msgtip").html(msg);
                $("#msgtip").show();
            } else {
                $("#msgtip").hide();
            }
     }
     $(".key_delete").click(function () {
        deletekey($(this).attr("key_id"));
     });
     function deletekey(id) {
         if (confirm("操作提醒\r\n数据删除之后不可恢复")) {
            $.ajax({
                'url': '/user/ucenter/sshkey/delete/' + id,
                'type': 'post',
                'dataType': 'json',
                success: function (res) {
                    var re =/(.*)?type=sshkey$/;
                    var url = window.location.href;
                    if (re.test(url)){
                        window.location.reload();
                    }
                    else{
                        window.location.href = window.location.href+"?type=sshkey";
                    }
                }
            });
        }
    }
    ucenter_ops.init();
    ucenter_ops.eventBind();
});

