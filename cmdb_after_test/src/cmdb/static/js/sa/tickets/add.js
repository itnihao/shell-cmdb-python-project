;
var tickets_add_ops = {
    init: function () {
        this.idx = 1;
        this.editors = new Array();
        $("#add").click();
        this.actiontips();
    },
    eventBind: function () {
        var that = this;
        $("#add").click(function(){
            that.addTaskForm();
        });
        $(".tabs-content form .button").click(function(){
            for(var i=0;i< tickets_add_ops.editors.length;i++){
                if(tickets_add_ops.editors[i] != undefined){
                    tickets_add_ops.editors[i].sync();
                }
            }
            $(".tabs-content form").submit();
        });
    },
    addTaskForm: function () {
        var cats = eval('(' + $("#cats").val() + ')');
        var idx = tickets_add_ops.idx;
        for(var tmp_idx = 1 ; tmp_idx<idx;tmp_idx++){
            $("#ticket_"+tmp_idx).removeClass("active");
        }
        var task_header = '' +
            '<div class="row" style="margin: 0 0 0 0;">'+
            '<div class="large-12 columns">' +
            '<dl class="accordion" data-accordion>' +
            '<dd class="accordion-navigation">' +
            '<a href="#ticket_'+idx+'" class="tickets_bg">任务'+idx;
       var task_body = '</a>';
       if(idx>1){
            task_body = '<span class="right del" data="'+idx+'">删除</span></a>'
       }
       var task_select = '<select name="cat[]" class="large-3 columns cats"  data="'+idx+'">'+
           '<option value="0">请选择工单分类</option>';
       for(var select_idx in cats){
           task_select += '<option value="'+select_idx+'">'+cats[select_idx].name+'</option>';
       }
       task_select += '</select>';
       var task_footer =''+
            '<div id="ticket_'+idx+'" class="content active">' +
            '<div class="row">' +
            '<table style="border: none; width: 100% " class="table">' +
            '<tr>' +
            '<td class="large-1 columns">工单分类</td>' +
            '<td class="large-11 columns">' + task_select +
            '</td>' +
            '</tr>' +
            '<tr>' +
            '<td class="large-1 columns">工单描述</td>' +
            '<td class="large-11 columns">' +
            '<textarea  name="content[]" class="task_content" placeholder="请输入工单描述"></textarea>' +
            '</td>' +
            '</tr>' +
            '</table>' +
            '</div>' +
            '</div>' +
            '</dd>' +
            '</dl>' +
            '</div>'+
            '</div>'
        $(".tabs-content .tasks").append(task_header+task_body+task_footer);
        tickets_add_ops.idx++;
        tickets_add_ops.kindinit();
        tickets_add_ops.delTaskForm();
        tickets_add_ops.selectOnchange();
        $(document).foundation();
    },
    delTaskForm:function(){
        $(".accordion .del").each(function(){
            $(this).unbind('click');
        });
        $(".accordion .del").each(function(){
            $(this).click(function(e){
                if(tickets_add_ops.idx<=2){
                    alert("删除失败,只有一个任务");
                    return false;
                }
                if (e && e.preventDefault ){
                    e.preventDefault();
                    e.stopPropagation();
                }
                var idx = $.trim($(this).attr("data"));
                $($("#ticket_"+idx).parent().parent().parent().parent()).remove();
                tickets_add_ops.editors[idx-1] = undefined;
                tickets_add_ops.idx--;
            });
        });
    },
    kindinit: function () {
        KindEditor.ready(function (K) {
           $('.task_content').each(function(idx){
               if(tickets_add_ops.editors[idx] == undefined){
                    var editor =  K.create(this, {
                    minHeight: 150,
                    resizeType: 1,
                    allowImageUpload: false,
                    items: [
                        'source', '|', 'undo', 'redo', '|', 'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', 'bold', 'italic', 'underline',
                        'removeformat', '|', 'justifyleft', 'justifycenter', 'justifyright', 'insertorderedlist',
                        'insertunorderedlist', '|', 'image', 'link']
                    });
                    tickets_add_ops.editors[idx] = editor;
               }
           });

        });
    },
    selectOnchange:function(){
        $(".cats").each(function(){
            $(this).unbind('change');
        });
        $(".cats").each(function(){
            $(this).change(function(){
                var cats = eval('(' + $("#cats").val() + ')');
                var idx = $(this).attr("data");
                var select_val = $(this).val();
                tickets_add_ops.editors[idx-1].html(cats[select_val].template);
            });
        });
    },
    actiontips:function(){
        function GetRequest() {
          var url = location.search; //获取url中"?"符后的字串
           var theRequest = new Object();
           if (url.indexOf("?") != -1) {
              var str = url.substr(1);
              strs = str.split("&");
              for(var i = 0; i < strs.length; i ++) {
                 theRequest[strs[i].split("=")[0]]=(strs[i].split("=")[1]);
              }
           }
           return theRequest;
        };
        var Request = new Object();
        Request = GetRequest();
        var code = Request['code'];
        var msg = decodeURIComponent(Request['msg']);
        if(code > 0){
            common_ops.msgtips(msg,code);
            setTimeout('$("#msgtips").hide();',1000);
        }
    }
};
$(document).ready(function () {
    tickets_add_ops.eventBind();
    tickets_add_ops.init();
});
