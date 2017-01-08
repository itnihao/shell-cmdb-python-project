;
var del_type = {
    init: function(){
        var that = this;
        $(".del").click(function(){
            var id = $(this).attr("type_id");
            $(this).each(function(){
                $.ajax({
                    'url':'/cmdb/orders/type_deleted/'+id,
                    'type': 'POST',
                    'dataType': 'json',
                    'data': {'id': id},
                    'success':function(res){
                        that.msgtips(res.msg,0);
                        if(res.code == 1){
                            that.msgtips(res.msg,1);
                        }else{
                            setTimeout(function(){
                                window.location.href = '/cmdb/orders/add_type';
                            },1000);
                        }
                    }
                })
            })
        });

        $(".edit").click(function(){
            var id = $(this).attr("type_id");
            $(this).each(function(){
                $.ajax({
                    'url':'/cmdb/orders/get_detailtype/'+id,
                    'type': 'POST',
                    'dataType': 'json',
                    'data': {'id': id},
                    'success':function(res){
                        $("#categorytype_name").val(res.data);
                        $("#categorytype_name").attr('type_id',id);
                        $("#move_type").val(id);
                    }
                })
            })
        });

        $("#ok").click(function(){
            var id = $("#categorytype_name").attr('type_id');
            var type_name = $("#categorytype_name").val();
            var move_typeid = $("#move_type").val();
            $.ajax({
                'url':'/cmdb/orders/edit_type/'+id,
                'type': 'POST',
                'dataType': 'json',
                'data': {'type_name':type_name,'move_typeid':move_typeid},
                'success':function(res){
                    that.msgtips(res.msg,0);
                    setTimeout(function(){
                        window.location.href = '/cmdb/orders/add_type';
                    },1000);
                }
            })
        })

    },

    msgtips: function(msg, code) {
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
};

$(document).ready(function () {
    del_type.init();
});