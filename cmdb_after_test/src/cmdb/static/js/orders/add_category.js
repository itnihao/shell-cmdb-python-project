;
var add_category = {
    init: function(){
        var that =this;
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


        $("body").on('click','.glyphicon-arrow-up',function(){
            var parents = $(this).parents('.row').first();
            parents.prev().before(parents);
        });

        $("body").on('click','.glyphicon-arrow-down',function(){
            var parents = $(this).parents('.row').first();
            parents.next().after(parents);
        });


        $("button[name=del_content]").unbind().click(function(){
            $(this).parent().parent().remove();
        });

        function bindListener(){
            $("button[name=del_content]").unbind().click(function(){
                $(this).parent().parent().remove();
            });
        }

        $("#add_content").click(function(){
            $("#add_order").append('<div name="jinbang" class="modal-body row"> <div class="col-md-3">' +
                '<input name="order_label" type="text" class="form-control" placeholder="标题"></div> ' +
                '<div class="col-md-5"><textarea name="order_content" type="text" class="form-control" placeholder="分类描述,如果选择select下拉框，请将选项以英文下的分号分隔"></textarea></div>' +
                '<div class="col-md-2"><select name="input_type" class="form-control"><option value="1">input</option><option value="2">text</option><option value="3">select</option></select></div>' +
                '<div class="col-md-2" style="margin-top: 7px;"><button class="glyphicon glyphicon-arrow-up"></button> ' +
                '<button class="glyphicon glyphicon-arrow-down"></button>' +
                '<button name="del_content" id="reduce" class="glyphicon glyphicon-minus"></button></div> </div>')
            bindListener();
        });


        var order_label = new Array();
        var order_content = new Array();
        var input_type = new Array();
        var tmp = [];

        $("#add").click(function(){
            $('#add_order .form-control').each(function(i){
                var select_type = $('select[name="select_type"]').val();
                var tmp_value = $.trim($(this).val());
                tmp.push(tmp_value);
                i++;
                if (!(i%3)) {
                    if (tmp[0].length !=0 && tmp[1].length !=0) {
                        that.msgtips1("提交成功",0);
                        $("#add").attr("data-dismiss","modal");
                        $("#msgtip1").hide();
                        order_label.push(tmp[0]);
                        order_content.push(tmp[1]);
                        input_type.push(tmp[2]);
                        if (tmp[2] == "2") {
                            $("#test").append(
                                '<div class="row" style="margin-top: 20px;">' +
                                '<div class="col-md-2">' +
                                ' <label name="label_name" class="qiqi" qitype="1">' + tmp[0] + '</label><span style="color: red;">*</span></div>' +
                                 ' <div class="col-md-5"><textarea name="category_name" rows="5" qitype="3" class="form-control qiqi" disabled="disbaled" placeholder=' + tmp[1] + '></textarea> </div></div>');
                        }
                        else{
                            if(tmp[2] == "1"){
                                 $("#test").append('<div class="row" style="margin-top: 20px;">' +
                                     '<div class="col-md-2">' +
                                    ' <label name="label_name" class="qiqi" qitype="1">' + tmp[0] + '</label><span style="color: red;">*</span></div>' +
                                    '<div class="col-md-5"> <input name="category_name" qitype="2" type="text" class="form-control qiqi" disabled="disbaled" placeholder=' + tmp[1] + '> </div></div>');
                            }
                            else{
                                var list=tmp[1].split(";")
                                var len=list.length
                                var str=""
                                for (var j=0;j<len;j++){
                                    str +='<option value=" '+j+'">'+ list[j]+'</option>'
                                }
                                $("#test").append('<div class="row" style="margin-top: 20px;">' +
                                    '<div class="col-md-2">' +
                                    ' <label name="label_name" class="qiqi" qitype="1">' + tmp[0] + '</label><span style="color: red;">*</span></div>' +
                                   '<div class="col-md-5"> <select name="category_name" qitype="2" class="form-control qiqi" > '
                                     + str +'</select></div></div>'
                                );
                            }
                        }
                    }else{
                        that.msgtips1("请补全内容后提交",1);
                        $("#add").attr("data-dismiss","");
                    }
                    tmp.length = 0;
                }
            });

            $("#test").attr('data_label',order_label);
            $("#test").attr('data_content',order_content);
        });

        var target=$("#add_order").attr("target");
        $("#click_add").click(function(){
            if (target==1){
                $("#add_order").html("");
            }
            $("#msgtip1").hide();
        });

        $("#ok").click(function(){

            var label_name = $.trim($("label[name='label_name']").text());
            var category_name = $.trim($("#ordercate_name").val());
            var select_type = $("#select_type").val();
            //var user_id = $("#user").attr("data_id");
            var data_label =  $.trim($("#test").attr("data_label"));
            var data_content =  $.trim($("#test").attr("data_content"));



            if(category_name.length == 0){
                that.msgtips("请输入工单分类的名字",1);
                return false;
            }


            var tmp_value = $("#user").attr("user_id");
            if(! tmp_value){
                var user_id = $("#user").attr("data_id");
            }else{
                var user_id = $("#user").attr("user_id");
            }


            if(user_id.length == 0){
                that.msgtips("请选择工单处理人",1);
                return false;
            }

            if (data_content.length==0||data_label.length==0){
                that.msgtips("请添加工单选项",1);
                return false;
            }

            var category_id= $("#add_order").attr("category_id");
            if (target ==1 ) {
                var url='/cmdb/orders/add_category'
            }else{
                var url='/cmdb/orders/edit_category/' + category_id
            }
            $.ajax({
                'url':url,
                'type':'POST',
                'dataType':'json',
                'data':{'category_name': category_name, 'user_id': user_id, 'select_type': select_type, 'data_label':data_label, 'data_content':data_content,'input_type':input_type },
                'success':function(res){
                    that.msgtips(res.msg,res.code);
                    if(res.code == 0){
                        setTimeout(function(){
                            window.location.href = '/cmdb/orders/add';
                        },1000);
                    }
                }
            });
        });

        var userData=""
        $('#adduser').click(function () {
            $("#usermodal").modal('show')
            //if (userData) {
            //    setTree()
            //    $("#loaduser").hide()
            //}
            //else {
            //    $("#loaduser").show()
            //    loaduser()
            //}
            $("#loaduser").show()
            loaduser()
        });
        function loaduser() {
            $.ajax({
                'url': '/cmdb/orders/getuser',
                'type': 'post',
                'dataType': 'json',
                'data': {},
                success: function (res) {
                    if (!userData) {
                        userData = res
                        setTree()
                        $("#loaduser").hide()
                    }
                },
                error: function (res) {
                    console.log(res)
                }
            })
        }
        var findCheckableNodess = function() {
             return $checkableUserTree.treeview('search', [$('#input-check-node').val(), {
                 ignoreCase: true,
                 exactMatch: false,
                 revealResults: true,
             }]);
        }
        var checkableUserNodes = ''
// Check/uncheck/toggle nodes
        $('#input-check-node').on('keyup', function (e) {
            checkableNodes = findCheckableNodess();
            $('.check-node').prop('disabled', !(checkableUserNodes.length >= 1));
        });

        var $checkableUserTree = ''

        function setTree() {
            $checkableUserTree = $('#usertree').treeview({
                data: userData,
                showIcon: false,
                showCheckbox: true,
                showTags: true,

                onNodeChecked: function (event, node) {
                    var children = node.nodes;

                    if (children) {
                        for (var i = 0; i < children.length; i++) {
                            var childNode = children[i];
                            var nodeId = childNode['nodeId'];
                            $('#usertree').treeview('checkNode', nodeId);
                        }
                    }
                },
                onNodeUnchecked: function (event, node) {
                    var children = node.nodes;
                    if (children) {
                        for (var i = 0; i < children.length; i++) {
                            var childNode = children[i];
                            var nodeId = childNode['nodeId'];
                            $('#usertree').treeview('uncheckNode', nodeId);
                        }
                    }
                }
            });
            $('#usertree').treeview('collapseAll', {silent: true});
        }

        $('#ok_user').click(function () {
            $('#user_alert').empty()
            $('#user_alert').hide()
            s_count = 0
            data_s = []
            $.each($('#usertree').treeview('getChecked'), function (i, item) {

                if (item) {
                    if (item.level == 3) {
                        data_s.push(item.text)
                    }
                }


            })
            if (data_s.length > 0) {
                $('#user').val(data_s)
                $("#usermodal").modal('hide')
                //$.ajax({
                //    type: 'POST',
                //    url: '/cmdb/workpermission/adduserrole/' + role_id,
                //    'dataType': 'json',
                //    'data': {user_info: JSON.stringify(data_s)},
                //    success: function (res) {
                //        if (res.code == 1) {
                //            $('#user_list').empty()
                //            $.each(res.data, function (i, w) {
                //                $('#user_list').append('<tr role="row" class="odd">' +
                //                    '<td>' + w.user.cn_name + '</td>' +
                //                    '<td>' + w.user.name + '</td>' +
                //                    '<td>' + w.user.email + '</td>' +
                //                    '<td >' +
                //                    '<div class="btn-list btn-xs span7 text-center">' +
                //                    '<button class="btn btn-danger btn-xs" id="user' + w.id + '" onclick="userdelete(' + w.id + ')">删除</button>' +
                //                    '</div>' +
                //                    '</td >' +
                //                    '</tr>')
                //            })
                //            $("#usermodal").modal('hide')
                //
                //        }
                //        else {
                //
                //            alert_msg('user_alert', true, true, '添加失败!')
                //        }
                //    },
                //    error: function () {
                //
                //        alert_msg('user_alert', true, true, '添加失败!')
                //    }
                //});
            }
            else {
                alert_msg('user_alert', true, true, '请选择用户!')
            }
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
    },

    msgtips1: function(msg, code) {
        if (msg) {
            if (code == 1) {
                $("#msgtip1").addClass('alert-warning');
            } else if (code == 0) {
                $("#msgtip1").addClass("alert-success");
            }
            $("#waining_text1").text(msg);
            $("#msgtip1").show();
        } else {
            $("#msgtip1").hide();
        }
    }

};


$(document).ready(function () {
    add_category.init();
});

