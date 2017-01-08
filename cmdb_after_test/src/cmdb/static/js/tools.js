;
$(document).ready(function(){
     if ($('#alert')){
            setTimeout("$('.close').click()",1500);
        }
     $("#addbtn").click(function () {
            msgtips();
            $("#ip").val("");
            $("#lb").val("0");
            $("#content").val("");
            $("#edit").foundation('reveal', 'open');
     });
     $("#doadd").click(function () {
        var ip = $.trim($("#ip").val());
        var lb = $.trim($("#lb").val());
        var content = $.trim($("#content").val());
        if (ip.length <= 0) {
            msgtips("请输入需要屏蔽的ip或ip段", 0);
            return false;
        } else {
            msgtips("");
        }
        if (lb.length <= 0 || lb <= 0) {
            msgtips("请选择需要生效的机器", 0);
            return false;
        } else {
            msgtips("");
        }
        $.ajax({
                'url': '/cmdb/tools/blacklist/add',
                'type': 'post',
                'dataType': 'json',
                'data': {'ip': ip, 'lb': lb, 'content': content},
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
     });
     $(".ip_delete").click(function () {
        ipdelete($(this).attr("ip_id"));
     });
     $("#ga").click(function () {
        $("#msg").val("");
        if(confirm("确认上线GA吗?\r\n确认之后不可恢复数据")){
            $("#btn").val("ga");
            var btn = $("#btn").val();
            post_data(btn);
        }
     });
     $("#beta").click(function () {
        $("#msg").val("");
        if(confirm("确认上线Beta吗?\r\n确认之后不可恢复数据")){
            $("#btn").val("beta");
            var btn = $("#btn").val();
            post_data(btn);
        }
     });
     $("#api").click(function(){
         $("#msg").val("");
         $("#btn").val("api");
         var btn = $("#btn").val();
         post_data(btn);

     });
     function post_data(btn){
         $.ajax({
                'url': '/cmdb/tools/check' ,
                'type': 'post',
                'dataType': 'json',
                'data': {'value': btn},
                success: function (res) {
                    $("#msg").val(res);
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
});