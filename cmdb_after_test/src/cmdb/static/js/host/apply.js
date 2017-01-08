;
var apply_host = {
    init:function(){
        $("#host_type").val(2);
        $("#cpu_amount" ).val(2);
        $("#mem_amount" ).val(2);
        $("#disk_amount").val(50);
    },
    apply: function(){
        var that = this;
        $( "#cpu_slider" ).slider({
            range: "min",
            value:1,
            min: 1,
            max: 4,
            step: 1,
            slide: function( event, ui ) {
                var tmp_step = parseInt(ui.value)-1;
                $( "#cpu_amount" ).val( 2*Math.pow(2,tmp_step));
            }
        }).bind("slide slidechange", function(event, ui){
            if(ui.value=="4"){
                $(this).find("a").css("marginLeft", "-16px")
            }
            else{
                $(this).find("a").css("marginLeft", "0");
            }
        });
        $( "#mem_slider" ).slider({
            range: "min",
            value:1,
            min: 1,
            max: 4,
            step:1,
            slide: function( event, ui ) {
                var tmp_step = parseInt(ui.value)-1;
                $( "#mem_amount" ).val( 2*Math.pow(2,tmp_step));
            }
        }).bind("slide slidechange", function(event, ui){
            if(ui.value=="4"){
                $(this).find("a").css("marginLeft", "-16px")
            }
            else{
                $(this).find("a").css("marginLeft", "0");
            }
        });
        $( "#disk_slider" ).slider({
            range: "min",
            value:1,
            min: 1,
            max: 4,
            step:1,
            slide: function( event, ui ) {
                tmp_value = parseInt(ui.value)*50;
                $( "#disk_amount" ).val(tmp_value);
            }
        }).bind("slide slidechange", function(event, ui){
            if(ui.value=="4"){
                $(this).find("a").css("marginLeft", "-16px")
            }
            else{
                $(this).find("a").css("marginLeft", "0");
            }
        });



        $( "#physical_cpu_slider" ).slider({
            range: "min",
            value:1,
            min: 1,
            max: 3,
            step: 1,
            slide: function( event, ui ) {
                var tmp_step = parseInt(ui.value)-1;
                $( "#physical_cpu_amount" ).val( 12*Math.pow(2,tmp_step));
            }
        }).bind("slide slidechange", function(event, ui){
            if(ui.value=="3"){
                $(this).find("a").css("marginLeft", "-16px")
            }
            else{
                $(this).find("a").css("marginLeft", "0");
            }
        });



        $( "#physical_mem_slider" ).slider({
            range: "min",
            value:1,
            min: 1,
            max: 4,
            step:1,
            slide: function( event, ui ) {
                var tmp_step = parseInt(ui.value)-1;
                var tmp_mem = 96
                if(ui.value == 4){
                    $( "#physical_mem_amount" ).val(tmp_mem);
                }else{
                    $( "#physical_mem_amount" ).val( 16*Math.pow(2,tmp_step));
                }
            }
        }).bind("slide slidechange", function(event, ui){
            if(ui.value=="4"){
                $(this).find("a").css("marginLeft", "-16px")
            }
            else{
                $(this).find("a").css("marginLeft", "0");
            }
        });


        $( "#physical_disk_slider" ).slider({
            range: "min",
            value:1,
            min: 1,
            max: 4,
            step:1,
            slide: function( event, ui ) {
                tmp_value = parseInt(ui.value)*300;
                tmp_disk1 = 1000;
                tmp_disk2 = 2000;
                if(ui.value == 3){
                    $( "#physical_disk_amount" ).val(tmp_disk1);
                }else if(ui.value == 4){
                    $( "#physical_disk_amount" ).val(tmp_disk2);
                }
                else{
                    $( "#physical_disk_amount" ).val(tmp_value);
                }
            }
        }).bind("slide slidechange", function(event, ui){
            if(ui.value=="4"){
                $(this).find("a").css("marginLeft", "-16px")
            }
            else{
                $(this).find("a").css("marginLeft", "0");
            }
        });
        $("#host_type").change(function(){
            var host_type = $("#host_type").val();
            if(host_type == 1){
                $("#physical_span").css('display','block');
                $("#virtual_span").css('display','none');
                $("#os").hide();
                $("#os_lable").hide();
            }
            else{
                $("#physical_span").css('display','none');
                $("#virtual_span").css('display','block');
            }
        });
        $("#applyhost").click(function(){
            var idc = $("#idc").val();
            var pool_id = $("#pool").val();
            var pool_source = $("#pool").attr("data")
            var num = $("#number").val();
            var content = $("#content").val();
            var host_type = $("#host_type").val();
            if(host_type == 1) {
                var cpu = $("#physical_cpu_amount").val();
                var mem = $("#physical_mem_amount").val();
                var one_disk = $("#physical_disk_amount").val();
                var disk_num = $("#disk_number").val();
                var disk = parseInt(one_disk)*parseInt(disk_num)
                var os = "";
            }
            else{
                var cpu = $("#cpu_amount").val();
                var mem = $("#mem_amount").val();
                var disk = $("#disk_amount").val();
                var os = $("#os").val();
            }
            if (pool_id == -1) {
                that.msgtips("请选择您机器要入的POOL", 0);
                return false;
            }
            if (num.length <= 0) {
                that.msgtips("请输入申请的主机数量", 0);
                return false;
            } else {
                that.msgtips("");
            }
            if (content.length <= 0) {
                that.msgtips("请输入描述", 0);
                return false;
            } else {
                that.msgtips("");
            }

            $.ajax({
                    'url': '/cmdb/host/apply/add',
                    'type': 'post',
                    'dataType': 'json',
                    'data': { 'idc': idc, 'os': os, 'host_type': host_type, "pool_id": pool_id, "num": num, "content": content, "cpu": cpu
                    , "mem": mem, "disk": disk},
                    success: function (res) {
                        if (res.code == 1) {
                            that.msgtips(res.msg, 0);
                        } else {
                            that.msgtips(res.msg, 1);
                            window.location.href = '/user/myhapply'
                        }
                    }
                })
        })
    },
    msgtips:function(msg, type) {
        if (msg) {
            if (type == 0) {
                $("#msgtip").removeClass("success");
                $("#msgtip").addClass("alert");
            } else if (type == 1) {
                $("#msgtip").removeClass("alert");
                $("#msgtip").addClass("success");
            }
            $("#msgtip").html(msg);
            $("#msgtip").show();
        } else {
            $("#msgtip").hide();
        }
    }
}


$(document).ready(function () {
    apply_host.init();
    apply_host.apply();
    var host_type = $("#host_type").val();
    if(host_type == 1){
        $("#physical_span").css('display','block');
        $("#virtual_span").css('display','none');
    }else{
        $("#physical_span").css('display','none');
        $("#virtual_span").css('display','block');
    }
});