;
var dns_list_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $("#zone_id").on("change",function(){
                $("#search").submit();
        });
        $(".del").each(function() {
            $(this).click(function () {
                deldns($(this).attr("data"));
            });
        });
        function deldns(id) {
           if(confirm("操作提示:\r\n确定删除此域名吗？")){
           if(!/^[1-9]\d*$/.test(id)){
               return false;
           }
           $.ajax({
                url: "/sa/dns/delete/"+id,
                type: 'POST',
                dataType: "json",
                success: function (res) {
                    if (res.code == 1) {
                        alert(res.msg);
                        return;
                    }
                    window.location.href = window.location.href;
                }
           })
       }
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
    }
};

$(document).ready(function () {
    dns_list_ops.init();
});