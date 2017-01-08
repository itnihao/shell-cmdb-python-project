;
var lblog_ops = {
    init:function(){
        this.get_all();
    },

    get_all:function(){
        this.wrap_ajax_get(this.build_url("querycount"),'json','querycount');
    },

    wrap_ajax_get:function(url, datatype,from){
        $.ajax({
            url: url,
            type: "get",
            dataType: datatype,
            success: function (resp) {
                $("#table-content").hide();
                mycharts_ops.draw_spline("querycount",resp);
                mycharts_ops.draw_spline("errorcode",resp);
                mycharts_ops.draw_spline("flow",resp);
            }
        });
    },
    build_url:function(item_type){
        return "/cmdb/tools/load_data";
    }
};

$(document).ready(function () {
    $("#list1").click(function () {
        var url = $(this).attr("data");
        window.location.href = url;
    });
    $("#list2").click(function () {
        var url = $(this).attr("data");
        window.location.href = url;
    });
    $("#searchbtn").click(function(){
        var starttime = $("#starttime").var();
        var endtime=$("#endtime").var();
        $.ajax({
                'url': '/tools/lblog/' + '?=' + type,
                'dataType': 'json',
                'type': 'post',
                'data':{'flag':flag},
                success: function (res) {
                    window.location.href = window.location.href
                }
        });
    });
    lblog_ops.init();
});