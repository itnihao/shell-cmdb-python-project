;
var tickets_cat_list_ops = {
    init:function(){
        this.editor = undefined;
        this.autofix();
    },
    eventBind:function(){
        var that = this;
        $("#add").click(function(){
            that.filldiv({'id':0,'manage_uid':0,'manage_cname':'','name':'','lable':'','template':''});
            $("#ticket_cat").foundation('reveal', 'open');
        });
        $("#doadd").click(function(){
            var name = $.trim($("#name").val());
            var label = $.trim($("#label").val());
            var manage_uid = parseInt($.trim($("#manage_uid").val()));
            var template = $.trim(tickets_cat_list_ops.editor.html());
            var id = parseInt($.trim($("#id").val()));
            var url = '/sa/tickets/category/add';
            if(name.length<2){
                that.msgtips('请输入分类名称',0);
                $("#name").focus();
                return false;
            }
            if(label.length<2){
                that.msgtips('请输入分类标签,可以直接输入分类名称',0);
                $("#label").focus();
                return false;
            }
            if(manage_uid < 1){
                that.msgtips('请输入此分类工单处理人',0);
                $("#manage_cname").focus();
                return false;
            }
            if(id > 0){
                url = '/sa/tickets/category/mod'
            }
            $.ajax({
                url:url,
                type:'POST',
                dataType:"json",
                data:{'name':name,'label':label,'manage_uid':manage_uid,'id':id,'template':template},
                success:function(res){
                    that.msgtips(res.msg,res.code);
                    if(res.code == 0){
                        window.location.href = window.location.href;
                    }
                }
            })

        });
        $(".mod").each(function(){
           $(this).click(function(){
                var id = $.trim($(this).attr("data"));
                $.ajax({
                    url: "/sa/tickets/category/"+id,
                    type: 'POST',
                    dataType: "json",
                    success:function(res){
                        if(res.code == 0){
                            that.filldiv(res.data)
                        }
                    }
                });

           });
        });
        $(document).on('opened.fndtn.reveal', '[data-reveal]', function () {
            if(tickets_cat_list_ops.editor == undefined){
                that.kindinit();
            }
        });
        $(document).on('closed.fndtn.reveal', '[data-reveal]', function () {
            if(tickets_cat_list_ops.editor != undefined){
                KindEditor.remove('#template');
                tickets_cat_list_ops.editor = undefined;
            }
        });
    },
    autofix: function () {
        options = {
            source: function (request, response) {
                $.ajax({
                    url: "/user/search",
                    type: 'POST',
                    dataType: "json",
                    data: {
                        maxRows: 12,
                        keyword: request.term
                    },
                    success: function (data) {
                        response($.map(data, function (item) {
                            return {
                                label: item[1],
                                value: item[0]
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
                 $("#manage_cname").val(ui.item.label);
                 $("#manage_uid").val(ui.item.value);
                return false;
            }
        };
        //添加autocomplete
        $("#manage_cname").autocomplete(options);
    },
    msgtips: function (msg, type) {
        if (msg) {
            if (type == 0) {
                $("#msgtips").removeClass("alert");
                $("#msgtips").addClass("success");
            } else if (type == 1) {
                $("#msgtips").removeClass("success");
                $("#msgtips").addClass("alert");
            }
            $("#msgtips").html(msg);
            $("#msgtips").show();
        } else {
            $("#msgtips").hide();
        }

    },
    filldiv: function(data){
        $("#name").val(data.name);
        $("#label").val(data.label);
        $("#template").val(data.template);
        $("#id").val(data.id);
        $("#manage_uid").val(data.manage_uid);
        $("#manage_cname").val(data.manage_cname);
        $("#ticket_cat").foundation('reveal', 'open');
    },
    kindinit: function () {
        var editor =  KindEditor.create('#template', {
            width: '100%',
            resizeType: 1,
            items: [
                'source',  '|', 'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', 'bold', 'italic', 'underline',
                'removeformat', '|', 'justifyleft', 'justifycenter', 'justifyright', 'insertorderedlist',
                'insertunorderedlist', '|', 'link']
            });
        tickets_cat_list_ops.editor = editor;
    }
};

$(document).ready(function(){
    tickets_cat_list_ops.init();
    tickets_cat_list_ops.eventBind();
});


