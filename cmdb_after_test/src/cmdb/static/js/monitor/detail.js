;
var  test_a = null;
var monitor_detail_ops = {
    init:function(){
        this.get_load();
        this.get_net();
        this.get_iowait();
        this.get_mem();
        this.get_last_ratio();
        this.get_host_monitor();
        $('#time_button').show();
    },
    eventBind:function(){
        var that = this;
        $('#time_picker').change(function(){
            that.get_load();
            that.get_net();
            that.get_iowait();
            that.get_mem();
        });
        $(".time").each(function () {
            $(this).click(function () {
                var _time = $(this).attr("data");
                that.get_ratio(_time);
            });
        });
        $($(".time").get(0)).click();
    },
    get_load:function(){
        this.wrap_ajax_get(this.build_url("load"),'json','load');
    },
    get_net:function(){
        this.wrap_ajax_get(this.build_url("net"),'json','net');
    },
    get_iowait:function(){
        this.wrap_ajax_get(this.build_url("iowait"),'json','iowait');
    },
    get_mem:function(){
        this.wrap_ajax_get(this.build_url("mem"),'json','mem');
    },
    get_ratio:function(time){
        var host_id = $("#host_id").val();
        var url = "/monitor/get_load_data" + "?type=host&id=" + host_id + "&time=" + time;
        this.wrap_ajax_get(url,'json','host_ratio');
    },
    get_last_ratio:function(){
        var host_id = $("#host_id").val();
        $.ajax({
            url: "/cmdb/host/ratio",
            type: 'POST',
            data:{'ids':host_id},
            dataType: "json",
            success: function (res) {
                if(!res){
                    return;
                }
                ratios =res.data[0];
                for(var key in ratios){
                    classname = key;
                    content ='<a href="javascript:void(0);">满载率 '+ratios[key][0]+'%</a>'
                    $("."+classname).html(content);
                }
            }
        });
    },
    get_host_monitor:function(){
        var host_id = $("#host_id").val();
        $.ajax({
            url: "/monitor/get_host_monitor/"+host_id,
            dataType: "json",
            success: function (res) {
                if(!res || !res.data){
                    return;
                }
                var data = res.data;
                var cpu = "CPU " + data.cpu;
                var mem = 'Mem ' + data.mem ;
                var disk = 'Disk ' + data.disk;
                var net = 'Net I/O ' + data.net;
                var iowait = 'IOWAIT ' + data.iowait ;
                $("#app_bar_cpu").html(cpu);
                $("#app_bar_mem").html(mem);
                $("#app_bar_disk").html(disk);
                $("#app_bar_net").html(net);
                $("#app_bar_iowait").html(iowait);
            }
        });
    },
    wrap_ajax_get:function(url, datatype,from){
        $.ajax({
            url: url,
            type: "get",
            dataType: datatype,
            success: function (resp) {
                if(resp.data.type == "spline"){
                    test_a = mycharts_ops.draw_spline(from,resp);
                }else if (resp.data.type == "area"){
                    mycharts_ops.draw_area(from,resp)
                }
                if(from == "host_ratio"){
                    mycharts_ops.draw_ratio(from,resp)
                }
            }
        });
    },
    build_url:function(item_type){
        var range = $("#time_picker").val();
        var host_id = $("#host_id").val();
        return "/monitor/act_load_data?item_type="+item_type+"&host_id="+host_id+"&range="+range;
    }
};

$(document).ready(function () {
    monitor_index_ops.init();
    monitor_detail_ops.init();
    monitor_detail_ops.eventBind();
});
