;
var order_detail = {
    init: function(){
        var that = this;
        $("#user").autocomplete({
            source: function (request, response) {
                $.ajax({
                    url: "/cmdb/orders/user/autocomplete",
                    type: 'POST',
                    dataType: "json",
                    data: {
                        q: request.term
                    },
                    success: function (data) {
                        response($.map(data, function (item) {
                            return {
                                label: item.name+ "  " +item.cn_name,
                                value: item.name,
                                id: item.id
                            }
                        }));
                    }
                });
            },
            minChars: 1,
            max: 5,
            scroll: true,
            autoFill: true,
            mustMatch: true,
            matchContains: false,
            scrollHeight: 50,
            select: function (event, ui) {
                $(this).val(ui.item.label);

                $("#user").val(ui.item.value);
                $("#user").attr("data_id",ui.item.id);
                return false;
            }
        });

        $("#level_show").mouseover(function(){
            $("#show_content").show("slow");
        });
        $("#level_show").mouseout(function(){
            $("#show_content").hide("slow");
        });

        $("#select_mail").tokenInput("/cmdb/orders/user/tokeninput", {
            theme: "facebook",
            hintText: "请输入收件人的名字",//中文字时候需要输入空格。
            noResultsText: "没有结果",
            searchingText: "正在拼命查询中...",
            onAdd: function (item) {
                $("#select_mail_hidden").append('<input type="hidden" name=mail value=' + item.mail + ' id="user_id_' + item.id + '" />')
            },
            onDelete: function (item) {
                $("#user_id_" + item.id).remove();
            }
        });

        var mail_list = new Array();
        var label_list = new Array();
        var content_list = new Array();
        $("#ok").click(function(){
            var order_title = $.trim($("#order_title").val());
            var order_level = $("#order_level").val();
            var category_id = $("#category").attr("category_id");
            var category_uid = $("#category").attr("category_uid");


            $("input[name='mail']").each(function(){
                var mail = $.trim($(this).attr("value"));
                mail_list.push(mail);
            });

            $("div[name='label']").each(function(){
                var data_label = $.trim($(this).attr("data_label"));
                label_list.push(data_label);
            });
            var flag = 0;
            var data_content=""
            $(".data_content").each(function(){
                if($(this).attr("name")=="select"){
                     data_content = $.trim($(this).find("option:selected").text());
                }
                else{  data_content = $.trim($(this).val());}
                if(data_content.length==0){
                    flag = 1;
                }else{
                    content_list.push(data_content)
                }
            });


            if(order_title.length == 0){
                that.msgtips("请输入工单标题",1);
                return false;
            }

            if(mail_list.length == 0){
                that.msgtips("请输入邮件通知人",1);
                return false
            }

            if (flag == 1){
                that.msgtips("工单内容不能为空",1);
                return false;
            }

            $.ajax({
                'url':'/cmdb/orders/order_detail',
                    'type':'POST',
                    'dataType':'json',
                    'data':{'order_title': order_title,'order_level':order_level,'mail_list':mail_list,'label_list':label_list,'content_list':content_list,'category_uid':category_uid,'category_id':category_id},
                    'success':function(res){
                        if(res.code == 0){
                            setTimeout(function(){
                                window.location.href = '/cmdb/orders/my';
                            },1000);
                        }
                    }
            });

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
    order_detail.init();
});