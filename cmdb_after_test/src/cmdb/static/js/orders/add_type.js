;
var add_type = {
    init: function(){
        $("#add").click(function(){
            var type_name = $.trim($("#type_name").val());
            if(type_name.length == 0){
                msgtips("请输入工单类型名字",1);
                return false;
            }else{
                $.ajax({
                    'url':'/cmdb/orders/add_type',
                        'type':'POST',
                        'dataType':'json',
                        'data':{'type_name': type_name},
                        'success':function(res){
                            msgtips(res.msg,res.code);
                            if(res.code == 0){
                                setTimeout(function(){
                                    window.location.href = '/cmdb/orders/add';
                                },1000);
                            }
                        }
                });
            }
        });

        $("#guanbi").click(function(){
            window.location.reload();
        });

        function msgtips(msg, code) {
        if (msg) {
            if (code == 1) {
                $("#msgtip").addClass('alert-warning');
            } else if (code == 0) {
                $("#msgtip").addClass("alert-success");
            }
            $("#waining_text").text(msg);
            $("#msgtip").show();
            } else {
                $("#msgtip").hide();
            }
        }

    }

};

$(document).ready(function () {
    add_type.init();
});