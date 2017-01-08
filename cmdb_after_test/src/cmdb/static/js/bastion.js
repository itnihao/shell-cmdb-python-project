;
var bastion_index_ops = {
    init: function () {
        this.msgtips("",0);
        if($("#no_key").size()>0){
            var time_left = 4;
            setInterval(function() {
                $("#no_key span").html(time_left);
                time_left = time_left - 1;
                if(time_left<=0){
                    window.location.href = "/user/ucenter?type=sshkey";
                }
            },1000);
        }
        else{
            this.msg();
            this.eventBind();
            var id = ($("#host_id").val());
            if(id<=0){
                $("#token-input-select_host").focus();
            }

        }
    },

    eventBind: function () {
        var that = this;
        $("#select_host").tokenInput("/cmdb/bastion/tokeninput", {
            theme: "facebook",
            hintText: "请输入申请机器名或IP",//中文字时候需要输入空格。
            noResultsText: "没有结果",
            searchingText: "正在拼命查询中...",
            onAdd: function (item) {
                if(item.type == 1){
                    $("#select_host_hidden").append('<input type="hidden" name=host_id[] value=' + item.id + ' id="host_id_' + item.id + '" />')
                }
                else{
                    $("#select_host_hidden").append('<input type="hidden" name=pool_id[] value=' + item.id + ' id="pool_id_' + item.id + '" />')
                }
            },
            onDelete: function (item) {
                $("#host_id_" + item.id).remove();
            }
        });
        that.tokeninput();
        $("#doadd").click(function () {
            var host = $.trim($("#select_host").val());
            var days = $.trim($("#days").val());
            var content = $.trim($("#content").val());
            if (host.length <= 0) {
                that.msgtips("请输入要申请的主机", 0);
                return false;
            } else {
                that.msgtips("");
            }
            if ($(".authority:checked").length <= 0) {
                that.msgtips("请选择申请权限", 0);
                return false;
            } else {
                that.msgtips("");
            }
            if (days.length <= 0) {
                that.msgtips("请选择有效期限", 0);
                return false;
            } else {
                that.msgtips("");
            }
            if (content.length <= 0) {
                that.msgtips("请输入申请描述", 0);
                return false;
            } else {
                that.msgtips("");
            }
            var obj = $("input[name=role]");
            for(var i=0; i<obj.length; i ++){
                if(obj[i].checked){
                    var role = obj[i].value;
                }
            }
            $("#roles").val(role);
            $("#apply_bastion").submit();

        });

        $(".days").each(function(){
           $(this).click(function(){
                $(".days").css("background-color","#e7e7e7");
                var flag = $(this).attr("data");
                $(this).css("background-color","#b9b9b9");
                $("#days").val(flag);
           });
        });
    },
    msgtips:function(msg, type) {
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
    },
    tokeninput:function(){
        if($("#host_id").val() != 0){
            var id = parseInt($("#host_id").val());
            var name = $("#hostname").val();
            var type = parseInt($("#type").val());
            $("#select_host").tokenInput("add", {id: id, name: name, type: type});
        }
    },
    GetRequest:function(){
               var url = location.search; //获取url中"?"符后的字串
               var theRequest = new Object();
               if (url.indexOf("?") != -1) {
                  var str = url.substr(1);
                  strs = str.split("&");
                  for(var i = 0; i < strs.length; i ++) {
                     theRequest[strs[i].split("=")[0]]=unescape(strs[i].split("=")[1]);
                  }
               }
               return theRequest;
     },
     msg:function(){
        var object = this.GetRequest();
        var msg = object['msg'];
        if(msg == 1){
            var message = "请输入要申请的主机"
        }
        else if(msg == 2){
            var message = "请选择需要的权限"
        }
        else if(msg == 3){
            var message = "请选择有效期限"
        }
        else if(msg == 4){
            var message = "请输入申请理由"
        }
        else if(msg == 5){
            var message = "您已拥有此权限，请勿重复申请"
        }
        if (message){
            this.msgtips(message, 0);
        }else {
            this.msgtips("");
        }
     }
};
$(document).ready(function () {
    bastion_index_ops.init();
});