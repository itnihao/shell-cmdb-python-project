;
allocate= {
    bindevents: function () {
       var that=this;
        var maxNumber = $.trim($("#check_num").val());
        $('.hosts').each(function(){
            $(this).click(function(){
               var size = $('.hosts:checked').size();
               if (size > maxNumber) {
                   var msg = "只需要选择" + maxNumber + "台主机!!";
                   that.msgtips(msg,0);
                   return false;
                 }
               return true;
            });
        });
        $("#return").click(function(){
            window.history.go(-1);
        });
        $("#allocate").click(function(){
           var hostids=new Array();
           var num = $.trim($("#check_num").val());
           var pool_id= $.trim($("#pool_id").val());
           var apply_id = $.trim($("#apply_id").val());
            $(".hosts").each(function(){
              if($(this).prop("checked")){
                    hostids.push($(this).val())
              }
           });
          if(hostids.length==num){
              $.ajax({
                 url:'/cmdb/host/allocate',
                 type:'POST',
                 dataType:'json',
                 data:{"pool_id":pool_id, "host_ids":hostids.join(","),"apply_id":apply_id},
                 success:function(res){
                    if (res.code == 1) {
                        that.msgtips(res.msg,0);
                    } else {
                        that.msgtips(res.msg+",正在跳转到审批页",1);
                        setTimeout(function(){
                           window.location.href = "/user/happroval";
                        },2000);
                    }
                 }
              });
          }else if (hostids.length < num){
              var msg = "需要选择" + num  + "台主机!!";
              that.msgtips(msg,0);
          }
        });
   },
   msgtips:function(msg,type){
        if (type == 0) {
            $("#msgtips").removeClass("success");
            $("#msgtips").addClass("alert");
        } else if (type == 1) {
            $("#msgtips").removeClass("alert");
            $("#msgtips").addClass("success");
        }
        $("#msgtips span").html(msg);
        $("#msgtips").show();
        setTimeout(function(){
           $("#msgtips").hide();
        },2000);
   }
}

$(document).ready(function(){
    allocate.bindevents();
});

