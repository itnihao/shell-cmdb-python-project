;
var ticket_my_ops = {
    init:function(){

    },
    eventBind:function(){
        var that = this;
        $(".del_taks").each(function(){
            $(this).click(function(){
                var task_id = $(this).attr("data");
                task_id = parseInt(task_id);
                if(confirm("忠告提示\r\n做了就是做了,没做就是没做\r\n确认关闭?")){
                    $.ajax({
                        'url':'/sa/tickets/task/mod',
                        'type':'POST',
                        'dataType':'json',
                        'data':{'type':'close','task_id':task_id},
                        'success':function(resp){
                            common_ops.msgtips(resp.msg,resp.code);
                            if(resp.code == 0){
                                setTimeout(function(){
                                    window.location.href = window.location.href;
                                },1000);
                            }
                        }
                    });
                }
            });
        });
    }
}
$(document).ready(function(){
    ticket_my_ops.eventBind();
    common_ops.tooltips();
});