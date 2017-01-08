



$('.del-btn').on("click", function(event){
    var value = $(this).attr('value');

    $.get('/api/orgdpt/del/',{id:value}, function(data){
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





// dpt tree
jQuery(function() {
    var remoteUrl = '/api/dpt/listlevel/';//动态树数据请求接口
    var current_id = parseInt($('#dpt_tree').attr('value').trim());

    var tag=0;
    var remoteDateSource = function (options, callback) {
        var parent_id = null
        if (!('text' in options || 'type' in options)) {
            //parent_id = 0; //load first level data
            parent_id = current_id
            tag = 1;
        }
        else if ('type' in options && options['type'] == 'folder') {
            if ('additionalParameters' in options && 'children' in options.additionalParameters) {
                parent_id = options.additionalParameters['id'];
            }
            tag = 0;
        }else {
            tag = 0;
        }


        if (parent_id !== null) {
            $.ajax({
                url: remoteUrl,
                data: 'id=' + parent_id + '&tag='+ tag,
                type: 'GET',
                dataType: 'json',
                success: function (response) {

                    var data = eval(response.data);
                    var res = {};
                    // 按照org的level来确定的
                    for (var i = 0; i < data.length; i++) {
                        var tmp_key = data[i].pk;
                        var tmp_data = {};
                        if (data[i].fields.is_leaf == 0) {
                            tmp_data = {"text": data[i].fields.dpt_name, "type": "folder"};
                            tmp_data['additionalParameters'] = {'id': tmp_key, 'children': null};
                        } else {
                            tmp_data = {"text": data[i].fields.dpt_name, "type": "item", "value": data[i].pk};
                        }
                        res[tmp_key] = tmp_data;

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


    $('#dpt_tree').ace_tree({
        dataSource: remoteDateSource,
        multiSelect: true,
        loadingHTML: '<div class="tree-loading"><i class="ace-icon fa fa-refresh fa-spin blue"></i></div>',
        'open-icon': 'ace-icon tree-minus',
        'close-icon': 'ace-icon tree-plus',
        'selectable': true,
        'selected-icon': 'ace-icon fa fa-check',
        'unselected-icon': 'ace-icon fa fa-times',
        cacheItems: true,
        folderSelect: false
    });
});


// add assoc dpt

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
        url:"/api/bsp/list/",// /api/dptopt/adddpt/
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
