
$('body').on('click', function(event){
     var $e = $(event.target);
    if($e.hasClass('del-btn')) {
        var value = $e.attr('value');
         $.get('/api/dpt/del/',{id:value}, function(data){
         if(data.code != 0){
                swal({
                    title: "删除失败",
                    type: "warning",
                    showCancelButton: true,
                    cancelButtonText: 'cancel',
                    confirmButtonClass: "btn-info",
                    closeOnConfirm: false
                });
            }else{
             swal({
                    title:  '删除成功',
                    type: "success",
                    showCancelButton: true,
                    cancelButtonText: 'cancel',
                    confirmButtonClass: "btn-info",
                    closeOnConfirm: true
                }, function(){
                    location.reload();
                    return false
                });

            }
    });
    }

})


$('#add_dpt').on('click', function(event) {
    var name = $('#dpt_name').val().trim();
    var desc = $('#dpt_desc').val().trim();
    var dpt_value = $('#dpt_table').attr('value');
    console.log(dpt_value);
    var level = 1;
    var pid = 0;
    if (dpt_value.length > 1) {
        console.log(12);
        var vals = dpt_value.split('-');
        level = parseInt(vals.pop()) + 1;
        pid = vals.pop();
    }
    console.log("level" + level);


    if ((name.length == 0) && (desc.length == 0)) {
        // error
    } else {
        //api/dptopt/(?P<action>\w+)
        $.get('/api/dptopt/adddpt/', {
            'dpt_name': name,
            'dpt_level': level,
            'dpt_pid': pid,
            'dpt_desc': desc
        }, function (data) {
            if (data.code != 0) {
                swal({
                    title: "保存失败",
                    type: "warning",
                    showCancelButton: true,
                    cancelButtonText: 'cancel',
                    confirmButtonClass: "btn-info",
                    closeOnConfirm: false
                });
            } else {
                swal({
                    title: data.data.name + '增加成功',
                    type: "success",
                    showCancelButton: true,
                    cancelButtonText: 'cancel',
                    confirmButtonClass: "btn-info",
                    closeOnConfirm: true
                }, function () {
                    $('#dpt_name').val('');
                    $('#dpt_desc').val('');
                    $('.close').trigger('click');
                    location.reload();
                    return false
                });

            }
        });
    }
});


$('.btn-search').on('click', function(evnet){
    var val = $('#search_value').val().trim()
    $.get('/api/dpt/search/', {'value':val}, function(data){
        var objs = eval(data.data);
        var htm = [];
        for(var i=0; i<objs.length; i++){
            var obj = objs[i];
            htm.push('<tr><th class="center"><label class="pos-rel">');
            htm.push('<input type="checkbox" value="', obj.pk, '" class="ace">');
            htm.push('<span class="lbl"></span>', '</label></th><td>');
            htm.push(obj.fields.dpt_name);
            htm.push('</td><td>');
            htm.push(obj.fields.dpt_desc);
            htm.push('</td><td>');
            htm.push(' <a value="',obj.pk,'" class="btn  btn-danger btn-xs del-btn"><i class="ace-icon fa fa-trash-o del-btn " value="',obj.pk,'"></i></a>&nbsp;');
            htm.push('<a href="/dpt/bsp/assoc/?id=',obj.pk,'" class="btn  btn-info btn-xs"><i class="ace-icon fa fa-group "></i></a>&nbsp;');
            htm.push('<a href="/dpt/pid/?id=',obj.pk,'" class="btn  btn-purple btn-xs"><i class="ace-icon fa fa-arrow-right "></i></a>&nbsp;')
            htm.push('<a href="/dpt/user/assoc/?id=',obj.pk,'" class="btn  btn-warning  btn-xs"><i class="ace-icon fa fa-user "></i></a>&nbsp;');
            htm.push('<a href="/dpt/detail/?id=',obj.pk,'" class="btn  btn-success btn-xs"><i class=" glyphicon glyphicon-zoom-in "></i></a>&nbsp;');
            htm.push('</td></tr>');
        }


        var htm_val = htm.join('');
        $('tbody').children().remove().end().append(htm_val);
        //$('tbody').append(htm_val);
        console.log(htm_val);


    })
});