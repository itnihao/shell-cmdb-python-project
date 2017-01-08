var apikey = 'testid';
var script = 'api';


function ajax(ajax_url,ajax_type,ajax_data,type)//ajax get function ajax_url,ajax_type,ajax_data
{
    var ret = null;
    $.ajax({
        url:ajax_url,
        async:false,
        type:ajax_type,
        data:ajax_data,
        dataType:type,
        timeout:1000,
        beforeSend: function(request){
            // request.setRequestHeader("apikey","g9srdmhjaj0DMef");
        },
        success: function(request)
        {
            ret = request;
        },

        error:function(XMLHttpRequest,textStatus,errorThrown)
        {
            alert(XMLHttpRequest.status);
        }
        });
        return ret;
}


$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});


function GetToken(){
  data = 'apikey=' + apikey + '&script=' + script;
  url = '/api/auth/token/';
  token = ajax(url, 'GET', data, 'json');
  if (token.code == 0){
    return token;
  }else{return 'error'}
}
