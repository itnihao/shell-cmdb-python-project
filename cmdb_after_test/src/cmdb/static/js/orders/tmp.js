;
var add_category = {
    init: function(){
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
                                value: item.cn_name,
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

        function bindListener(){
            $("a[name=del_content]").unbind().click(function(){
                $(this).parent().parent().remove();
            });
        }

        $("#add_content").click(function(){
            $("#add_order").append('<div name="jinbang" class="modal-body row"> <div class="col-md-3"><input name="order_label" type="text" class="form-control" placeholder="标题Label"></div> <div class="col-md-8"><input name="order_content" type="text" class="form-control" placeholder="分类描述"></div> <div class="col-md-1"><a name="del_content" href="#"><span id="reduce" class="glyphicon glyphicon-minus"></span></a></div> </div>')
            bindListener();
        });

        var order_label = new Array();
        var order_content = new Array();
        var tmp = new Array();
        var dec = new Array();

        $("#add").click(function(){
            $("div[name=jinbang]  input[type='text']").each(function(i){
                var tmp_value = $(this).val();
                tmp.push(tmp_value);
                dec.push(tmp_value);
                if (i%2) {
                    $("#test").append('<div class="row" style="margin-top: 20px;"> <div class="col-md-2"> <label name="label_name">'+tmp[0]+'</label><span style="color: red;">*</span> </div><div class="col-md-8"> <input id="category_name" type="text" class="form-control" disabled="disbaled" placeholder='+tmp[1]+'> </div> </div>');
                    tmp.length = 0;
                }
                $("#test").attr('data',dec);
            });
        });

        $("#click_add").click(function(){
            $("#add_order").html("");
        });

        $("#ok").click(function(){
            var label_name = $("label[name='label_name']").text();
            var category_name = $("#category_name").val();
            var select_type = $("#select_type").val();
            var user_id = $("#user").attr("data_id");
            var dec =  $("#test").attr("data");
            if(category_name.length == 0){
                alert("请输入name")
            }else{
                $.ajax({
                    'url':'/cmdb/orders/add_category',
                        'type':'POST',
                        'dataType':'json',
                        'data':{'category_name': category_name, 'user_id': user_id, 'select_type': select_type, 'dec':dec },
                        'success':function(res){
                            common_ops.msgtips(res.msg,res.code);
                            if(res.code == 0){
                                setTimeout(function(){
                                    window.location.href = window.location.href;
                                },1000);
                            }
                        }
                });
            }
        });

    }
};


$(document).ready(function () {
    add_category.init();
});