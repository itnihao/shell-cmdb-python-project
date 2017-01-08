//$('.del-btn').on("click", function(event){
//
//    var value = $(this).attr('value');
//    $.get('/api/cluster/del/',{id:value}, function(data){
//         if(data.code != 0){
//                swal({
//                    title: "删除失败",
//                    type: "warning",
//                    showCancelButton: true,
//                    cancelButtonText: 'cancel',
//                    confirmButtonClass: "btn-info",
//                    closeOnConfirm: false
//                });
//            }else{
//             swal({
//                    title:  '删除成功',
//                    type: "success",
//                    showCancelButton: true,
//                    cancelButtonText: 'cancel',
//                    confirmButtonClass: "btn-info",
//                    closeOnConfirm: true
//                }, function(){
//                    location.reload();
//                    return false
//                });
//
//            }
//    });
//});




$('tbody tr').on('click', function(event){
    var $e = $(event.target);
    if($e.hasClass('del-btn')){
        var value = $e.attr('value');
        console.log(12);
        $.get('/api/cluster/del/',{id:value}, function(data){
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
        return false;

    }

});




$('#add_cluster').on('click', function(event) {
    var name = $('#cluster_name').val().trim();
    var path = $('#cluster_path').val().trim();
    console.log(name + path);
    if ((name.length == 0) && (desc.length == 0)) {
        swal({
                    title: "集群名称或者路径不可为空",
                    type: "warning",
                    showCancelButton: true,
                    cancelButtonText: 'cancel',
                    confirmButtonClass: "btn-info",
                    closeOnConfirm: false
                });
    } else {
        $.get('/api/cluster/add/', {
            'cluster_name': name,
            'cluster_path': path
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
    $.get('/api/cluster/search/', {'value':val}, function(data){
        var objs = eval(data.data);
        var htm = [];
        for(var i=0; i<objs.length; i++){
            var obj = objs[i];
            htm.push('<tr><th class="center"><label class="pos-rel">');
            htm.push('<input type="checkbox" value="', obj.pk, '" class="ace">');
            htm.push('<span class="lbl"></span>', '</label></th><td>');
            htm.push(obj.fields.cluster_name);
            htm.push('</td><td>');
            htm.push(obj.fields.deploy_path);
            htm.push('</td><td>');


            htm.push(' <a class="btn  btn-danger btn-xs del-btn"  value="',obj.pk,'" ><i class="ace-icon fa fa-trash-o "></i></a>&nbsp;');
            htm.push('<a class="btn  btn-info btn-xs" href="/cluster/busline/assoc/?id=',obj.pk,'"><i class="ace-icon fa fa-group "></i></a>&nbsp;');
            htm.push('<a class="btn  btn-warning  btn-xs" href="/cluster/user/assoc/?id=',obj.pk,'"><i class="ace-icon fa fa-user "></i></a>&nbsp;')
            htm.push('</td></tr>');
        }


        var htm_val = htm.join('');
        $('tbody').children().remove().end().append(htm_val);
        //$('tbody').append(htm_val);
        //console.log(htm_val);


    })
});
