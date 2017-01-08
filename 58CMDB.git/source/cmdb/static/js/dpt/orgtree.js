
var id =$('#treeview').attr('value');

jQuery(function() {
    var remoteUrl = '/api/listorg/';//动态树数据请求接口
    var remoteDateSource = function (options, callback) {
        var parent_id = null
        if (!('text' in options || 'type' in options)) {
            parent_id = 0; //load first level data

        }
        else if ('type' in options && options['type'] == 'folder') {
            if ('additionalParameters' in options && 'children' in options.additionalParameters) {
                parent_id = options.additionalParameters['id'];
            }
        }


        if (parent_id !== null) {
            $.ajax({
                url: remoteUrl,
                data: 'id=' + parent_id,
                type: 'GET',
                dataType: 'json',
                success: function (response) {
                    //console.log(response.data);
                    var data = eval(response.data);
                    var res = {};
                    // 按照org的level来确定的
                    for(var i=0; i<data.length; i++){
                        var tmp_key = data[i].pk;
                        var tmp_data = {};
                        if(data[i].fields.is_leaf  == '0'){
                            tmp_data = {"text": data[i].fields.org_name, "type": "folder"};
                            tmp_data['additionalParameters']  = {'id':tmp_key, 'children':null};
                        }else{
                            tmp_data = {"text":data[i].fields.org_name, "type":"item", "value": data[i].fields.org_id};
                        }
                        res[tmp_key] =  tmp_data;

                    }

                    if (response.code == 0) {
                        callback({data: res})
                    }

                },
                error: function (response) {
                    //console.log(response);
                }
            });
        }
    }

    $('#treeview' ).ace_tree({
        dataSource: remoteDateSource ,
        multiSelect: true ,
        loadingHTML: '<div class="tree-loading"><i class="ace-icon fa fa-refresh fa-spin blue"></i></div>',
        'open-icon' : 'ace-icon tree-minus',
        'close-icon' : 'ace-icon tree-plus',
        'selectable' : true ,
        'selected-icon' : 'ace-icon fa fa-check',
        'unselected-icon' : 'ace-icon fa fa-times',
        cacheItems: true ,
        folderSelect: false
    });
    //show selected items inside a modal
    $('#submit-button' ).on('click' , function () {
        var output = '' ;
        var items = $('#treeview' ).tree('selectedItems' );
        for (var i in items) if (items.hasOwnProperty(i)) {
            var item = items[i];
//            output += item.additionalParameters['id' ] + ":"+ item.text+"\n" ;
            output += item.text+"\n" ;

        }
        $('#modal-tree-items' ).modal('show' );
        $('#tree-value' ).css({'width' :'98%' , 'height' :'200px' }).val(output);
                   
    });

    $('#sure-btn').on("click", function(event){
        var val =$('#tree-value').val().trim();
        var val_id = $(this).val();
        val = val.split('\n').join(',');
        $.get('/api/orgdpt/addassocorg/',{'item':val, 'dpt_id':val_id},  function(data){
            console.log(eval(data.data));

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
                    title: '与'+ val + '关联成功',
                    type: "success",
                    showCancelButton: true,
                    cancelButtonText: 'cancel',
                    confirmButtonClass: "btn-info",
                    closeOnConfirm: true
                }, function(){
                    $('#tree-value').val('');
                    $('.close').trigger('click');
                    location.href='/dpt/detail/?id='+id ;
                    //history.back();
                    return false
                });

            }
        });
        // swal
    })
                   
});

