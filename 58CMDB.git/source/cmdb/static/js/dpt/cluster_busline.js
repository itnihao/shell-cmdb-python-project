function resultFormatResult(medata) {

    return medata.text;
}

function resultFormatSelection(medata) {
    return medata.text;
}



var chooseParm ={
    allowClear:true,
    data:[],
    placeholder: "请输入参数",
    minimumInputLength: 4,
    separator:',,',
    ajax: {
        url:"/api/busline/list/",// /api/dptopt/adddpt/
        data: function (term, page) {
            return {
                q: term,
                page_limit: 5
            };
        },
        dataType: 'json',
        results: function (data, page) {
            return { results: data.data };
        },
        formatResult: resultFormatResult,
        formatSelection: resultFormatSelection,
        dropdownCssClass: "bigdrop",
        escapeMarkup: function (m) { return m; }
    }
};


$('#user_name').select2(chooseParm);

$('#control_type').select2();


$('#add_user').on('click', function(event){
    var cluster_id = $('#cluster_info').attr('value');
    var busline_id  =  $('#user_name').val();
    $.get('/api/cluster/addbusline/', {'cluster_id':cluster_id, 'busline_id':busline_id}, function(data){
        if(data.code != 0){
                swal({
                    title: "保存失败",
                    type: "warning",
                    showCancelButton: true,
                    cancelButtonText: 'cancel',
                    confirmButtonClass: "btn-info",
                    closeOnConfirm: false
                });
            }else{
             swal({
                    title:  '增加成功',
                    type: "success",
                    showCancelButton: true,
                    cancelButtonText: 'cancel',
                    confirmButtonClass: "btn-info",
                    closeOnConfirm: true
                }, function(){
                    $('#dpt_name').val('');
                    $('#dpt_desc').val('');
                    $('.close').trigger('click');
                    location.reload();
                    return false
                });

            }
    });

    return false;
});




$('.del-btn').on("click", function(event){
    var value = $(this).attr('value');
    $.get('/api/cluster/delbusline/',{id:value}, function(data){
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
});
