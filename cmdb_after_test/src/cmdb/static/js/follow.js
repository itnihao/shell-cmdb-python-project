;
(function($){
	var elementAttr = 'data-options';
	var requstURI = '/user/actFollow';
	function Follow(){
		var self = this;
		$("["+elementAttr+"]").bind('click',evtTrigger);
		function evtTrigger(){
            var that =this;
			try{
				var data = $.parseJSON($(this).attr(elementAttr));
				data.act = data.act || 'follow';
				$.post(requstURI, data , function(response){
					var r = $.parseJSON(response);
					if(r.code===0) {
                        if(data.act == "follow"){
                            $(that).html("已关注");
                        }else if(data.act == "unfollow"){
                            $(that).html("取消成功");
                        }
					}
 				});
			}catch(e){
				alert(e);
			}

		}
	}

	$.extend({follow:Follow});

})(jQuery);


$(function(){
	jQuery.follow();
});

