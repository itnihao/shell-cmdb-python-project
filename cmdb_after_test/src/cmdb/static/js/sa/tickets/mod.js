;
var tickets_mod_ops = {
    init:function(){
        this.editors = new Array();
        this.kindinit();
    },
    eventBind:function(){
        $(".tabs-content form .button").click(function(){
            for(var i=0;i< tickets_mod_ops.editors.length;i++){
                if(tickets_mod_ops.editors[i] != undefined){
                    tickets_mod_ops.editors[i].sync();
                }
            }
            $(".tabs-content form").submit();
        });
    },
    kindinit: function () {
        KindEditor.ready(function (K) {
           $('.task_content').each(function(idx){
                var editor =  K.create(this, {
                minHeight: 150,
                resizeType: 1,
                allowImageUpload: false,
                items: [
                    'source', '|', 'undo', 'redo', '|', 'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', 'bold', 'italic', 'underline',
                    'removeformat', '|', 'justifyleft', 'justifycenter', 'justifyright', 'insertorderedlist',
                    'insertunorderedlist', '|', 'image', 'link']
                });
                tickets_mod_ops.editors[idx] = editor;
           });

        });
    }
};
$(document).ready(function(){
    tickets_mod_ops.init();
    tickets_mod_ops.eventBind();
});
