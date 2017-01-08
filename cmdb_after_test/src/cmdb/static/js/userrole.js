;
$(document).ready(function(id) {
    msgtips();
    $("input[name=user]").autocomplete({
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
            $(this).val(ui.item.label);
            $(this).next().val(ui.item.value);
            return false;
        }
    });
    $("#ajxuser").click(function () {
        var roleid = $.trim($("#roleid").val());
        var userid = $.trim($("#userid").val());
        var name   = $.trim($("#user").val());
        if (name.length == 0)
        {
            msgtips("请输人名", 0);
            return false;
        }
        if (userid == 0)
        {
            msgtips("请选择人名", 0);
            return false;
        }
        $.ajax({
                'url': '/user/permission/userrole/add',
                'type': 'post',
                'dataType': 'json',
                'data': {'userid': userid,'roleid':roleid},
                success: function (res) {
                    if (res.code == 1) {
                        msgtips(res.msg, 0);
                    } else {
                        msgtips(res.msg, 1);
                        $("#edit").foundation('reveal', 'close');
                        window.location.href = window.location.href;
                    }
                }
        });
    });
    $(".close").click(function() {
        if (confirm("操作提醒\r\n确定这样做吗?")) {
            var data = $(this).attr('data');
            segs = data.split('_');
            roleid = segs[0];
            userid = segs[1];
            $.ajax({
                'url': '/user/permission/userrole/delete',
                'type': 'post',
                'dataType': 'json',
                'data': {'userid': userid, 'roleid': roleid}
            });
        }else{
            return false;
        }

    });
});

function msgtips(msg, type){
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

function adduser(id) {
    msgtips();
    $($("#edit h4").get(0)).html("添加人员");
    $($("#user")).val("");
    $($("#roleid")).val(id);
    $("#edit").foundation('reveal', 'open');
}

function removeuser(id) {
    msgtips();
    $($("#edit h4").get(0)).html("移除人员");
    $($("#user")).val("");
    $($("#roleid")).val(id);
    $("#edit").foundation('reveal', 'open');
}