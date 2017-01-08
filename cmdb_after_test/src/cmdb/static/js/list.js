;
var device_list_ops={
    init:function(){
        this.changeRack();
        var rack_num = this.getParams("rack");
        if (!rack_num)
        {
            rack_num = 0;
        }
        $("#rack").val(rack_num);
    },
    eventBind:function(){
        var that=this;
        $('#date').datepicker({
            changeMonth: true,
            changeYear: true,
            yearRange: 'c-30:c+10',
            dateFormat: 'yy-mm-dd'
        });
        $("#idc").change(function(){
             that.changeRack();
        });
    },
    resetRack:function(data){
         var target=$("#rack");
         target.empty();
         target.prepend("<option value='0'>请选择机柜</option>");
         var rack_html="";
         for(var idx in data){
                rack_html+="<option value='"+data[idx].id+"'>"+data[idx].name+"</option>";
         }
        target.append(rack_html);
    },
    changeRack:function(){
        var that = this;
         var selectVal=$("#idc").val();
         if(selectVal==0){
             target=$("#rack");
             target.empty();
             target.prepend("<option value='0'>请选择机柜</option>");
             return;
         }
         var idc_to_rack =  eval('(' + $("#test").val() + ')');
         for(var datacenter_id in idc_to_rack){
                if(datacenter_id == selectVal){
                     that.resetRack(idc_to_rack[datacenter_id]);
                }
         }
    },
    getParams:function(par){
        var local_url = document.location.href;
        //获取要取得的get参数位置
        var get = local_url.indexOf(par +"=");
        if(get == -1){
        return false;
        }
        //截取字符串
        var get_par = local_url.slice(par.length + get + 1);
        //判断截取后的字符串是否还有其他get参数
        var nextPar = get_par.indexOf("&");
        if(nextPar != -1){
        get_par = get_par.slice(0, nextPar);
        }
        return get_par;
    }
};
$(document).ready(function(){
    device_list_ops.init();
    device_list_ops.eventBind();
});



