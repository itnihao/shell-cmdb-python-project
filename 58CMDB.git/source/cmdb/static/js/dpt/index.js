

$('.details').on('click',function(){
    var value = $(this).attr('data-target');
    var ekId = value.split('-').pop();
    $.get('/Monitor/Pigeons/ajaxGetDashboardDetail',{'ekId':ekId}, function(data){
        var info = [];
        var tmpBefore = '<div class="table-responsive"><table class="table table-bordered"><tbody>' ;
        var tmpFinal='</tbody></table></div>';
        var divName = cat('entry',data['entry']);
        var divKey =  cat('key',data['key']);
        var divAllCount = cat('all_count', data['all_count']);
        var divCount = cat('count', data['count']);
        var divFirstTime =cat('first_time',getLocalTime(data['first_time']));
        var divLastTime = cat('last_time', getLocalTime(data['last_time']));
        var divMessage = cat('message', data['message']);
        var divState = cat('stateVal', data['stateVa']);
        var divUpdateTime = cat('update_time',getLocalTime(data['update_time']));
        info = [tmpBefore,divName, divKey, divAllCount, divCount, divFirstTime, divLastTime, divMessage, divState, divUpdateTime, tmpFinal].join('');
        var divSub = '';
        var isDone = parseInt(data['is_done']);
        $('.modal-body').children().remove();
        if(data['is_sub']){
            var names = data['rNames'];
            var  tmpSub=['<table class="table table-bordered"><thead><tr> <td>已经订阅的规则名</td> </tr> </thead><tbody>'];
            $.each(names, function(i, val){
                tmpSub.push('<tr><td><a href="/Monitor/Pigeons/editRule/rule/', val, '">', val, '</a></td></tr>');
            });
            tmpSub.push('</tbody> </table>');
            divSub = tmpSub.join('');
        }
        var final = [info, divSub].join('');
        $('.modal-body').append(final);
    },'json');
    $('.modal').attr('id', value.substr(1));

});



function cat(name, value) {
    return ['<tr><td>', name, '</td><td>', value, '</td></tr>'].join('');
}




$('#item-save').on('click',function(){
    var tagName = $('#e9').val();
    var itemValues = $('#e15').val();
    $.post('/Monitor/Pigeons/ajaxAddRuleItem', {'tag':tagName, 'items':itemValues}, function(data){
        var id = data['id'];
        var href = ['<a href="#" class="delete-item" id="item-',id ,'" onclick="return del_item(',id,')">delete</a>'].join('');
        var tmp = ['<tr ','id="tr-rule-',id,'"','><td>',tagName, '</td><td>',itemValues,'</td><td>',href,'</td></tr>'].join('');
        $('#table-rules tr:last').after(tmp);
        data = data['res'];
        var tmpHtml = [];
        $.each(data, function(k,v){
            tmpHtml.push('<tr><td>');
            tmpHtml.push('<a data-original-title="详情"  data-target="#own-',v['ek_id'],'" rel="tooltip" data-toggle="modal" class="btn details ">');
            tmpHtml.push(v['entry'],'</a></td><td>',v['key'],'</td> <td>',v['message'],'</td><td>',v['state'],'</td> <td>',v['count'],'</td> <td>',getLocalTime(v['start_time']),'</td> </tr>');
        });
        tmpHtml = tmpHtml.join('');
        $('#all-tr').nextAll('tr').each(function(){
            $(this).remove();
        }).end().after(tmpHtml);
        ////console.log(data)

    });
    $('#e15').select2('val','');
    $('#item-save').attr('disabled', false);

});



function del_item(id){
    $.get('/Monitor/Pigeons/ajaxDelRuleItem',{'id':id}, function(data){
        var idValue = ['tr-rule', id].join('-');
        idValue=['#', idValue].join('');
        $(idValue).remove();
        var tmpHtml = [];
        $.each(data,function(k,v){
            tmpHtml.push('<tr><td>');
            tmpHtml.push('<a data-original-title="详情"  data-target="#own-',v['ek_id'],'" rel="tooltip" data-toggle="modal" class="btn details ">');
            tmpHtml.push(v['entry'],'</a></td><td>',v['key'],'</td> <td>',v['message'],'</td><td>',v['state'],'</td> <td>',v['count'],'</td> <td>',v['start_time'],'</td> </tr>');
        });
        tmpHtml = tmpHtml.join('');
        $('#all-tr').nextAll('tr').each(function(){
            $(this).remove();
        }).end().after(tmpHtml);
    });
    return false;
}

/*
maintenance 的相关处理
 */


$(document).on('click', '.handle', function(){
    var values = $(this).attr('value').split(',,');
    var value = values[0];
    var tar = $(this).attr('data-target');
    var id = tar.split('-').pop();
    var val = tar.substr(1);
    var state = values[1];
    $('.modal-body').children().remove();
    $.get('/Monitor/Pigeons/getHandleLeaveState', {'state':state}, function(data){
        console.log(data);
        var tmp = ['<table class="table table-striped" id="addH"> <tbody>'];
        tmp.push('<tr><td>结束时间</td><td>状态</td><td>操作</td></tr>')
        var startDateHtml = '<input type="text" class="form-control "   id="end_time_picker" />';
        tmp.push('<tr><td>', startDateHtml, '</td><td><select class="form-control " id="handle-state">  ');
        $.each(data,function(k,v){
            tmp.push('<option value="',k,'">',v,'</option>');
        })
        tmp.push('</select></td><td><a class="btn btn-default bordered" id="hAdd" value="',id,'">受理</a></td></tr>');
        tmp.push('</tbody></table>');
        tmp = tmp.join('');
        $('.modal-body').append(tmp);
        $('#myModalLabel').text(value);
        $('.modal').attr('id', val);

    })




})

$(document).on('click', '#hAdd', function(){
    var  id = $(this).attr('value');
    var endTime = $('#end_time_picker').prop('value');
    var state = $('#handle-state').val();
    endTime = get_unix_time(endTime);
    var tmp ='';
    $('#addH').siblings().each(function(){
        $(this).remove();
    });
    $.get('/Monitor/Pigeons/ajaxAddHandle', {'id':id, 'endTime':endTime, 'state':state}, function(data){
        var stateVal = data['stateVal'];
        data = data['res'];
        if(data==-1){
            alertType='alert-warning';
            alertMess='不可选择过去的时间';
        }else if(data==0){
            alertType='alert-warning';
            alertMess='结束时间段处于运维状态';
        }else{
            alertType='alert-success';
            alertMess='受理成功';
            var utcEndTime = getLocalTime(endTime);
            tmp = ['<tr><td>',utcEndTime,'</td><td>',stateVal,'</td><td><a href="#" class="del-h" id="h-',id,'">',,'删除</a></td>'].join('');
        }
        var alertInfo = ['<div class="alert ',alertType,' alert-dismissable">'];
        alertInfo.push('<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>');
        alertInfo.push(alertMess,'</div>');
        alertInfo = alertInfo.join('');
        $('#addH').before(alertInfo);
        if(data!=-1){
            $('#addH tr:last').remove();
            $('#addH tr:last').after(tmp);
        }

    })
})


$(document).on('click','.del-h', function(){
    var id = $(this).attr('id').split('-')[1];
    $.get('/Monitor/Pigeons/ajaxDelHandle', {'id':id}, function(data){

    })
})

$(document).on('click', '#save-rule', function(){
    var name = $('#rule_name').val();
    var users = $('#e12').val()
    $.get('/Monitor/Pigeons/ajaxSaveRule',{'name':name, 'users':users}, function(data){
        location.href="/Monitor/Pigeons/index";
    });
})

$(document).on('focus','#end_time_picker', function(){
    $(this).datetimepicker();
})

$(document).on('focus','#start_time_picker', function(){
    $(this).datetimepicker();
})

/*
把时间转换为时间戳的函数
 */

function get_unix_time(dateStr)
{
    var newstr = dateStr.replace(/-/g,'/');
    var date =  new Date(newstr);
    var time_str = date.getTime().toString();
    var time = parseInt(time_str.substr(0, 10));
    return time;
}

function getLocalTime(nS) {
    return new Date(parseInt(nS) * 1000).toLocaleString();
    //return new Date(parseInt(nS) * 1000).toLocaleString().substr(0,20);
}



$(document).on('hidden.bs.modal', '.modal-hAdd', function(){
    var tmp = '';

    $.get('/Monitor/Pigeons/ajaxGetDashboard',{}, function(data){
        console.log(data);
        tmp=makeTab(data);
        tmp = tmp.join('');
        $('#home-tr').nextAll().each(function(){
            $(this).remove();
        }).end().after(tmp);
    });
    return false;
})



function makeTab(data)
{
    if(data.length<=0){
        return [];
    }else{
        var tmp=[];
        $.each(data,function(k,v){
            tmp.push('<tr> <td ><a class="btn bordered details " data-toggle="modal"  rel="tooltip"  data-target="#own-',v.ek_id,'" data-original-title="详情">');
            tmp.push(v.entry,'</a>');
            tmp.push('</td> <td > <span class="tag">',v.key,'</span> </td> <td ><span class="tag">',v.message,'</span></td>');
            tmp.push('<td><span class="tag">',v.stateVal, '</span></td> <td >',v.count,'</td> <td >',v.firstTime,'</td>');
            if(v.is_done == 0){
                tmp.push(' <td > <a class="btn  handle  btn-default bordered" data-toggle="modal"  rel="tooltip"  data-target="#handle-', v.ek_id,'"   value="', v.entry,',,', v.state,'" data-original-title="受理该机器">');
                tmp.push('受理 </a> </td>');
            }else{
                tmp.push('<td > <span class="tag">',v.done.stateVal,'</span> <span class="tag">',v.done.endTime,'</span> </td>');
            }
            tmp.push('</tr>');
        });
        return tmp;
    }

}

function makeTab2(data)
{
    var tmp=[];
    if(data.length<=0){
        return [];
    }else{
        $.each(data,function(k,v){
            tmp.push('<tr> <td ><a class="btn bordered details " data-toggle="modal"  rel="tooltip"  data-target="#own-',v.ek_id,'" data-original-title="详情">');
            tmp.push(v.entry,'</a>');
            tmp.push('</td> <td > <span class="tag">',v.key,'</span> </td> <td ><span class="tag">',v.message,'</span></td>');
            tmp.push('<td>',v.state,'</td> <td >',v.count,'</td> <td > ',v.firstTime,'</td>');
            tmp.push('</tr>');
        });
        return tmp;
    }
}


/*
检查用户输入的值
 */
$('#save-rule').attr('disabled',true);

$('#rule_name').on('blur',function(){
    var value  = $(this).prop('value');
    var type='';
    if($(this).hasClass('save-rule')){
        type='#save-rule';
    }else{
        type='#update-rule';
    }
    value = $.trim(value)
    if(!isNaN(value)){
        //$('#alert-val').text('不可全为数字');
        //$('#alert-rule').removeClass('hidden');
        $(type).attr('disabled',true);
    }else if(value.length==0){
        $(type).attr('disabled',true);
    }else{
        $.get('/Monitor/Pigeons/checkRuleName',{'rule':value}, function(data){
            if(data == -1) {
                $('#alert-val').text('请更新当前名字');
                $('#alert-rule').removeClass('hidden');
                $(type).attr('disabled',true);
            }else{
                $('#alert-rule').addClass('hidden');
                $(type).attr('disabled',false);
            }
        })
    }

})





// main page

function resultFormatResult(medata) {

    return medata.text;
}

function resultFormatSelection(medata) {
    return medata.text;
}



var userParm ={
    tags: [],
    allowClear:true,
    data:[],
    multiple:true,
    placeholder: "请输入参数",
    minimumInputLength: 1,
    separator:',,',
    ajax: {
        url: "/Monitor/Pigeons/ajaxGetUser",
        data: function (term, page) {
            return {
                q: term,
                page_limit: 5
            };
        },
        dataType: 'json',
        results: function (data, page) {
            return { results: data };
        },
        formatResult: resultFormatResult,
        formatSelection: resultFormatSelection,
        dropdownCssClass: "bigdrop",
        escapeMarkup: function (m) { return m; }
    }
}

var selectParm ={
    tags: [],
    allowClear:true,
    data:[],
    multiple:true,
    placeholder: "请输入参数",
    minimumInputLength: 1,
    separator: ',,',
    ajax: {
        //url: "/Monitor/Pigeons/ajaxGetItem",
        maximumSelectionSize:1,
        url:"/Monitor/Pigeons/ajaxSelect2GetItem",
        data: function (term, page) {
            return {
                q: term,
                page_limit: 5,
                tag:$('#e9').val()
            };
        },
        dataType: 'json',
        results: function (data, page) {
            return { results: data };
        },
        formatResult: resultFormatResult,
        formatSelection: resultFormatSelection,
        dropdownCssClass: "bigdrop",
        escapeMarkup: function (m) { return m; }
    }
}

var chooseParm ={
    allowClear:true,
    data:[],
    placeholder: "请输入参数",
    minimumInputLength: 0,
    separator:',,',
    ajax: {
        url:"/Monitor/Pigeons/ajaxGetChooseItems",
        data: function (term, page) {
            return {
                q: term,
                page_limit: 5
            };
        },
        dataType: 'json',
        results: function (data, page) {
            return { results: data };
        },
        formatResult: resultFormatResult,
        formatSelection: resultFormatSelection,
        dropdownCssClass: "bigdrop",
        escapeMarkup: function (m) { return m; }
    }
}


/*select2 的相关操作
 */
$('#e9').select2(chooseParm);
$('#e12').select2(userParm);
$('#e15').select2(selectParm);



$('#e9').on('change',function(){
    $('.item-do').each(function(){
        $(this).attr('disabled', true);
    });
    $('#e15').select2('val','');
});

$('#e15').on('change', function(){
    var val = $(this).val();
    if(val.length>0){
        $('.item-do').each(function(){
            $(this).attr('disabled', false);
        });

    }
})


$(document).on('focus','#end_time_picker', function(){
    $(this).datetimepicker();
})
$(document).on('focus','#start_time_picker', function(){
    $(this).datetimepicker();
})

function get_unix_time(dateStr)
{
    var newstr = dateStr.replace(/-/g,'/');
    var date =  new Date(newstr);
    var time_str = date.getTime().toString();
    var time = parseInt(time_str.substr(0, 10));
    return time;
}


// loadpage
function reloadPage()
{
    $.get('/Monitor/Pigeons/ajaxReloadDashboard',{},function(data){
        var isSearch = data['isSearch'];
        if(isSearch==-1){
            return false;
        }
        var allInfoTab = makeTab2(data['allDashes']).join('');
        var userInfoTab = makeTab(data['userDashes']).join('');

        $('#home-tr').nextAll().each(function(){
            $(this).remove();
        }).end().after(userInfoTab);
        $('#all-tr').nextAll().each(function(){
            $(this).remove();
        }).end().after(allInfoTab);

    })
}

timer=setInterval('reloadPage()',10000);

