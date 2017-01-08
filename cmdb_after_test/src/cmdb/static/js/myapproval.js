;
var bastion_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $("#list2").click(function(){
           var url = $("#list2").attr("data");
            window.location.href = url;
        });
        $("#list1").click(function(){
           var url = $("#list1").attr("data");
            window.location.href = url;
        });
        $(".pass").click(function(){
            var flag = 1;
            var id = $(this).attr("data1");
            var type = $(this).attr("data2");

            $.ajax({
                'url': '/user/add_bastiontasks/' + id +'?type=' + type,
                'dataType': 'json',
                'type': 'post',
                'data':{'flag':flag},
                success: function (res) {
                    window.location.href = window.location.href
                }
            });
        });
        $(".reject").click(function(){
            var flag = 0;
            var id = $(this).attr("data1");
            var type = $(this).attr("data2");

            $.ajax({
                'url': '/user/add_bastiontasks/' + id +'?type=' + type,
                'dataType': 'json',
                'type': 'post',
                'data':{'flag':flag},
                success: function (res) {
                    window.location.href = window.location.href

                }
            });
        });
    }
};
$(document).ready(function(){
     bastion_ops.init();

     $("[name=host_reject]").each(function () {
        $(this).click(function () {
            host_reject_info($(this).attr("apply_id"));
        });
     });

     function host_reject_info(id) {
        $("#host-reject").find("form").html(
                        '<h5>驳回申请</h5>' +
                            '<hr/>' +
                            '<div class="tips"></div>' +
                            '<input type="hidden" name="id" value="' + id + '" />' +
                            '<textarea name="note" placeholder="备注"></textarea>' +
                            '<button type="submit" class="button tiny right" id="vm">确定</button>'
                    );
        $("#host-reject").foundation('reveal', 'open');
        submit.bindevents();
     }

     $("[name=host-bastion-reject]").each(function () {
        $(this).click(function () {
            host_bastion_reject_info($(this).attr("data1"));
        });
     });

     function host_bastion_reject_info(id) {
        $("#host-bastion-reject").find("form").html(
                        '<h5>驳回申请</h5>' +
                            '<hr/>' +
                            '<div class="tips"></div>' +
                            '<input type="hidden" name="id" value="' + id + '" />' +
                            '<textarea name="note" placeholder="备注"></textarea>' +
                            '<button type="submit" class="button tiny right" id="vm">确定</button>'
                    );
        $("#host-bastion-reject").foundation('reveal', 'open');
        submit.bindevents();
     }

     function msgtips(msg) {

        if (msg) {
            $(".tips").html('<div data-alert class="alert-box alert">' + msg + '</div>').show()
        } else {
            $(".tips").html('').hide();
        }
    }
    var submit = {
        bindevents: function () {
           $("#vm").each(function () {
                $(this).click(function () {
                    var note = ($(this).parent().find("textarea[name=note]").val());

                    if (note.length <= 0) {
                        msgtips("请输入驳回理由");
                        return false;
                    }
                    $(this).parent().submit();
                    return true;
                })
            });
        }
    };

});

function host_pass(id) {
     var flag = 1;
     $.ajax({
         'url': '/user/add_applyhosttasks/' + id,
         'dataType': 'json',
         'type': 'post',
         'data': {'flag': flag},
         success: function (res) {
             window.location.href = window.location.href;
         }
     });
 };
 function host_reject(id){
     var flag = 0;
    $.ajax({
        'url': '/user/add_applyhosttasks/' + id,
        'dataType': 'json',
        'type': 'post',
        'data':{'flag':flag},
        success: function (res) {
            window.location.href = window.location.href;
        }
    });
};




