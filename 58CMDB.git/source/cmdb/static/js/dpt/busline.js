$('tbody tr').on('click', function(event){
    var $e = $(event.target);
    if($e.hasClass('del-btn')){
        var value = $e.attr('value');
        $.get('/api/busline/del/',{id:value}, function(data){
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


//$('.del-btn').on("click", function(event){
//    var value = $(this).attr('value');
//    $.get('/api/busline/delbusline/',{id:value}, function(data){
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
//    return false;
//});
//


// add busline

$('#add_busline').on('click', function(event) {
    var name = $('#busline_name').val().trim();
    var code = $('#busline_code').val().trim();
	var desc = $('#busline_desc').val().trim()



    if ((name.length == 0) && (desc.length == 0)) {
        // error
		 swal({
			 title: "业务线名称和代码不可为空",
			 type: "warning",
			 showCancelButton: true,
			 cancelButtonText: 'cancel',
			 confirmButtonClass: "btn-info",
			 closeOnConfirm: false
		 });
    } else {
        //api/dptopt/(?P<action>\w+)
        var token = GetToken();
        if (token == 'error') {
            alert('Token过期');
            return false;
        }
        token = token.data.token;
        var postData = {
            'token': token,
            'busline_name': name,
            'busline_code': code,
            'desc': desc
            };
        postData = JSON.stringify(postData);
        $.ajax({
            type: "POST",
            url: '/api/busline/add/',
            data: postData,
            success: function (data) {
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
                      title: data.data.code + '增加成功',
                      type: "success",
                      showCancelButton: true,
                      cancelButtonText: 'cancel',
                      confirmButtonClass: "btn-info",
                      closeOnConfirm: true
                  }, function () {
                      $('#busline_name').val('');
                      $('#busline_code').val('');
                      $('.close').trigger('click');
                      location.reload();
                      return false
                  });

              }
          },
          dataType: 'json'
});
    }
});


$('.btn-search').on('click', function(evnet){
    var val = $('#search_value').val().trim()
    $.get('/api/busline/search/', {'value':val}, function(data){
        var objs = eval(data.data);
        var htm = [];
        for(var i=0; i<objs.length; i++){
            var obj = objs[i];
            htm.push('<tr><th class="center"><label class="pos-rel">');
            htm.push('<input type="checkbox" value="', obj.pk, '" class="ace">');
            htm.push('<span class="lbl"></span>', '</label></th><td>');
            htm.push(obj.fields.busline_code);
            htm.push('</td><td>');
            htm.push(obj.fields.busline_name);
            htm.push('</td><td>');
            htm.push('<a class="btn  btn-danger btn-xs del-btn"  value="',obj.pk,'" ><i class="ace-icon fa fa-trash-o " value="',obj.pk,'"></i></a>&nbsp;');
            htm.push('<a class="btn  btn-info btn-xs" href="/busline/dpt/assoc/?id=',obj.pk,'"><i class="ace-icon fa fa-group "></i></a>&nbsp;');
            htm.push('<a class="btn  btn-warning  btn-xs" href="/busline/user/assoc/?id=',obj.pk,'"><i class="ace-icon fa fa-user "></i></a>&nbsp;');
            htm.push('<a class="btn  btn-success btn-xs"><i class="ace-icon  glyphicon glyphicon-zoom-in "></i></a>&nbsp;')


        }


        var htm_val = htm.join('');
        $('tbody').children().remove().end().append(htm_val);
        //$('tbody').append(htm_val);
        //console.log(htm_val);


    })
});
