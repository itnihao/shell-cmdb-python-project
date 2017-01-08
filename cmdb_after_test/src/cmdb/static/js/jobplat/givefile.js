;
var givefile = {
    init:function(){
        var that = this;

        var filecount=0

        $("#add-server").click(function(){
            $("#add-server-host").foundation('reveal', 'open');
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

        $(":radio").click(function(){
            var file_upload =$("input[name='pokemon-type']:checked").val()
            if (file_upload == "1"){
                $("#localfile").css('display','block');
                $("#ip").css('display', 'none')
                $("#filelist").css('display', 'none')
            }
            else{
                $("#localfile").css('display','none');
                $("#ip").css('display', 'block')
                $("#filelist").css('display', 'block')
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
            scrollHeight: 50,
            select: function (event, ui) {
                $(this).val(ui.item.label);
                $("#ok1").attr('data_type',ui.item.type);
                $("#ok1").attr('data_id',ui.item.value);
                $("#msgtip1").hide();
                return false;
            }
        });


        var input_list = new Array();
        var tmp_list = new Array();
        $("#ok1").click(function(){
            var host_pool = $("#select_host").val();
            var data_id = $(this).attr("data_id")
            var data_type = $(this).attr("data_type")
            var aa = {'name': host_pool, 'id': data_id, 'type': data_type }
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
                                $("#server").append('<div id='+host_pool+' class="alert-box success radius small-2 columns left " data-alert=""><span>'+host_pool+'</span><div><a class="close" data="2_10" href="javascript:void(0);">×</a></div></div>')
                                $("#select_host").val("")
                                $("#add-server-host").foundation('reveal', 'close');
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
                }
            });
        });

        $("#close").click(function(){
            $("#select_host").val("")
        })


        //$("#push_form").click(function(){
        //    var job_name = $("#job-name").val();
        //    var upload_type = $('input[name="pokemon-type"]:checked').val();
        //    var script_name = $("#view1").val();
        //    var remote_dir = $("#remote_dir").val();
        //    var limit_speed = $("#limit_speed").val();
        //    var run_user = $("#run_user").val();
        //    var remote_ip=$("#remote_ip").val();
        //    var remote_file=$("#remote_file").val();
        //    $("#retrun_log").val('正在执行...');
        //
        //    $.ajax({
        //            'url': '/cmdb/tools/jobplat/givefiles',
        //            'traditional': true,
        //            'type': 'post',
        //            'dataType': 'json',
        //            'data': {'job_name':job_name,'upload_type': upload_type, 'script_name':script_name,'limit_speed': limit_speed ,
        //                'run_user': run_user,'remote_dir': remote_dir, 'filelist': filelist, 'input_list': input_list,'remote_ip':remote_ip,'remote_file':remote_file},
        //            success: function (res) {
        //                if (res.code == 1) {
        //                    that.msgtips('上传失败!', 0);
        //                } else {
        //                    if (res.data.issuccess_r==1 ||res.data.issuccess_r=='1') {
        //                        //that.msgtips('上传成功!', 1);
        //                        $("#retrun_log").val(res.data.show_log)
        //                        //alert('success')
        //                        //window.location.href = '/cmdb/tools/jobplat/givefiles'
        //                    }
        //                    else{
        //                        //that.msgtips('上传失败!', 0);
        //                        $("#retrun_log").val(res.data.show_log)
        //                    }
        //                }
        //            },
        //          error:function(res){
        //              alert('failed')
        //          }
        //        })
        //
        //});


        $("#fileupload").change(function(){
            var file = $('#fileupload').get(0).files[0];
            var filename =file.name;
            $("#view1").val(filename);
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

}



$(document).ready(function(){
    var file_upload =$("input[name='pokemon-type']:checked").val()

    if (file_upload == "1"){
        $("#localfile").css('display','block');
        $("#ip").css('display', 'none')
        $("#filelist").css('display', 'none')
    }
    else{
        $("#localfile").css('display','none');
        $("#ip").css('display', 'block')
        $("#filelist").css('display', 'block')
    }
    givefile.init();
    $("#select_host").val("")
});


