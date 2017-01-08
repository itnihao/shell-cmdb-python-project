;
var tickets_detail_ops = {
    init:function(){
        this.editor = undefined;
    },
    eventBind:function(){
        var that = this;
        $("#docommmit").click(function(){
            $("#content").val("");
            $("#comments").foundation('reveal', 'open');
        });
        $("#doadd").click(function(){
            var ticket_id = $.trim($("#ticket_id").val());
            var content = $.trim(that.editor.html());
            if(content.length<5){
                common_ops.msgtips('请输入评论,不少于5字节',1);
                return false;
            }
            $.ajax({
                url:'/sa/tickets/add/comments/'+ticket_id,
                type: 'POST',
                dataType:'json',
                data:{'content':content},
                success:function(resp){
                    common_ops.msgtips(resp.msg,resp.code);
                    if(resp.code == 0){
                        window.location.href = window.location.href;
                    }
                }
            });
        });
        $(".accordion .del").each(function(){
            $(this).click(function(e){
                if (e && e.preventDefault ){
                    e.preventDefault();
                    e.stopPropagation();
                }
                if(confirm("忠告提示\r\n删除任务就是不用执行了\r\n确认删除?")){
                    var task_id = $.trim($(this).attr("data"));
                    $.ajax({
                        url:'/sa/tickets/task/mod',
                        type:'POST',
                        dataType:'json',
                        data:{'type':'deleted','task_id':task_id},
                        success:function(resp){
                            common_ops.msgtips(resp.msg, resp.code);
                            if(resp.code == 0){
                                window.location.href = window.location.href;
                            }
                        }
                    })
                }
            });
        });
        $(".accordion .close").each(function(){
            $(this).click(function(e){
                if (e && e.preventDefault ){
                    e.preventDefault();
                    e.stopPropagation();
                }
                if(confirm("忠告提示\r\n做了就是做了,没做就是没做\r\n确认关闭?")){
                    var task_id = $.trim($(this).attr("data"));
                    $.ajax({
                        url:'/sa/tickets/task/mod',
                        type:'POST',
                        dataType:'json',
                        data:{'type':'close','task_id':task_id},
                        success:function(resp){
                            common_ops.msgtips(resp.msg, resp.code);
                            if(resp.code == 0){
                                window.location.href = window.location.href;
                            }
                        }
                    })
                }
            });
        });
        $(document).on('opened.fndtn.reveal', '[data-reveal]', function () {
            if(tickets_detail_ops.editor == undefined){
                that.kindinit();
            }
        });
        $(document).on('closed.fndtn.reveal', '[data-reveal]', function () {
            if(tickets_detail_ops.editor != undefined){
                KindEditor.remove('#content');
                tickets_detail_ops.editor = undefined;
            }
        });
    },
    kindinit: function () {
        var editor =  KindEditor.create('#content', {
            width: '100%',
            resizeType: 1,
            items: [
                'source', '|', 'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', 'bold', 'italic', 'underline',
                'removeformat', '|', 'justifyleft', 'justifycenter', 'justifyright', 'insertorderedlist',
                'insertunorderedlist', '|',  'link']
            });
        tickets_detail_ops.editor = editor;
    }
};

$(document).ready(function(){
    tickets_detail_ops.init();
    tickets_detail_ops.eventBind();
});