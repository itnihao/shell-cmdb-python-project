;
var my_apply = {
    my_apply:function(){
        var that=this;
        $(".list2").click(function(){
           var url = $(this).attr("data");
            window.location.href = url;
        });
        $(".list1").click(function(){
           var url = $(this).attr("data");
            window.location.href = url;
        });
        $(".list3").click(function(){
           var url = $(this).attr("data");
            window.location.href = url;
        });
        $(".dns_modify").each(function(){
            $(this).click(function(){
                that.modifydns($(this).attr("id"));
                return false;
            });
        });
    },
    modifydns:function(id){
        $("#doadd").click(function(){
            var dns_value = $('#dns_value').val();
            var tmp_type = $('#switch_cname').css('display');
            if ($("#deny_ip1").is(":checked")){
                var ip_updated = 1;
            }else{
                var ip_updated = 0;
            }
            if (tmp_type =='none'){
                var type = 1;
                if(!(/^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/).test(dns_value)){
                    msgtips("请输入正确的ip格式",0);
                    return false;
                }else{
                    msgtips("");
                }
            }
            else{
                var type = 2;
                if(!(/^([a-z0-9]+\.)+[a-z0-9]+$/).test(dns_value)){
                   msgtips("请输入正确的域名格式", 0);
                    return false;
                } else {
                    msgtips("");
            }
        }
        $.ajax({
            'url': '/sa/dns/modify/' + id,
            'type': 'post',
            'dataType': 'json',
            'data': {'dns_value': dns_value ,'type': type, 'ip_updated': ip_updated},
            success: function (res){
                if (res.code == 1) {
                    msgtips(res.msg, 0);
                } else {
                    msgtips(res.msg, 1);
                    $("#doadd").foundation('reveal', 'close');
                    window.location.href = window.location.href;
                    }
            }
        })
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
        $("#switch_ip").click(function(){
            $("#switch_ip").css('display','none');
            $("#switch_cname").css('display','block');
            $("#self_ip").css('display','none');
        });
        $("#switch_cname").click(function(){
            $("#switch_ip").css('display','block');
            $("#switch_cname").css('display','none');
            $("#self_ip").css('display','none');
        });
        $.ajax({
            url: "/sa/dns/"+id,
            dataType: "json",
            success: function(res){
                if (res){
                    $($("#dns_edit h3").get(0)).html("修改域名");
                    if (res.type == 1 ){
                        $("#switch_ip").css('display','block');
                        $("#switch_cname").css('display','none');
                        $("#self_ip").css('display','none');
                        if(res.zone == "d.corp.anjuke.com"){
                            $("#deny_ip1").css('display','inline');
                            $("#deny_ip2").css('display','inline');
                        }else{
                            $("#deny_ip1").css('display','none');
                            $("#deny_ip2").css('display','none');
                        }
                    }else{
                        $("#switch_ip").css('display','none');
                        $("#switch_cname").css('display','block');
                        $("#self_ip").css('display','none');
                    }
                    $("#zone").val(res.prefix + '.' + res.zone);
                    if (res.zone == 'd.corp.anjuke.com'){
                        $("#switch_cname").css('display','none');
                        $("#switch_ip").css('display','none');
                        $("#self_ip").css('display','block');
                        $("#self_ip").click(function(){
                            $("#dns_value").val(res.remote_addr);
                        })
                        var ip_updated = res.ip_updated;
                        if (ip_updated == 1){
                            $("#deny_ip1").prop("checked",true);
                        }else{
                            $("#deny_ip1").prop("checked",false);
                        }
                    }
                    $("#dns_value").val(res.value);
                    $("#content").val(res.content);
                    $("#dns_edit").foundation('reveal', 'open');
                }


            }
        })
    }
}

$(document).ready(function () {
    my_apply.my_apply();
});