;
(function($){
	var elementAttr = 'data-option';
	var requstURI = '/user/actAlarm';
	function Alarm(){
		$("["+elementAttr+"]").bind('click',evtTrigger);
		function evtTrigger(){
            var that =this;
			try{
				var data = $.parseJSON($(this).attr(elementAttr));
				data.act = data.act || 'alarm';
				$.post(requstURI, data , function(response){
					var r = $.parseJSON(response);
					if(r.code===0) {
                        if(data.act == "alarm"){
                            $(that).html("已接警");
                        }else if(data.act == "unalarm"){
                            var a =data.fid;
                            $(that).html("取消成功");
                            $(".fid_"+a).remove();
                        }
					}
 				});
			}catch(e){
                alert(e);
			}

		}
	}

	$.extend({alarm:Alarm});

})(jQuery);


$(function(){
	jQuery.alarm();
});

