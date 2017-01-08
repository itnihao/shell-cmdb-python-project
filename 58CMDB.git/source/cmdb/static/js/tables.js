function GetIdc(){
    token = GetToken();
    if(token == 'error'){
      alert('Token过期');
      return false;
    }
    token = token.data.token;
    //token for api
    //data = 'token=' + token;
    data = {'token':token};
    data = JSON.stringify(data);
    url = '/api/idc/getidcinfoall/';
    idc = ajax(url, 'POST', data, 'json');
    return idc;
}

function GetRepairsServer(){

  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }
  token = token.data.token;
  data = {'token':token, 'num': 20};
  data = JSON.stringify(data);

  url = '/api/server/getrepair/';
  server = ajax(url, 'POST', data, 'json');
  return server;
}


function EditIdc(o){
  $('#myModal').modal('show');
  fields = o.fields;
  pk = o.pk;
  $('#idc_name').val(fields.idc_name);
  $('#idc_region').val(fields.idc_region);
  $('#idc_zone').val(fields.idc_zone);
  $('#idc_address').val(fields.idc_address);
  $('#idc_supplier').val(fields.idc_supplier);
  $('#idc_resource_type').val(fields.idc_resource_type);
  $('#idc_contacts').val(fields.idc_contacts);
  $('#idc_phone').val(fields.idc_phone);
  $('#idc_fax').val(fields.idc_fax);
  $('#idc_email').val(fields.idc_email);
  $('#idc_owner_master_id').val(fields.idc_owner_master_id);
  $('#idc_owner_backup_id').val(fields.idc_owner_backup_id);
  $('#idc_enable_time').val(fields.idc_enable_time);
  $('#idc_due_time').val(fields.idc_due_time);
}

function AddIdc(){
    $('#myModal').modal('show');
    $('#myModal :input').val('');
}

function DelIdc(o){
  $('#del_idc').modal('show');
  alert(o);
}

function ShowServerList(pk){
    $('#myModal').modal('show');
    token = GetToken();
    if(token == 'error'){
      alert('Token过期');
      return false;
    }
    token = token.data.token;
    //data = 'token=' + token + '&pk=' + pk;
    data = {'token':token, 'pk':pk};
    data = JSON.stringify(data);
    url = '/api/server/getserverdetailedinfo/';
    server = ajax(url, 'POST', data, 'json');
    if(server.code == 0){
      data = server.data[0];
      var htm = [];
      htm.push('<tr><th>sn</td><td>'+data.sn+'</td><th>设备类型</th><td>'+data.device_type+'</td></tr>');
      htm.push('<tr><th>厂商</th><td>'+data.producer+'</td><th>上架时间</th><td>'+data.asset_on_shelf_time+'</td></tr>');
      htm.push('<tr><th>过保日期</th><td>'+data.asset_warranty_due_time+'</td><th>操作系统信息</th><td>'+data.os+'</td></tr>');
      htm.push('<tr><th>内网IP</th><td>'+data.inip+'</td><th>掩码</th><td>'+data.in_mask+'</td></tr>');
      htm.push('<tr><th>外网IP</th><td>'+data.outip+'</td><th>掩码</th><td>'+data.out_mask+'</td></tr>');
      htm.push('<tr><th>设备位置</th><td>'+data.position+'</td><th>设备型号</th><td>'+data.server_type+'</td></tr>');
      htm.push('<tr><th>运维管理员</th><td>'+data.op_user_name+' ('+data.op_user+') '+data.op_user_phone+'</td><th>所属业务线</th><td>'+data.busline+'</td></tr>');
      htm.push('<tr><th>业务线管理员</th><td>'+data.buline_user_name+' ('+data.buline_user+') '+data.buline_user_phone+'</td><th>宿主资产编号</th><td><font color="#FF0000">'+data.domain0+'</font></td></tr>');
      var htm_val = htm.join('');

      $('#tab1 > table').children().remove().end().append(htm_val);

      htm = [];
      htm.push('<tr><th>处理器</td><td>'+data.cpu_info+'</td></tr>');
      htm.push('<tr><th>内存</td><td>'+data.memory_info+'</td></tr>');
      htm.push('<tr><th>硬盘</td><td>'+data.disk_info+'</td></tr>');
      htm.push('<tr><th>网卡</td><td>'+data.net_card+'</td></tr>');
      var server_pk = data.pk;
      var htm_val = htm.join('');

      $('#tab2 > table').children().remove().end().append(htm_val);
        token = GetToken();
        if(token == 'error'){
          alert('Token过期');
          return false;
        }
        token = token.data.token;
        //token for api
    	data = {
    		'token':token,
    		'server_pk':server_pk
    		};
    	data = JSON.stringify(data);
      url = '/api/logger/serverlog/';
      server = ajax(url, 'POST', data, 'json');
    	var datatable = $('#tab3 > table').dataTable({
        "aoColumns": [
            {
                "mDataProp": "pk",
                "sClass": "center",
                "mRender": function (pk) {
                    return "<label class='pos-rel'> <input type='checkbox' class='ace' value='" + pk + "'> <span class='lbl'></span> </label>";
                },
//"sWidth":"5%",
                "bSortable": false
            },
            {"mData": "las_time"},
            {"mData": "auther"},
            {"mData": "context"},
            {
                "mDataProp": "num",
              //  "mRender": function (fields, type, full) {
              //      return "<a class='tooltip-error'  title='查看详情' onclick='ShowServerList(" + full.pk + ");'>" + fields + "</a>";
              //  },
            },
        ],}
      );//.api();
      var datatable2 = $('#tab3 > div > table').dataTable().api();
    	datatable2.clear();
    	datatable2.rows.add(server.data);
    	datatable2.draw();
    }else{
      return false;
    }

}

function ShowRepairServerDetail(pk){
    $('#myModal').modal('show');
    token = GetToken();
    if(token == 'error'){
      alert('Token过期');
      return false;
    }
    token = token.data.token;
    //data = 'token=' + token + '&pk=' + pk;
    data = {'token':token, 'pk':pk};
    data = JSON.stringify(data);
    url = '/api/server/getserverdetailedinfo/';
    server = ajax(url, 'POST', data, 'json');
    if(server.code == 0){
      //console.log(server.data);
      //data = server.data;
      data = server.data[0];
      //console.log(data.inip);

      $('#asset_type').val(data.device_type);
      $('#producer').val(data.producer);
      $('#server_type').val(data.server_type);
      $('#os').val(data.os);
      $('#inip_info').val(data.inip);
      $('#outip_info').val(data.outip);
      $('#inmask').val(data.in_mask);
      $('#outmask').val(data.out_mask);
      $('#sn').val(data.sn);
      $('#position').val(data.position);
      // $('#cpu').val(data.cpu_info);
      // $('#memory').val(data.memory_info);
      // $('#disk').val(data.disk_info);
      // $('#netcard').val(data.net_card);
      $('#warranty').val(data.asset_warranty_due_time);
      $('#shelf_time').val(data.asset_on_shelf_time);
      // $('#modal-table').val();
      jumpto = "/repairorderform/?sn=" + data.sn;
      // console.log(jumpto);
      $("#jumpto_repair_order").attr("href", jumpto);
      // console.log(data.sn);
      repair_info = Get_Repair_Info(data.sn);

    }else{
      return false;
    }

}

var memoryClickID;
function ShowBuslineDetail(id){
    $('#myModal').modal('show');
    memoryClickID = id;
    // console.log(memoryClickID);
}

function ServerSearch(){
	var datatable = $('#dynamic-table').dataTable().api();
	datatable.clear();
	datatable.draw();
}

function ServerReset(){
	$('#inip').val('');
	$('#outip').val('');
	$('#bmcip').val('');
	$('#accessno').val('');
  $('#cluster').val('');
  $('#incservertype').val('');
  $('#servertype').val('');
  $('#servermodel').val('');
  $('#accesssn').val('');
}

function IpSearch(){
  var datatable = $('#dynamic-table').dataTable().api();
  datatable.clear();
  datatable.draw();
}

function IpReset(){
	$('#ip').val('');
	$('#iptype').val('');
	$('#accessno').val('');
}

function GetRepairDetail(pk){

  token = GetToken();
  if(token == 'error'){
    alert('Token过期');
    return false;
  }
  token = token.data.token;

  data = {'token':token, 'pk':pk};
  data = JSON.stringify(data);
  url = '/api/server/getserverdetailedinfo/';
  server = ajax(url, 'POST', data, 'json');
  if(server.code == 0){
    //console.log(server.data);
    //data = server.data;
    data = server.data[0];
    //console.log(data.inip);

    $('#asset_type').val(data.device_type);
    $('#producer').val(data.producer);
    $('#server_type').val(data.server_type);
    $('#os').val(data.os);
    $('#inip_info').val(data.inip);
    $('#outip_info').val(data.outip);
    $('#inmask').val(data.in_mask);
    $('#outmask').val(data.out_mask);
    $('#sn').val(data.sn);
    $('#position').val(data.position);
    // $('#cpu').val(data.cpu_info);
    // $('#memory').val(data.memory_info);
    // $('#disk').val(data.disk_info);
    // $('#netcard').val(data.net_card);
    $('#warranty').val(data.asset_warranty_due_time);
    $('#shelf_time').val(data.asset_on_shelf_time);
    // $('#modal-table').val();
    jumpto = "/repairorderform/?sn=" + data.sn;
    // console.log(jumpto);
    $("#jumpto_repair_order").attr("href", jumpto);

  }else{
    return false;
  }

}

function Get_Repair_Info(sn){
  token = GetToken();
  if(token == 'error'){
    alert('Token过期');
    return false;
  }
  token = token.data.token;
  //data = 'token=' + token + '&pk=' + pk;
  data = {'token':token, 'sn':sn};
  data = JSON.stringify(data);
  url = '/api/server/getrepairinfo/';
  repair = ajax(url, 'POST', data, 'json');
  appendInput(repair);
  return repair;
}

function appendInput(content){
  var data = [];
  try {
    data = content["data"];
  } catch (e) {

  } finally {

  }
  try {
//  删除之前动态插入的input标签
    var time = document.getElementById("repair_time");
    var time_input = document.getElementById("repair_end_time");
    while (time_input) {
      time.removeChild(time_input);
      time_input = document.getElementById("repair_end_time");
    }

    var time = document.getElementById("repair_persion");
    var time_input = document.getElementById("repair_user");
    while (time_input) {
      time.removeChild(time_input);
      time_input = document.getElementById("repair_user");
    }

    var time = document.getElementById("repair_reason");
    var time_input = document.getElementById("repair_info");
    while (time_input) {
      time.removeChild(time_input);
      time_input = document.getElementById("repair_info");
    }

  } catch (e) {

  } finally {

  }

  if (data && data.length>0) {
    // console.log(data);
    for (var i = 0; i < data.length; i++) {
      var dict = data[i];
      // console.log(dict);

      var time = dict["repair_end_time"];
      var input_time = '<input type="text" class="form-control" id="repair_end_time" placeholder="维修时间" value="' + time + '" readonly>';
      $("#repair_time").append(input_time);

      var persion = "Manager";//dict["repair_end_time"];
      var input_persion = '<input type="text" class="form-control" id="repair_user" placeholder="维修人" value="' + persion + '" readonly>';
      $("#repair_persion").append(input_persion);

      var reasons = dict["context"];
      var input_reasons = '<input type="text" class="form-control" id="repair_info" placeholder="维修内容" value="' + reasons + '" readonly>';
      $("#repair_reason").append(input_reasons);
    }
  }else {
    var input_time = '<input type="text" class="form-control" id="repair_end_time" placeholder="维修时间" readonly>';
    $("#repair_time").append(input_time);

    var input_persion = '<input type="text" class="form-control" id="repair_user" placeholder="维修人" readonly>';
    $("#repair_persion").append(input_persion);

    var input_reasons = '<input type="text" class="form-control" id="repair_info" placeholder="维修内容" readonly>';
    $("#repair_reason").append(input_reasons);
  }
}


function CreateRepair(){
  //get repair info
  var sn = $('#sn').val();

  var repair_context = $('#reason').val();

  token = GetToken();
  if(token == 'error'){
    alert('Token过期');
    return false;
  }
  token = token.data.token;
  if($("#inputcheckbox").is(':checked')){
    ChageMonitor(sn, 'close');
    data = {'token':token, 'sn': sn, 'context': repair_context, 'offline': 1};
  }else {
    data = {'token':token, 'sn': sn, 'context': repair_context};
  }

  data = JSON.stringify(data);
  console.log(data);
  url = '/api/server/createrepair/';
  repair = ajax(url, 'POST', data, 'json');
  window.location.href="/repairorderform/?sn=" + sn;

  //console.log(data);

}

function ChageMonitor(hostname, flag){
  token = GetToken();
  if(token == 'error'){
    alert('Token过期');
    return false;
  }
  token = token.data.token;
  flag = flag;
  hostname = hostname;
  d = {'token':token, 'flag': flag, 'hostname': hostname};
  d = JSON.stringify(d);
  url = '/api/server/monitor/';
  re = ajax(url, 'POST', d, 'json');
}

function GetSntoRepair(sn){
  if(sn){
    sn = sn;
  }else{
    sn = $("#repair_sn").val();
  }
  //console.log(sn);
  window.location.href="/repairorderform/?sn=" + sn;
}

function UpdateRepairStep(step){

  sn = $('#sn').val();
  token = GetToken();
  if(token == 'error'){
    alert('Token过期');
    return false;
  }
  token = token.data.token;

  data = {'token': token, 'sn': sn, 'step': step};
  data = JSON.stringify(data);
  url = '/api/server/updaterepairstep/'
  result = ajax(url, 'POST', data, 'json');
  window.location.href="/repairorderform/?sn=" + sn;
  // console.log(data);
}

// 业务线相关

function GetBuslineInfo(level){
  level = arguments[0]?arguments[0]:0;
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }
  token = token.data.token;
  data = {'token':token, 'level':level};
  data = JSON.stringify(data);
  url = '/api/busline/buslineinfo/'
  result = ajax(url, 'POST', data, 'json');

  // console.log(result);
  return result;
}

function BuslineSearch(){
	// var id=$('#InputID').val();
	var name=$('#InputName').val();
	var op=$('#InputOP').val();
	var manager=$('#InputManager').val();

    token = GetToken();
    if(token == 'error'){
      alert('Token过期');
      return false;
    }
    token = token.data.token;
    //token for api
	data = {
		'token':token,
		// 'id':id,
		'name':name,
		'op':op,
		'manager':manager,
		};
	data = JSON.stringify(data);
    url = '/api/busline/searchbuslineinfo/';
    server = ajax(url, 'POST', data, 'json');

	var datatable = $('#dynamic-table').dataTable().api();
	datatable.clear();
	datatable.rows.add(server.data);
	datatable.draw();
}

function BuslineReset(){
	$('#InputID').val('');
	$('#InputName').val('');
	$('#InputOP').val('');
	$('#InputManager').val('');
}

function GetBspOrgList(bl_id){

  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }
  token = token.data.token;
  data = {'bol_id':bl_id, 'token':token};
  data = JSON.stringify(data);
  url = '/api/busline/getbsporgtree/';
  result = ajax(url, 'POST', data, 'json');
  // console.log(result);
  return result;
}

function GetAllBspOrgList(){
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }
  token = token.data.token;
  data = {'token':token};
  data = JSON.stringify(data);
  url = '/api/busline/getallbsporgtree/';
  result = ajax(url, 'POST', data, 'json');
  // console.log(result);
  return result;
}

// function GetBspUser(buslineid){
//   if (!buslineid) {
//     alert('请选择业务线');
//     return;
//   }
//
//   token = GetToken();
//   if (token == 'error') {
//     alert('Token过期');
//     return false;
//   }
//   console.log(buslineid);
//   token = token.data.token;
//   data = {'buslineid':buslineid, 'token':token};
//   data = JSON.stringify(data);
//   url = '/api/cluster/getbspuser/';
//   result = ajax(url, 'POST', data, 'json');
//   console.log(result);
//   return result;
//
// }

// function MouseOver(x){
//   x.style.background="#b0c4de"
// }
//
// function MouseLeave(x){
//   x.style.background="#FFFFFF"
// }

// function Animation(x){
//   childlist = x.childNodes;
//   var x_id = x.getAttribute("id").substr(1);
//   var div = $(x);
//   if (childlist.length<=0) {
//     //还没有子标签，也就是还没有点开过
//     bsp_org_data = GetBspOrgList(x_id).data;
//     if (bsp_org_data.length<=0) {
//       //没有子对象，此时选中
//       $('#myModal').modal('hide');
//       LinkBspOrg(x_id);
//     }else {
//       for (var i=0; i<bsp_org_data.length; i++){
//         obj = bsp_org_data[i];
//         var bspname = obj.org_name;
//         var bspid = 'a' + obj.org_id.toString();
//         var tag = '<ul><li style="list-style-type:none" onmouseover="MouseOver(this)" onmouseout="MouseLeave(this)" onclick="Animation('+ bspid +')">"' + bspname + '"</li><div id="' + bspid + '"></div></ul>';
//         div.append(tag);
//       };
//     }
//   }else {
//     div.slideToggle();
//   }
// }

function AddModelElement(){
  bsp_org_data = GetBspOrgList().data;
  // console.log(bsp_org_data);
  for (var i=0; i<bsp_org_data.length; i++){
    obj = bsp_org_data[i];
    var bspname = obj.org_name;
    var bspid = 'a' + obj.org_id.toString();
    // console.log(typeof bspid);
    // console.log(bspid);
    var tag = '<ul><li style="list-style-type:none" onmouseover="MouseOver(this)" onmouseout="MouseLeave(this)" onclick="Animation('+ bspid +')"><span class="ui-accordion-header-icon ui-icon ui-icon-triangle-1-e"></span>"' + bspname + '"</li><div id="' + bspid + '"></div></ul>';
    $('.list-group').append(tag);
  };
}

function LinkBspOrg(link_id){

  // console.log(link_id);
  token = GetToken();
  if (token=='error') {
    alert('Token过期');
    return false;
  }

  token = token.data.token;
  data = {'token':token, 'buslineid':memoryClickID,'linkbsporgid':link_id};
  data = JSON.stringify(data);
  url = '/api/busline/linkbsporg/';
  result = ajax(url, 'POST', data, 'json');
  return result
}

function ShowBspOrgDetail(bsporgid){

  window.location.href='/busline/detail/?id=' + bsporgid;

}

function saveChange(content){
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }
  token = token.data.token;
  content['token']=token;
  // console.log('append:');
  // console.log(content);
  content = JSON.stringify(content);
  // console.log(content);
  url = '/api/busline/savebusline/';
  result = ajax(url, 'POST', content, 'json');
  if (result.data) {
    alert('操作成功！');
  }else {
    alert('操作失败！');
  }
  return result
}

function setBuslineList(){
  if ($('#parentDiv li').size() > 0) {
    $('#parentDiv').slideToggle();
    return true;
  }
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }

  token = token.data.token;
  data = {'token':token};
  data = JSON.stringify(data);
  url = '/api/busline/allbuslines/';
  result = ajax(url, 'POST', data, 'json');
  dealwithBuslineList(result);
  // console.log('busline:',result);
  return result
}

function JustGetBuslineData(){
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }

  token = token.data.token;
  data = {'token':token};
  data = JSON.stringify(data);
  url = '/api/busline/allbuslines/';
  result = ajax(url, 'POST', data, 'json');
  return result
}

function dealwithBuslineList(data){
  if ($('#parentDiv li').size() > 0) {
    $('#parentDiv').slideToggle();
    return true;
  }
  var data = data.data;
  var temp = [];
  var level = 0;
  for (var i = 0; i < data.length; i++) {
    var obj = data[i];
    temp.push(obj);
    if (!obj.busline_level) {
      continue;
    }
    level = parseInt(level)>parseInt(obj.busline_level)?parseInt(level):parseInt(obj.busline_level);
  }
  var maxLevel = level;
  var list = [];
  var tapList = [];
  for (var i = level; i >= 0; i--) {
    var levelList = [];
    for (var j = 0; j < temp.length; j++) {
      var obj = temp[j];
      if (parseInt(obj.busline_level) == i) {
        var name = obj.busline_name;
        var id = obj.busline_id;
        var parent = obj.parent_id;
        var dic = {
                    'text': name,
                    // 'nodes': [],
                    'id': id,
                    'parentID': parent,
                    'level': i.toString()
                  }
        tapList.push(dic);
        levelList.push(dic);
      }
    }
    list.push(levelList);
  }

  console.log('after:',list);

  for (var i = 0; i < list.length-1; i++) {
    var arr1 = list[i];
    var arr2 = list[i+1];
    for (var j = 0; j < arr1.length; j++) {
      var obj = arr1[j];
      for (var k = 0; k < arr2.length; k++) {
        var parentObj = arr2[k];
        if (parentObj.id == obj.parentID) {
          if (!parentObj['nodes']) {
            parentObj['nodes'] = [];
          }
          var tempArr = parentObj['nodes'];
          tempArr.push(obj);
          break;
        }
      }
    }
  }
  // console.log('aaaa');
  // console.log(list);
  // console.log('aaaa');
  tapList = tapList.reverse();
  tapContent1 = '<span class="icon expand-icon glyphicon glyphicon-minus"></span>'
  tapContent2 = '<span class="icon glyphicon"></span>'
  tapContent3 = '<span class="indent"></span>'
  var count = 1;
  for (var i = 0; i < tapList.length; i++) {

    var obj = tapList[i];
    if (parseInt(obj.level)>0) {
      if (parseInt(obj.level)==1) {
        count = count + 1;
      }
      continue;
    }
    tapHead = '<li class="list-group-item node-parentDiv" data-nodeid="'+ i +'" style="color:undefined;background-color:undefined;">'
    tap = tapHead;
    for (var j = 0; j < parseInt(obj.level); j++) {
      tap = tap + tapContent3;
    }
    if (parseInt(obj.level)<parseInt(maxLevel)) {
      tap = tap + tapContent1;
    }else {
      tap = tap + tapContent2;
    }

    tapTail = '<span class="icon node-icon"></span> \
               "' + obj.text + '" \
               </li>'
    tap = tap + tapTail;

    // $('#treeULTap').append(tap);
  }

  //设置背景半透明的黑色的范围
  var style = $('.modal-backdrop').attr('style');
  if (style) {
    var value = style.replace(/[^0-9]/ig,"");
    value = parseInt(value) + parseInt(count*41);
    style = 'height: ' + value.toString() + 'px';
    $('.modal-backdrop').attr('style', style);
  }

  var result = list[list.length-1];
  // console.log(result);

  $('#parentDiv').treeview({
    data: result,
    onNodeSelected: function(event, node) {
      //点击选中
      selectBusline(node.id);
    },
    onNodeExpanded: function(event, node) {
      //修改黑色背景
      var style = $('.modal-backdrop').attr('style');
      if (style) {
        var value = style.replace(/[^0-9]/ig,"");
        value = parseInt(value) + parseInt(node.nodes.length*41);
        style = 'height: ' + value.toString() + 'px';
        $('.modal-backdrop').attr('style', style);
      }
    },
    onNodeCollapsed: function(event, node) {
      //修改黑色背景
      var style = $('.modal-backdrop').attr('style');
      if (style) {
        var value = style.replace(/[^0-9]/ig,"");
        value = parseInt(value) + parseInt(node.nodes.length*41);
        style = 'height: ' + value.toString() + 'px';
        $('.modal-backdrop').attr('style', style);
      }
    }
  });
}

function setBspOrgList(){
  if ($('#parentDiv1 li').size() > 0) {
    $('#parentDiv1').slideToggle();
    return true;
  }
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }

  token = token.data.token;
  data = {'token':token};
  data = JSON.stringify(data);
  url = '/api/busline/allbsporg/';
  result = ajax(url, 'POST', data, 'json');
  // console.log('result:',result);
  dealwithBspOrgList(result);
  return result
}

function JustGetBspOrgData(){
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }

  token = token.data.token;
  data = {'token':token};
  data = JSON.stringify(data);
  url = '/api/busline/allbsporg/';
  result = ajax(url, 'POST', data, 'json');
  return result
}

function dealwithBspOrgList(data){
  if ($('#parentDiv1 li').size() > 0) {
    $('#parentDiv1').slideToggle();
    return true;
  }
  var data = data.data;
  var temp = [];
  var level = 0;
  for (var i = 0; i < data.length; i++) {
    var obj = data[i];
    temp.push(obj);
    // console.log(obj.org_level);
    // if (!obj.org_level) {
    //   continue;
    // }
    level = parseInt(level)>parseInt(obj.org_level)?parseInt(level):parseInt(obj.org_level);
  }
  var maxLevel = level;

  var list = [];
  var tapList = [];
  for (var i = level; i >= 0; i--) {
    var levelList = [];
    for (var j = 0; j < temp.length; j++) {
      var obj = temp[j];
      if (parseInt(obj.org_level) == i) {
        var name = obj.org_name;
        var id = obj.org_id;
        var parent = obj.parent_id;
        var dic = {
                    'text': name,
                    // 'nodes': [],
                    'id': id,
                    'parentID': parent,
                    'level': i.toString()
                  }
        tapList.push(dic);
        levelList.push(dic);
      }
    }
    list.push(levelList);
  }

  // console.log("list:",list);

  for (var i = 0; i < list.length-1; i++) {
    var arr1 = list[i];
    var arr2 = list[i+1];
    for (var j = 0; j < arr1.length; j++) {
      var obj = arr1[j];
      for (var k = 0; k < arr2.length; k++) {
        var parentObj = arr2[k];
        if (parentObj.id == obj.parentID) {
          if (!parentObj['nodes']) {
            parentObj['nodes'] = [];
          }
          var tempArr = parentObj['nodes'];
          tempArr.push(obj);
          break;
        }
      }
    }
  }

  // console.log(tempArr);

  tapList = tapList.reverse();

  tapContent1 = '<span class="icon expand-icon glyphicon glyphicon-minus"></span>'
  tapContent2 = '<span class="icon glyphicon"></span>'
  tapContent3 = '<span class="indent"></span>'
  var count = 1;
  for (var i = 0; i < tapList.length; i++) {

    var obj = tapList[i];
    if (parseInt(obj.level)>0) {
      if (parseInt(obj.level)==1) {
        count = count + 1;
      }
      continue;
    }
    tapHead = '<li class="list-group-item node-parentDiv" data-nodeid="'+ i +'" style="color:undefined;background-color:undefined;">'
    tap = tapHead;
    for (var j = 0; j < parseInt(obj.level); j++) {
      tap = tap + tapContent3;
    }
    if (parseInt(obj.level)<parseInt(maxLevel)) {
      tap = tap + tapContent1;
    }else {
      tap = tap + tapContent2;
    }

    tapTail = '<span class="icon node-icon"></span> \
               "' + obj.text + '" \
               </li>'
    tap = tap + tapTail;

    // $('#treeULTap_bsp').append(tap);
  }

  //设置背景半透明的黑色的范围
  var style = $('.modal-backdrop').attr('style');
  if (style) {
    var value = style.replace(/[^0-9]/ig,"");
    value = parseInt(value) + parseInt(count*41);
    style = 'height: ' + value.toString() + 'px';
    $('.modal-backdrop').attr('style', style);
  }

  var result = list[list.length-1];
  // console.log(result);

  $('#parentDiv1').treeview({
    data: result,
    onNodeSelected: function(event, node) {
      //点击选中
      // console.log(node);
      selectBsporg(node.id);
    },
    onNodeExpanded: function(event, node) {
      //修改黑色背景
      $('#parentDiv1').treeview({data:result});

      var style = $('.modal-backdrop').attr('style');
      if (style) {
        var value = style.replace(/[^0-9]/ig,"");
        value = parseInt(value) + parseInt(node.nodes.length*41);
        style = 'height: ' + value.toString() + 'px';
        $('.modal-backdrop').attr('style', style);
      }
    },
    onNodeCollapsed: function(event, node) {
      //修改黑色背景
      var style = $('.modal-backdrop').attr('style');
      if (style) {
        var value = style.replace(/[^0-9]/ig,"");
        value = parseInt(value) + parseInt(node.nodes.length*41);
        style = 'height: ' + value.toString() + 'px';
        $('.modal-backdrop').attr('style', style);
      }
    }
  });
}



// function setBsporgList(){
//   if ($('#bsporgDiv li').size() > 0) {
//     $('#bsporgDiv').slideToggle();
//     return true;
//   }
//   bsp_org_data = GetBspOrgList().data;
//   // console.log(bsp_org_data);
//   for (var i=0; i<bsp_org_data.length; i++){
//     obj = bsp_org_data[i];
//     var bspname = obj.org_name;
//     var bspid = 'a' + obj.org_id.toString();
//     // console.log(typeof bspid);
//     // console.log(bspid);
//     var tag = '<ul><li style="list-style-type:none" onmouseover="MouseOver(this)" onmouseout="MouseLeave(this)" onclick="dealwithBsporgListClcik('+ bspid +')"><span class="ui-accordion-header-icon ui-icon ui-icon-triangle-1-e"></span>"' + bspname + '"</li><div id="' + bspid + '"></div></ul>';
//     $('#bsporgDiv').append(tag);
//   };
// }

// function dealwithBsporgListClcik(x){
//   childlist = x.childNodes;
//   var x_id = x.getAttribute("id").substr(1);
//   var div = $(x);
//   if (childlist.length<=0) {
//     //还没有子标签，也就是还没有点开过
//     bsp_org_data = GetBspOrgList(x_id).data;
//     if (bsp_org_data.length<=0) {
//       //没有子对象，此时选中
//       selectBsporg(x_id);
//       // console.log('aaaaaa');
//     }else {
//       for (var i=0; i<bsp_org_data.length; i++){
//         obj = bsp_org_data[i];
//         var bspname = obj.org_name;
//         var bspid = 'a' + obj.org_id.toString();
//         var tag = '<ul><li style="list-style-type:none" onmouseover="MouseOver(this)" onmouseout="MouseLeave(this)" onclick="dealwithBsporgListClcik('+ bspid +')">"' + bspname + '"</li><div id="' + bspid + '"></div></ul>';
//         div.append(tag);
//       };
//     }
//   }else {
//     div.slideToggle();
//   }
// }

function setModelBsporgList(){
  if ($('#parentDiv1_model li').size() > 0) {
    $('#parentDiv1_model').slideToggle();
    return true;
  }

  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }

  token = token.data.token;
  data = {'token':token};
  data = JSON.stringify(data);
  url = '/api/busline/allbsporg/';
  result = ajax(url, 'POST', data, 'json');
  // console.log(result);
  dealwithModelBsporgListClcik(result);
  return result

}

function dealwithModelBsporgListClcik(x){
  var data = x.data;
  var temp = [];
  var level = 0;
  for (var i = 0; i < data.length; i++) {
    var obj = data[i];
    temp.push(obj);
    // console.log(obj.org_level);
    // if (!obj.org_level) {
    //   continue;
    // }
    level = parseInt(level)>parseInt(obj.org_level)?parseInt(level):parseInt(obj.org_level);
  }
  var maxLevel = level;

  var list = [];
  var tapList = [];
  for (var i = level; i >= 0; i--) {
    var levelList = [];
    for (var j = 0; j < temp.length; j++) {
      var obj = temp[j];
      if (parseInt(obj.org_level) == i) {
        var name = obj.org_name;
        var id = obj.org_id;
        var parent = obj.parent_id;
        var dic = {
                    'text': name,
                    // 'nodes': [],
                    'id': id,
                    'parentID': parent,
                    'level': i.toString()
                  }
        tapList.push(dic);
        levelList.push(dic);
      }
    }
    list.push(levelList);
  }

  // console.log(list);

  for (var i = 0; i < list.length-1; i++) {
    var arr1 = list[i];
    var arr2 = list[i+1];
    for (var j = 0; j < arr1.length; j++) {
      var obj = arr1[j];
      for (var k = 0; k < arr2.length; k++) {
        var parentObj = arr2[k];
        if (parentObj.id == obj.parentID) {
          if (!parentObj['nodes']) {
            parentObj['nodes'] = [];
          }
          var tempArr = parentObj['nodes'];
          tempArr.push(obj);
          break;
        }
      }
    }
  }

  // console.log(tempArr);

  tapList = tapList.reverse();

  tapContent1 = '<span class="icon expand-icon glyphicon glyphicon-minus"></span>'
  tapContent2 = '<span class="icon glyphicon"></span>'
  tapContent3 = '<span class="indent"></span>'
  var count = 1;
  for (var i = 0; i < tapList.length; i++) {

    var obj = tapList[i];
    if (parseInt(obj.level)>0) {
      if (parseInt(obj.level)==1) {
        count = count + 1;
      }
      continue;
    }
    tapHead = '<li class="list-group-item node-parentDiv" data-nodeid="'+ i +'" style="color:undefined;background-color:undefined;">'
    tap = tapHead;
    for (var j = 0; j < parseInt(obj.level); j++) {
      tap = tap + tapContent3;
    }
    if (parseInt(obj.level)<parseInt(maxLevel)) {
      tap = tap + tapContent1;
    }else {
      tap = tap + tapContent2;
    }

    tapTail = '<span class="icon node-icon"></span> \
               "' + obj.text + '" \
               </li>'
    tap = tap + tapTail;

    $('#treeULTap_bsp_model').append(tap);
  }

  //设置背景半透明的黑色的范围
  var style = $('.modal-backdrop').attr('style');
  if (style) {
    var value = style.replace(/[^0-9]/ig,"");
    value = parseInt(value) + parseInt(count*41);
    style = 'height: ' + value.toString() + 'px';
    $('.modal-backdrop').attr('style', style);
  }

  var result = list[list.length-1];
  // console.log(result);

  $('#parentDiv1_model').treeview({
    data: result,
    onNodeSelected: function(event, node) {
      //点击选中
      // console.log(node);
      selectModelBsporg(node.id);
    },
    onNodeExpanded: function(event, node) {
      //修改黑色背景
      var style = $('.modal-backdrop').attr('style');
      if (style) {
        var value = style.replace(/[^0-9]/ig,"");
        value = parseInt(value) + parseInt(node.nodes.length*41);
        style = 'height: ' + value.toString() + 'px';
        $('.modal-backdrop').attr('style', style);
      }
    },
    onNodeCollapsed: function(event, node) {
      //修改黑色背景
      var style = $('.modal-backdrop').attr('style');
      if (style) {
        var value = style.replace(/[^0-9]/ig,"");
        value = parseInt(value) + parseInt(node.nodes.length*41);
        style = 'height: ' + value.toString() + 'px';
        $('.modal-backdrop').attr('style', style);
      }
    }
  });
}

function selectBusline(x){

  $('#parentDiv').slideToggle();
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }

  token = token.data.token;
  data = {'token':token, 'currentID':x};
  data = JSON.stringify(data);
  url = '/api/busline/getclickbusline/';
  result = ajax(url, 'POST', data, 'json');
  // console.log(result);
  obj = result.data[0];
  // console.log('obj:',obj);

  $('#input_parent').val(obj.busline_name);
  $('#input_parent').attr('placeholder',obj.busline_id);

  var fullpath = $('#input_fullpath').val();
  if (!fullpath) {
    return;
  }
  // console.log(fullpath);
  var paths = fullpath.split(",");
  // console.log(paths);
  var finalpath = obj.fullpath.toString() + ',' + paths[paths.length-1];
  // console.log(finalpath);
  $('#input_fullpath').val(finalpath);

}

function selectBsporg(x){

  $('#parentDiv1').slideToggle();
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }
  token = token.data.token;
  data = {'token':token, 'currentID':x};
  data = JSON.stringify(data);
  url = '/api/busline/getclickbsporg/';
  result = ajax(url, 'POST', data, 'json');
  obj = result.data[0];

  $('#input_bsporg').val(obj.org_name);
  $('#input_bsporg').attr('placehold',obj.org_id);

}

function selectModelBsporg(x){

  $('#parentDiv1_model').slideToggle();
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }

  token = token.data.token;
  data = {'token':token, 'currentID':x};
  data = JSON.stringify(data);
  url = '/api/busline/getclickbsporg/';
  result = ajax(url, 'POST', data, 'json');
  obj = result.data[0];
  // console.log(obj);
  document.getElementById('input_model_bsporg').value=obj.org_name;
  document.getElementById('input_model_bsporg').placeholder=obj.org_id;

}

function GetCluster(){
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }

  token = token.data.token;
  data = {'token':token};
  data = JSON.stringify(data);
  url = '/api/cluster/getcluster/';
  result = ajax(url, 'POST', data, 'json');
  return result
}

function GetCurrentCluster(id){
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }

  token = token.data.token;
  data = {'token':token, 'clusterid':id};
  data = JSON.stringify(data);
  url = '/api/cluster/getcurrentcluster/';
  result = ajax(url, 'POST', data, 'json');
  return result
}

function SaveCluster(data){

  // console.log(data);
  var busline_id = data.busline_id;
  var cluster_id = data.cluster_id;
  var cluster_name = data.cluster_name;
  var cluster_state = data.cluster_state;
  var cluster_code = data.cluster_code;
  var op_owner = data.op_owner;
  var busline_owner = data.busline_owner;

  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }

  token = token.data.token;
  data = {'token':token, 'busline_id':busline_id, 'cluster_id':cluster_id, 'cluster_name':cluster_name, 'cluster_state':cluster_state, 'cluster_code':cluster_code, 'op_owner':op_owner, 'busline_owner':busline_owner};
  console.log("data:",data);
  data = JSON.stringify(data);
  url = '/api/cluster/savecluster/';
  result = ajax(url, 'POST', data, 'json');
  if (result.data) {
    alert('操作成功');
    location.reload();
  }else {
    alert('操作失败');
  }
}

function ClusterSearchWithBusline(){

	// var name = $('#codeSearch').val();
  // var busline = $('#buslineSearch').val();
  //   token = GetToken();
  //   if(token == 'error'){
  //     alert('Token过期');
  //     return false;
  //   }
  //   token = token.data.token;
  //   //token for api
	// data = {
	// 	'token':token,
	// 	'name':name,
  //   'busline':busline,
	// 	};
	// data = JSON.stringify(data);
  // url = '/api/cluster/clustersearchwithbusline/';
  // server = ajax(url, 'POST', data, 'json');
  // console.log(server);
	var datatable = $('#dynamic-table').dataTable().api();
	datatable.clear();
	// datatable.rows.add(server.data);
	datatable.draw();
}

function ClusterReset(){
	$('#codeSearch').val('');
  $('#buslineSearch').val('');
}

// 业务线相关

function GetPool(){
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }
  token = token.data.token;
  data = {'token':token};
  data = JSON.stringify(data);
  url = '/api/server/getresoursepool/';
  result = ajax(url, 'POST', data, 'json');
  return result;
}

function ShowPoolList(){
  $('#myModal').modal('show');
  return false;
}

function CreatePool(){
  pool_name = $('#pool_name').val();
  description = $('#description').val();
  //console.log(pool_name);
  //console.log(description);
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }
  token = token.data.token;
  data = {'token': token, 'pool_name': pool_name, 'description': description};
  data = JSON.stringify(data);
  url = '/api/server/createresoursepool/';
  result = ajax(url, 'POST', data, 'json');
  if(result.code == 0){
    $('#myModal').modal('hide');
    alert('添加成功');
  }
  return false;

}

function AddSelectPool(){
  pool = GetPool().data;
  select = $('#pool');
  select.append("<option value=''> </option>");
  for(i=0;i<pool.length;i++){
    select.append("<option value='"+pool[i].pk+"'>"+pool[i].resource_pool_name+"</option>");
  }

}

function GetResoursePoll(){
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }
  token = token.data.token;
  data = {'token': token};
  data = JSON.stringify(data);
  url = '/api/server/getresoursepool/';
  back = ajax(url, 'POST', data, 'json');
  return back.data;

}

function GetClusterUser(id){
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }
  token = token.data.token;
  data = {'token':token, 'id':id.toString()};
  data = JSON.stringify(data);
  url = '/api/cluster/getclusteruser/';
  result = ajax(url, 'POST', data, 'json');
  return result.data
}

function GetClusterData(){
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }

  token = token.data.token;
  data = {'token':token};
  data = JSON.stringify(data);
  url = '/api/cluster/getclusterdata/';
  result = ajax(url, 'POST', data, 'json');
  return result;
}

function GetUserData(){
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }

  token = token.data.token;
  data = {'token':token};
  data = JSON.stringify(data);
  url = '/api/cluster/getuserdata/';
  result = ajax(url, 'POST', data, 'json');
  return result;
}

function SaveClusterUserChange(clusteruserid,clusterid,role){
  token = GetToken();
  if (token=='error') {
    alert=('Token过期');
    return false;
  }

  token = token.data.token;
  data = {'token':token, 'clusteruserid':clusteruserid, 'clusterid':clusterid, 'role':role};
  data = JSON.stringify(data);
  url = '/api/cluster/saveclusteruserchange/';
  result = ajax(url, 'POST', data, 'json');

}

function SaveNewClusterUser(clusteruserid,clusterid,userid,role,effect_time,disabled_time,operation_user){
  token = GetToken();
  if (token=='error') {
    alert=('Token过期');
    return false;
  }

  token = token.data.token;
  // console.log(userid.length);
  data = {'token':token, 'clusteruserid':clusteruserid, 'clusterid':clusterid, 'role':role, 'userid':userid, 'startDate':effect_time, 'endDate':disabled_time, 'operation_user':operation_user};
  console.log(data);
  data = JSON.stringify(data);
  url = '/api/cluster/savenewclusteruser/';
  result = ajax(url, 'POST', data, 'json');
  console.log("result:",result);
  if (result.data) {
    alert('操作成功！');
  }else {
    alert('操作失败！');
  }
  return result;
}

function ShowRepairForm(){
  $('#AddFix').modal('show');
  return false;
}

function GetClusterUserCluster(id){
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }
  token = token.data.token;
  data = {'token':token, 'id':id};
  data = JSON.stringify(data);
  url = '/api/cluster/getclusterusercluster/';
  result = ajax(url, 'POST', data, 'json');
  return result;
}

function GetBaseResourceData(id){
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }
  token = token.data.token;
  data = {'token':token, 'type':id};
  data = JSON.stringify(data);
  url = '/api/server/getbaseresource/';
  result = ajax(url, 'POST', data, 'json');
  return result;
}

function SaveBaseResourceChange(type, id, code, name, other){
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }
  token = token.data.token;
  data = {'token':token, 'type':type, 'id':id, 'code':code, 'name':name};
  if (other) {
    data.other = other;
  }
  data = JSON.stringify(data);
  url = '/api/server/savebaseresourcechange/';
  result = ajax(url, 'POST', data, 'json');
  return result;
}

function GetProducerData(){
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }
  token = token.data.token;
  data = {'token':token};
  data = JSON.stringify(data);
  url = '/api/server/getproducerdata/';
  result = ajax(url, 'POST', data, 'json');
  // console.log(result.data);
  return result;
}

function GetUserGroupList(){
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }
  token = token.data.token;
  data = {'token':token};
  data = JSON.stringify(data);
  url = '/api/auth/getallgroups/';
  result = ajax(url, 'POST', data, 'json');
  return result;
}

function ResetUserTable(){
  var datatable = $('#dynamic-table').dataTable().api();
  datatable.clear();
  datatable.draw();
}

function SaveUserGroup(userid, groupid){
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }
  token = token.data.token;
  data = {'token':token, 'userid':userid, 'groupid':groupid};
  data = JSON.stringify(data);
  url = '/api/auth/saveusergroup/';
  result = ajax(url, 'POST', data, 'json');
  return result;
}

function ResetUserSearchLabel(){
  $('#name').val('');
  $('#account').val('');
}

function GetAllRoleList(){
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }
  token = token.data.token;
  data = {'token':token};
  data = JSON.stringify(data);
  url = '/api/auth/getallrolelist/';
  result = ajax(url, 'POST', data, 'json');
  return result;
}

function GetRoleForGroup(id){
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }
  token = token.data.token;
  data = {'token':token, 'id':id};
  data = JSON.stringify(data);
  url = '/api/auth/getroleforgroup/';
  result = ajax(url, 'POST', data, 'json');
  return result;
}

function SaveGroupRoleChange(groupid,groupname,roleid){
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }
  token = token.data.token;
  data = {'token':token, 'groupid':groupid, 'groupname':groupname, 'roleid':roleid};
  data = JSON.stringify(data);
  url = '/api/auth/savegrouprolechange/';
  result = ajax(url, 'POST', data, 'json');
  // console.log(result);
  return result;
}

function FindModelsForRole(id){
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }
  token = token.data.token;
  data = {'token':token, 'roleid':id};
  data = JSON.stringify(data);
  url = '/api/auth/findmodelsforrole/';
  result = ajax(url, 'POST', data, 'json');
  // console.log(result);
  return result;
}

function GetAllModels(){
  // token = GetToken();
  // if (token == 'error') {
  //   alert('Token过期');
  //   return false;
  // }
  // token = token.data.token;
  // data = {'token':token};
  // data = JSON.stringify(data);
  // url = '/api/auth/findmodelsforrole/';
  // result = ajax(url, 'POST', data, 'json');
  // // console.log(result);
  // return result;
}

function FindOperationsInModel(id){
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }
  if (!isall) {
    isall = '0';
  }
  token = token.data.token;
  data = {'token':token, 'modelid':id,};
  data = JSON.stringify(data);
  url = '/api/auth/findoperationinmodel/';
  result = ajax(url, 'POST', data, 'json');
  return result;
}

function GetAllOperations(){
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }
  token = token.data.token;
  data = {'token':token,};
  data = JSON.stringify(data);
  url = '/api/auth/findoperationinmodel/';
  result = ajax(url, 'POST', data, 'json');
  console.log(result);
  return result;
}

function GetAllPermissionType(){
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }
  token = token.data.token;
  data = {'token':token,};
  data = JSON.stringify(data);
  url = '/api/auth/getallpermission/';
  result = ajax(url, 'POST', data, 'json');
  return result;
}

function GetAllModels(){
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }
  token = token.data.token;
  data = {'token':token,};
  data = JSON.stringify(data);
  url = '/api/auth/getallmodels/';
  result = ajax(url, 'POST', data, 'json');
  return result;
}

function UpdateOrInsert(dicList,roleid,rolename){
  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }

  token = token.data.token;
  data = {'token':token, 'modularPermissions':dicList, 'roleid':roleid, 'rolename':rolename};
  console.log(data);
  data = JSON.stringify(data);
  url = '/api/auth/updataorinsertrolemodularpermissiontype/';
  result = ajax(url, 'POST', data, 'json');
  return result;

}

//treeview 异步加载节点
//业务线选择
function BuslinesWithLevelAndPid(level, pid){

  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }

  token = token.data.token;
  data = {'token':token, 'level':level, 'pid':pid};
  data = JSON.stringify(data);
  url = '/api/busline/buslineswithlevelandpid/';
  result = ajax(url, 'POST', data, 'json');
  // console.log('busline:',result.data);
  return result
}

function AddBuslineTreeview(){

  if ($('#parentDiv li').size() > 0) {
    $('#parentDiv').slideToggle();
    return true;
  }

  var initData = BuslinesWithLevelAndPid().data;

  SetBuslineTreeview(initData, []);
}

function SetBuslineTreeview(thedata, memoryClick){

  var initData = thedata;

  //修改背景范围
  var style = $('.modal-backdrop').attr('style');
  if (style) {
    var value = style.replace(/[^0-9]/ig,"");
    value = parseInt(value) + parseInt(initData.length*41);
    style = 'height: ' + value.toString() + 'px';
    $('.modal-backdrop').attr('style', style);
  }

  var nodeid = '';
  $('#parentDiv').treeview({
    data:initData,
    onNodeSelected: function(event, node) {
      //点击选中
      selectBusline(node.id);
    },
    onNodeExpanded: function(event, node) {
      nodeid = node['nodeId'];

      var has = false;
      for (var i = 0; i < memoryClick.length; i++) {
        var m_id = memoryClick[i];
        if (m_id == nodeid) {
          has = true;
          break;
        }
      }
      if (!has) {
        memoryClick.push(nodeid);
      }

      if (node['nodes'].length <= 0) {
        var level = parseInt(node['level']) + 1;
        var pid = node['id']
        var children = BuslinesWithLevelAndPid(level, pid).data;
        ResetNodes(initData, node, children);
        SetBuslineTreeview(initData, memoryClick);

        $('#parentDiv').treeview('collapseAll',{silent: true});
        for (var i = 0; i < memoryClick.length; i++) {
          var temp = memoryClick[i];
          $('#parentDiv').treeview('expandNode', temp);
        }
        $('#parentDiv').render();
      }

      //修改背景范围
      var style = $('.modal-backdrop').attr('style');
      if (style) {
        var value = style.replace(/[^0-9]/ig,"");
        value = parseInt(value) + parseInt(node.nodes.length*41);
        style = 'height: ' + value.toString() + 'px';
        $('.modal-backdrop').attr('style', style);
      }

    },
    onNodeCollapsed: function(event, node) {

      if (node) {
        var index = memoryClick.indexOf(node['nodeid']);
        console.log(index);
        memoryClick.splice(index, 1);
      }

      //修改背景范围
      var style = $('.modal-backdrop').attr('style');
      if (style) {
        var value = style.replace(/[^0-9]/ig,"");
        value = parseInt(value) - parseInt(node.nodes.length*41);
        style = 'height: ' + value.toString() + 'px';
        $('.modal-backdrop').attr('style', style);
      }

    }
  });
}


//部门选择
function BsporgWithLevelAndPid(level, pid){

  token = GetToken();
  if (token == 'error') {
    alert('Token过期');
    return false;
  }

  token = token.data.token;
  data = {'token':token, 'level':level, 'pid':pid};
  data = JSON.stringify(data);
  url = '/api/busline/bsporgwithlevelandpid/';
  result = ajax(url, 'POST', data, 'json');
  // console.log('busline:',result.data);
  return result
}

function AddBsporgTreeview(){

  if ($('#parentDiv1 li').size() > 0) {
    $('#parentDiv1').slideToggle();
    return true;
  }

  var initData = BsporgWithLevelAndPid().data;

  SetBsporgTreeview(initData, []);
}
// memoryClick数组是用于记录那个节点被点击过。方便刷新列表后展开之前展开的节点。
function SetBsporgTreeview(thedata, memoryClick){

  var initData = thedata;

  //修改背景范围
  var style = $('.modal-backdrop').attr('style');
  if (style) {
    var value = style.replace(/[^0-9]/ig,"");
    value = parseInt(value) + parseInt(initData.length*41);
    style = 'height: ' + value.toString() + 'px';
    $('.modal-backdrop').attr('style', style);
  }

  $('#parentDiv1').treeview({
    data:initData,
    onNodeSelected: function(event, node) {
      //点击选中
      selectBsporg(node.id);
    },
    onNodeExpanded: function(event, node) {

      var nodeid = node['nodeId'];

      var has = false;
      for (var i = 0; i < memoryClick.length; i++) {
        var m_id = memoryClick[i];
        if (m_id == nodeid) {
          has = true;
          break;
        }
      }
      if (!has) {
        memoryClick.push(nodeid);
      }

      console.log("onNodeExpanded:",memoryClick);
      if (node['nodes'].length <= 0) {
        var level = parseInt(node['level']) + 1;
        var pid = node['id']
        var children = BsporgWithLevelAndPid(level, pid).data;
        ResetNodes(initData, node, children);
        SetBsporgTreeview(initData, memoryClick);

        $('#parentDiv1').treeview('collapseAll',{silent: true});
        for (var i = 0; i < memoryClick.length; i++) {
          var temp = memoryClick[i];
          $('#parentDiv1').treeview('expandNode', temp);
        }
        $('#parentDiv1').render();
      }

      //修改背景范围
      var style = $('.modal-backdrop').attr('style');
      if (style) {
        var value = style.replace(/[^0-9]/ig,"");
        value = parseInt(value) + parseInt(node.nodes.length*41);
        style = 'height: ' + value.toString() + 'px';
        $('.modal-backdrop').attr('style', style);
      }


    },
    onNodeCollapsed: function(event, node) {

      if (node) {
        var index = memoryClick.indexOf(node['nodeid']);
        console.log(index);
        memoryClick.splice(index, 1);
      }
      //修改背景范围
      var style = $('.modal-backdrop').attr('style');
      if (style) {
        var value = style.replace(/[^0-9]/ig,"");
        value = parseInt(value) - parseInt(node.nodes.length*41);
        style = 'height: ' + value.toString() + 'px';
        $('.modal-backdrop').attr('style', style);
      }

    },
  });
}

function ResetNodes(source, clickNode, childNode){
  for (var i = 0; i < source.length; i++) {
    var temp = source[i];
    if (temp['nodes']) {

      if (temp['id'] == clickNode['id']) {
        temp['nodes'] = childNode;
        return;
      }else {
        if (temp['nodes'].length > 0) {
          ResetNodes(temp['nodes'], clickNode, childNode);
        }
      }
    }
  }
}
