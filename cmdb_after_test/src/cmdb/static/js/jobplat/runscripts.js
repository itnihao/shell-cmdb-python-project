;
var runscripts = {
    init: function () {
        var that = this;
        $("#add-server").click(function(){
            $("#add-server-host").foundation('reveal', 'open');
            //$("#add-server-host").modal('show')
        });
    $("#select-user").click(function(){
        $("#select-username").foundation('reveal', 'open');
    });
    $(":radio").click(function(){
        var file_type =$("input[name='pokemon-type']:checked").val()
        var file_upload =$("input[name='pokemon-file']:checked").val()
        if (file_upload == "2"){
            $("#localfile").css('display','block');
        }
        else{
            $("#localfile").css('display','none');
        }
    });
    var datetime = new Date();
    var year = datetime.getFullYear();
    var month = datetime.getMonth() + 1 < 10 ? "0" + (datetime.getMonth() + 1) : datetime.getMonth() + 1;
    var date = datetime.getDate() < 10 ? "0" + datetime.getDate() : datetime.getDate();
    var hour = datetime.getHours()< 10 ? "0" + datetime.getHours() : datetime.getHours();
    var minute = datetime.getMinutes()< 10 ? "0" + datetime.getMinutes() : datetime.getMinutes();
    var second = datetime.getSeconds()< 10 ? "0" + datetime.getSeconds() : datetime.getSeconds();
    var current_time = year+month+date+hour+minute+second
    $("#job-name").val(current_time);

    $("#fileupload").change(function(){
        var file = $('#fileupload').get(0).files[0];
        if(file.length == 0){
            alert('请选择文件');
            return;
        }else{
            var filename =file.name;
            var script_type = $('input[name="pokemon-type"]:checked').val();
            var tmp_type=0

            if (filename.split('.', 2)[1] == 'sh'){
                tmp_type = 1
            }else if(filename.split('.', 2)[1] == 'py'){
                tmp_type = 2
            }else if(filename.split('.', 2)[1] == 'pl'){
                tmp_type = 3
            }
            if ( typeof(filename.split('.', 2)[1]) == 'undefined' || tmp_type != script_type){
                alert('请上传正确的文件格式!!!')
            }else{
                $("#view1").val(filename);
                $('#view1').attr('disabled',"true");
                $("#export").click(function(){
                    var reader = new FileReader();//新建一个FileReader
                    reader.readAsText(file, "UTF-8");//读取文件
                    reader.onload = function(evt){ //读取完文件之后会回来这里
                        var fileString = evt.target.result;
                        $("#content").val(fileString);
                    }
                });
            }
        }
    });

    $("#select_host").autocomplete({
        source: function (request, response) {
            $.ajax({
                url: "/cmdb/tools/jobplat/hostname/autocomplete",
                type: 'POST',
                dataType: "json",
                data: {
                    q: request.term
                },
                success: function (data) {
                    response($.map(data, function (item) {
                        return {
                            label: item[1],
                            value: item[0],
                            type: item[2]
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
        index:9999,
        scrollHeight: 50,
        select: function (event, ui) {
            $(this).val(ui.item.label);
            $("#ok1").attr('data_type',ui.item.type);
            $("#ok1").attr('data_id',ui.item.value);
            $("#msgtip1").hide();
            return false;
        },
        open: function () {

            $(this).autocomplete('widget').zIndex(999999);
        }
    });
    var input_list = new Array();
    var tmp_list = new Array();
    $("#ok1").click(function(){
        var host_pool = $("#select_host").val();
        var data_id = $(this).attr("data_id")
        var data_type = $(this).attr("data_type")
        var aa = {name: host_pool, id: data_id, type: data_type }
        var tmp = JSON.stringify(aa);

        var exits = $.inArray(host_pool,tmp_list);
        if(host_pool.length == 0) {
            that.msgtips1('请选择主机或者POOL');
        }else{
            if(exits < 0){
                $.ajax({
                    'url': "/cmdb/tools/jobplat/checkallow",
                    'type': "post",
                    'dataType': "json",
                    'data': {'host_pool': host_pool},
                    success: function(res){
                        if (res.code == 1){
                            that.msgtips1(res.msg,0);
                        }else{
                            input_list.push(tmp);
                            tmp_list.push(aa.name);
                            $("#server").append('<div id='+host_pool+' class="alert-box success radius small-2 columns left "><span>'+host_pool+'</span><div><a class="close" href="javascript:void(0);"><font color="red">×</font></a></div></div>')
                            $("#select_host").val("")
                            $("#add-server-host").foundation('reveal', 'close');
                            //$("#add-server-host").modal('close')
                        }
                    }
                });
            }else{
                that.msgtips1("已经存在主机或POOL");
            }
        }
    });



    $("#server").on("click",'a.close',function() {
        $(this).parents(".alert-box").remove()
        var remove_id = $(this).closest(".alert-box").attr("id");
        $.each(input_list,function(index,name){
            var test =  jQuery.parseJSON(name);
            if (remove_id == test.name){
                input_list.splice(index,1)
                tmp_list.splice(index,1)
            }
        });
    });


    $("#closeReveal").click(function(){
        $("#select_host").val("");
    });


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
    },
    msgtips1:function(msg, type) {
        if (msg) {
            if (type == 0) {
                $("#msgtip1").removeClass("success");
                $("#msgtip1").addClass("alert");
            } else if (type == 1) {
                $("#msgtip1").removeClass("alert");
                $("#msgtip1").addClass("success");
            }
            $("#msgtip1").html(msg);
            $("#msgtip1").show();
        } else {
            $("#msgtip1").hide();
        }
    }
};
$(document).ready(function(){

    runscripts.init();
    $("#select_host").val("")
    var file_upload =$("input[name='pokemon-file']:checked").val()
        if (file_upload == "2"){
            $("#localfile").css('display','block');
        }
        else{
            $("#localfile").css('display','none');
        }
});
