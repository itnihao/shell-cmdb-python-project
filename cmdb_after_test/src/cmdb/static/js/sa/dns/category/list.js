;
var dns_cat_list_ops = {
    init: function () {
        this.eventBind();
        this.autofix();
    },
    eventBind: function () {
        var that = this;
        $("#add").click(function () {
            msgtips("", 0);
            $("#edit").html("添加ZONE");
            $("#zone").val("");
            $("#display").val("");
            $("#type").val("-1");
            $("#content").val("");
            $("#dns_cat").foundation('reveal', 'open');
        });
        $("#doadd").click(function () {
            var zone = $("#zone").val();
            var type = $("#type").val();
            var content = $("#content").val();
            var display = $("#display").val();
            var manage_uid = parseInt($.trim($("#manage_uid").val()));
            var zone_cat_id =parseInt($("#zone_cat_id").val())
            if (zone.length <= 0) {
                msgtips("请输入zone名称", 0);
                return false;
            } else {
                msgtips("");
            }
            if (!(/^([a-z0-9]+\.)+[a-z0-9]+$/).test(zone)) {
                msgtips("请检查域名是否正确", 0);
                return false;
            } else {
                msgtips("");
            }
            if (type == "-1") {
                msgtips("请选择使用范围", 0);
                return false;
            } else {
                msgtips("");
            }
            if (manage_uid < 1) {
                msgtips('请输入域名的审批人', 0);
                $("#manage_cname").focus();
                return false;
            }
            if (zone_cat_id && /^[1-9]\d*$/.test(zone_cat_id)) {
                $.ajax({
                    'url': '/sa/dns/category/modify/' + zone_cat_id,
                    'type': 'post',
                    'dataType': 'json',
                    'data': {'zone': zone, 'display': display, 'type': type, 'content': content, 'approve_uid': manage_uid},
                    success: function (res) {
                        if (res.code == 1) {
                            msgtips(res.msg, 0);
                        } else {
                            msgtips(res.msg, 1);
                            $("#dns_cat").foundation('reveal', 'close');
                            window.location.href = window.location.href;
                        }
                    }
                });
            }
            else{
                $.ajax({
                'url': '/sa/dns/category/add',
                'type': 'post',
                'dataType': 'json',
                'data': {'zone': zone, 'display': display, 'type': type, 'content': content, 'approve_uid': manage_uid},
                    success: function (res) {
                        if (res.code == 1) {
                            msgtips(res.msg, 0);
                        } else {
                            msgtips(res.msg, 1);
                            $("#dns_cat").foundation('reveal', 'close');
                            window.location.href = window.location.href;
                        }
                    }
                });
            }

        });

        $(".del").each(function() {
            $(this).click(function () {
                delFqdn($(this).attr("data"));
            });
        });
        function delFqdn(id) {
           if(confirm("操作提示:\r\n确定删除此域名吗？")){
           if(!/^[1-9]\d*$/.test(id)){
               return false;
           }
           $.ajax({
                url: "/sa/dns/category/delete/"+id,
                type: 'POST',
                dataType: "json",
                success: function (res) {
                    if (res.code == 1) {
                        alert(res.msg);
                        return;
                    }
                    window.location.href = window.location.href;
                }
           })
           }
        }

        $(".mod").each(function () {
            $(this).click(function () {
                msgtips("", 0);
                $("#edit").html("修改ZONE");
                modifydns($(this).attr("data"));
            });
        });
        function modifydns(id) {
            $.ajax({
                'url': '/sa/dns/category/get/' + id,
                'dataType': 'json',
                success: function (res) {
                    if (res) {
                        $("#zone").val(res.zone);
                        $("#display").val(res.display);
                        $("#type").val(res.type);
                        $("#content").val(res.content);
                        $("#manage_uid").val(res.approve_uid);
                        $("#manage_cname").val(res.approval);
                        $("#zone_cat_id").val(res.id);
                        $("#dns_cat").foundation('reveal', 'open');
                    }
                }
            });
        }

        function msgtips(msg, type) {
            if (msg) {
                if (type == 0) {
                    $("#msgtips").removeClass("success");
                    $("#msgtips").addClass("alert");
                } else if (type == 1) {
                    $("#msgtips").removeClass("alert");
                    $("#msgtips").addClass("success");
                }
                $("#msgtips").html(msg);
                $("#msgtips").show();
            } else {
                $("#msgtips").hide();
            }
        }
    },
    autofix: function () {
        options = {
            source: function (request, response) {
                $.ajax({
                    url: "/user/search",
                    type: 'POST',
                    dataType: "json",
                    data: {
                        maxRows: 12,
                        keyword: request.term
                    },
                    success: function (data) {
                        response($.map(data, function (item) {
                            return {
                                label: item[1],
                                value: item[0]
                            }
                        }));
                    }
                });
            },
            minChars: 1,
            max: 5,
            scroll: true,
            autoFill: true,
            mustMatch: true,
            matchContains: false,
            scrollHeight: 50,
            select: function (event, ui) {
                $("#manage_cname").val(ui.item.label);
                $("#manage_uid").val(ui.item.value);
                return false;
            }
        };
        //添加autocomplete
        $("#manage_cname").autocomplete(options);
    }
}

$(document).ready(function () {
    dns_cat_list_ops.init();
});
