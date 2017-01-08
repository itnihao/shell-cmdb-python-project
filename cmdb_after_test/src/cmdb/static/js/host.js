;
$(document).ready(function () {
    if($(".host_del_btn")) {
        $(".host_del_btn").click(function () {
            var flag = confirm("警告\r\n删除主机不可恢复!!请慎用!!");
            if (!flag) {
                return;
            }
            var id = parseInt($(this).attr('data'));
            if (id <= 0) {
                return false;
            }
            $.ajax({
                'url': '/cmdb/host/delete/' + id,
                'type': 'post',
                'dataType': 'json',
                success: function (res) {
                    window.location.href = window.location.href;
                }
            });
        });
    }
    $("#searchBtn").click(function () {
        if ($(this).parent().parent().find("input[name=q]").val().length > 0) {
            $("#searchForm").submit()
        }
    });

    $("#addEntityDeviceBtn").click(function () {
        var c_id = $("#c_id").val();
        var c_label = $("#c_label").val();
        if (c_id > 0) {
            $("#remote_ip").val(c_label);
            $("#device_id").val(c_id);
        }
        $("#add-entity-form").foundation('reveal', 'open');
        bind();
        submit.bindevents();
        $.ajax({
            url: "/cmdb/device/frame_add_services",
            type: 'GET',
            dataType: "json",
            success: function (data) {
                $("#device_list").empty();
                for (var i in data) {
                    $("#device_list").append("<option>" + data[i] + "</option>");
                }
            }
        });

    });

    $("#addEntityHostBtn").click(function () {
        var d_id = $("#d_id").val();
        var d_label = $("#d_label").val();
        $("#add-entity-form").find("form").html(
                '<h5>添加新的主机</h5>' +
                '<hr/>' +
                '<div class="tips"></div>' +
                '<label>选择主机类型:</label>' +
                '<input type="hidden" name="is_virtual" value="0">' +
                '<input type="hidden" name="host_id" value="0">' +
                '<input type="radio" name="host_type" value="1" id="app" checked="checked"><label for="app">APP</label>' +
                '<input type="radio" name="host_type" value="2" id="apc"><label for="apc">APC</label>' +
                '<input type="radio" name="host_type" value="3" id="db"><label for="db">DB</label>' +
                '<input type="radio" name="host_type" value="4" id="db"><label for="hadoop">HADOOP</label>' +
                '<input type="text" name="hostname" placeholder="主机名字(自动提示为建议主机名字)"/>' +
                '<input type="text" name="primary_ip" id="primary_ip" placeholder="主机(主要)IP"/>' +
                '<input type="hidden" name="primary_ip_id" id="primary_ip_id" value="0"/>' +
                '<input type="text" name="item" id="remote_ip" placeholder="远程控制卡IP或资产编号"/>' +
                '<input type="hidden" name="device_id" id="device_id"/>' +
                '<input type="hidden" name="type" id="type" value="host">' +
                '<textarea name="note" placeholder="备注"></textarea>' +
                '<a href="#" class="net-add-btn">+添加网卡</a>' +
                '<button type="submit" class="button tiny right" id="real">确定</button>'
        );
        if (d_id > 0) {
            $("#remote_ip").val(d_label);
            $("#device_id").val(d_id);
            $("#type").val("device");
        }
        $("#add-entity-form").foundation('reveal', 'open');
        bind();
        submit.bindevents();
    });

    $("#addVirtualHostBtn").click(function () {
        $("#add-virtual-form").find("form").html(
                '<h5>添加虚拟主机</h5>' +
                '<hr/>' +
                '<div class="tips"></div>' +
                '<input type="hidden" name="is_virtual" value="1">' +
                '<input type="hidden" name="host_id" value="0">' +
                '<input type="text" name="hostname" placeholder="主机名字(自动提示为建议主机名字)"/>' +
                '<input type="text" name="primary_ip" placeholder="主机(主要)IP"/>' +
                '<input type="hidden" name="primary_ip_id" id="primary_ip_id" value="0"/>' +
                '<input type="text" name="item" id="entity_host_name" placeholder="宿主机名称"/>' +
                '<input type="hidden" name="entity_host_id" id="entity_host_id">' +
                '<textarea name="note" placeholder="备注"></textarea>' +
                '<a href="#" class="net-add-btn">+添加网卡</a>' +
                '<button type="submit" class="button tiny right" id="vm">确定</button>'
        );
        $("#add-virtual-form").foundation('reveal', 'open');
        bind();
        submit.bindevents();
    });


    $("[name=host_modify]").each(function () {
        $(this).click(function () {
            modifyHost($(this).attr("host_id"));
        });
    });

    function modifyHost(id) {
        $.ajax({
            'url': '/cmdb/host/get/' + id,
            'dataType': 'json',
            success: function (res) {
                if (res && res.is_virtual == 0) {
                    $("#modify-entity-form").find("form").html(
                            '<h5>修改主机信息</h5>' +
                            '<hr/>' +
                            '<div class="tips"></div>' +
                            '<label>选择主机类型:</label>' +
                            '<input type="hidden" name="is_virtual" value="0">' +
                            '<input type="hidden" name="host_id" value="' + res.id + '">' +
                            '<input type="radio" name="host_type" value="1" id="app" checked="checked"><label for="app">APP</label>' +
                            '<input type="radio" name="host_type" value="2" id="apc"><label for="apc">APC</label>' +
                            '<input type="radio" name="host_type" value="3" id="db"><label for="db">DB</label>' +
                            '<input type="radio" name="host_type" value="4" id="db"><label for="hadoop">HADOOP</label>' +
                            '<div class="row"><div style="float:left"><span style="height=33px;line-height:33px;vertical-align:middle" class="input-group-label" >主机名字</span></div>' +
                            '<div style="float:left"><input type="text" style="float:left;display:inline;width:300px;margin-left:10px" name="hostname" placeholder="主机名字(自动提示为建议主机名字)" value="' + res.hostname + '" /></div></div>' +

                            '<div class="row"><div style="float:left"><span style="height=33px;line-height:33px;vertical-align:middle;margin-left:20px" class="input-group-label" >IP</span></div>' +
                            '<div style="float:left"><input type="text" style="float:left;display:inline;width:300px;margin-left:38px" name="primary_ip" id="primary_ip" placeholder="主机(主要)IP" value="' + res.primary_ip + '" /></div></div>' +

                            '<input type="hidden" name="primary_ip_id" id="primary_ip_id" value="' + res.primary_ip_id + '" />' +

                            '<div class="row"><div style="float:left"><span style="height=33px;line-height:33px;vertical-align:middle" class="input-group-label" >资产编号</span></div>' +
                            '<div style="float:left"><input style="float:left;display:inline;width:300px;margin-left:10px" type="text" name="item" id="remote_ip" placeholder="远程控制卡IP或资产编号" value="' + res.remote_ip + '" /></div></div>' +

                            '<div class="row"><div style="float:left"><span style="height=33px;line-height:33px;vertical-align:middle" class="input-group-label" >主机备注</span></div>' +
                            '<div style="float:left"><textarea style="float:left;display:inline;width:300px;margin-left:10px" name="note" placeholder="备注">' + res.note + '</textarea></div></div>' +

                            '<input type="hidden" name="device_id" id="device_id" value="' + res.device_id + '" />' +
                            '<a href="#" class="net-add-btn">+添加网卡</a>' +
                            '<button type="submit" class="button tiny right" id="real">确定</button>'
                    );
                    $("#modify-entity-form").find("input[type=radio][value='" + res.type + "']").prop("checked", true);
                    if (res.net_ip) {
                        $.each(res.net_ip, function (index, value) {
                            var option = '';
                            for (var i = 0; i < 8; i++) {
                                if (value.net_name_id == i) {
                                    option = option + '<option value="' + i + '" selected>eth' + i + '</option>';
                                } else {
                                    option = option + '<option value="' + i + '" >eth' + i + '</option>';
                                }
                            }
                            var row = $('<div class="row columns">' +
                                '<div class="small-2 columns">' +
                                '<select name="net_name_id[]">' + option + '</select>' +
                                '</div>' +
                                '<div class="small-8 columns">' +
                                '<input type="text" name="net_ip" id="entity_host_name" value="' + value.ip + '">' +
                                '<input type="hidden" name="net_ip_id[]" id="net_ip_id" value="' + value.ip_address_id + '">' +
                                '</div>' +
                                '<div class="small-2 columns">' +
                                '<a href="#" class="delete-row-btn" >&nbsp;&nbsp;删除</a>' +
                                '</div>' +
                                '</div>');
                            row.find('a.delete-row-btn').click(function () {
                                $(this).parent().parent().remove();
                            });
                            row.insertBefore($(".net-add-btn"));
                        });
                    }

                    bind();
                    $("#modify-entity-form").foundation('reveal', 'open');

                } else if (res && res.is_virtual == 1) {
                    $("#modify-virtual-form").find("form").html(
                            '<h5>修改主机信息</h5>' +
                            '<hr/>' +
                            '<div class="tips"></div>' +
                            '<input type="hidden" name="is_virtual" value="1">' +
                            '<input type="hidden" name="host_id" value="' + res.id + '">' +
                            '<div class="row"><div style="float:left"><span style="height=33px;line-height:33px;vertical-align:middle" class="input-group-label" >主机名字</span></div>' +
                            '<div style="float:left"><input type="text" style="float:left;display:inline;width:300px;margin-left:10px" name="hostname" placeholder="主机名字(自动提示为建议主机名字)" value="' + res.hostname + '" /></div></div>' +

                            '<div class="row"><div style="float:left"><span style="height=33px;line-height:33px;vertical-align:middle;margin-left:20px" class="input-group-label" >IP</span></div>' +
                            '<div style="float:left"><input type="text" style="float:left;display:inline;width:300px;margin-left:38px" name="primary_ip" id="primary_ip" placeholder="主机(主要)IP" value="' + res.primary_ip + '" /></div></div>' +

                            '<input type="hidden" name="primary_ip_id" id="primary_ip_id" value="' + res.primary_ip_id + '" />' +

                            '<div class="row"><div style="float:left"><span style="height=33px;line-height:33px;vertical-align:middle" class="input-group-label" >宿主机名</span></div>' +
                            '<div style="float:left"><input type="text" style="float:left;display:inline;width:300px;margin-left:10px" name="item" id="entity_host_name" placeholder="宿主机名称" value="' + res.entity_host_name + '" /></div></div>' +
                            '<input type="hidden" name="entity_host_id" id="entity_host_id" value="' + res.entity_host_id + '" />' +
                            '<div class="row"><div style="float:left"><span style="height=33px;line-height:33px;vertical-align:middle" class="input-group-label" >主机备注</span></div>' +
                            '<div style="float:left"><textarea style="float:left;display:inline;width:300px;margin-left:10px" name="note" placeholder="备注">' + res.note + '</textarea></div></div>' +
                            '<a href="#" class="net-add-btn">+添加网卡</a>' +
                            '<button type="submit" class="button tiny right" id="vm">确定</button>'
                    );
                    $("#modify-virtual-form").find("input[type=radio][value='" + res.type + "']").prop("checked", true);
                    if (res.net_ip) {
                        $.each(res.net_ip, function (index, value) {
                            var option = '';
                            for (var i = 0; i < 8; i++) {
                                if (value.net_name_id == i) {
                                    option = option + '<option value="' + i + '" selected>eth' + i + '</option>';
                                } else {
                                    option = option + '<option value="' + i + '" >' + i + '</option>';
                                }
                            }
                            var row = $('<div class="row columns">' +
                                '<div class="small-2 columns">' +
                                '<select name="net_name_id[]">' + option + '</select>' +
                                '</div>' +
                                '<div class="small-8 columns">' +
                                '<input type="text" name="net_ip" id="entity_host_name" value="' + value.ip + '">' +
                                '<input type="hidden" name="net_ip_id[]" id="net_ip_id" value="' + value.ip_address_id + '">' +
                                '</div>' +
                                '<div class="small-2 columns">' +
                                '<a href="#" class="delete-row-btn" >&nbsp;&nbsp;删除</a>' +
                                '</div>' +
                                '</div>');
                            row.find('a.delete-row-btn').click(function () {
                                $(this).parent().parent().remove();
                            });
                            row.insertBefore($(".net-add-btn"));
                        });
                    }
                    bind();
                    $("#modify-virtual-form").foundation('reveal', 'open');

                }
                $("input[name=net_ip]").autocomplete({
                    source: function (request, response) {
                        $.ajax({
                            url: "/cmdb/host/hostip/autocomplete",
                            type: 'POST',
                            dataType: "json",
                            data: {
                                q: request.term
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
                        $(this).next().val(ui.item.value)
                        return false;
                    }
                });
                submit.bindevents();

            }
        });
    }

    var bind = function () {
        $("input[name=primary_ip]").autocomplete({
            source: function (request, response) {
                $.ajax({
                    url: "/cmdb/host/hostip/autocomplete",
                    type: 'POST',
                    dataType: "json",
                    data: {
                        q: request.term
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
                $("input[name=primary_ip_id]").val(ui.item.value);
                return false;
            }
        });

        $("input[name=hostname]").autocomplete({
            source: function (request, response) {
                $.ajax({
                    url: "/cmdb/host/hostname/autocomplete",
                    type: 'POST',
                    dataType: "json",
                    data: {
                        q: request.term
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
                return false;
            }
        });

        $("#remote_ip").autocomplete({
            source: function (request, response) {
                $.ajax({
                    url: "/cmdb/host/device/autocomplete",
                    type: 'POST',
                    dataType: "json",
                    data: {
                        q: request.term
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
                $("#remote_ip").val(ui.item.label);
                $("#device_id").val(ui.item.value);
                return false;
            }
        });

        $("#entity_host_name").autocomplete({
            source: function (request, response) {
                $.ajax({
                    url: "/cmdb/host/entityname/autocomplete",
                    type: 'POST',
                    dataType: "json",
                    data: {
                        q: request.term
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
                $("#entity_host_name").val(ui.item.label);
                $("#entity_host_id").val(ui.item.value);
                return false;
            }
        });

        function delete_row(e) {
            e.preventDefault();
            $(this).parents('.row').remove();
        }

        $('.delete-row-btn').click(delete_row);
        $('.net-add-btn').click(function (e) {
            e.preventDefault();
            var row = $('<div class="row columns">' +
                '<div class="small-2 columns">' +
                '<select name="net_name_id[]">' +
                '<option value="0">eth0</option>' +
                '<option value="1">eth1</option>' +
                '<option value="2">eth2</option>' +
                '<option value="3">eth3</option>' +
                '<option value="4">eth4</option>' +
                '<option value="5">eth5</option>' +
                '<option value="6">eth6</option>' +
                '<option value="7">eth7</option>' +
                '</select>' +
                '</div>' +
                '<div class="small-8 columns">' +
                '<input type="text" name="net_ip" id="entity_host_name" placeholder="ip地址"/>' +
                '<input type="hidden" name="net_ip_id[]" id="net_ip_id" value="0">' +
                '</div>' +
                '<div class="small-2 columns">' +
                '<a href="#" class="delete-row-btn" >&nbsp;&nbsp;删除</a>' +
                '</div>' +
                '</div>');

            row.find('a.delete-row-btn').click(delete_row);
            row.insertBefore($(this));
            $("input[name=net_ip]").autocomplete({
                source: function (request, response) {
                    $.ajax({
                        url: "/cmdb/host/hostip/autocomplete",
                        type: 'POST',
                        dataType: "json",
                        data: {
                            q: request.term
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
                    $(this).next().val(ui.item.value)
                    return false;
                }
            });

        });

    };
    var submit = {
        bindevents: function () {
            $("#real").each(function () {
                $(this).click(function () {
                    var hostname = ($(this).parent().find("input[name=hostname]").val());
                    var primary_ip = $.trim($(this).parent().find("input[name=primary_ip]").val());
                    var remote_ip = $.trim($(this).parent().find("input[name=primary_ip]").val());
                    var primary_ip_id = $.trim($("#primary_ip_id").val());
                    var device_id = $.trim($("#device_id").val());
                    if (hostname.length <= 0) {
                        msgtips("请输入主机名称");
                        return false;
                    }
                    if (primary_ip.length <= 0) {
                        msgtips("请输入IP地址");
                        return false;
                    }
                    if (remote_ip.length <= 0) {
                        msgtips("请输入远控卡IP");
                        return false;
                    }
                    var re = /^([0-9]{1,3}\.{1}){3}[0-9]{1,3}$/;
                    if (!re.test(primary_ip)) {
                        msgtips("IP不合法");
                        return false;
                    }
                    if (primary_ip_id == 0) {
                        msgtips("请输入IP地址");
                        return false;
                    }
                    if (device_id == 0) {
                        msgtips("请输入远控卡IP");
                        return false;
                    }
                    $(this).parent().submit();
                    return true;
                })
            });
            $("#vm").each(function () {
                $(this).click(function () {
                    var hostname = ($(this).parent().find("input[name=hostname]").val());
                    var primary_ip_id = $.trim($("#primary_ip_id").val());
                    var primary_ip = $.trim($(this).parent().find("input[name=primary_ip]").val());
                    var entity_host_id = $.trim($("#entity_host_id").val());

                    if (hostname.length <= 0) {
                        msgtips("请输入主机名称");
                        return false;
                    }
                    if (primary_ip.length <= 0) {
                        msgtips("请输入IP地址");
                        return false;
                    }
                    if (primary_ip_id == 0) {
                        msgtips("请输入IP地址");
                        return false;
                    }
                    if (entity_host_id <= 0) {
                        msgtips("请输入宿主机名字");
                        return false;
                    }
                    var re = /^([0-9]{1,3}\.{1}){3}[0-9]{1,3}$/;
                    if (!re.test(primary_ip)) {
                        msgtips("IP不合法");
                        return false;
                    }
                    $(this).parent().submit();
                    return true;
                })
            });
        }
    };

    $("#list1").click(function () {
        var url = $(this).attr("data");
        window.location.href = url;
    });
    $("#list2").click(function () {
        var url = $(this).attr("data");
        window.location.href = url;
    });

    $(".card_remove").click(function () {
        $(".remote_card_details").slideToggle();
    });

    $(".remote_card").click(function () {
        $(".remote_card_details").slideToggle();
        $('#copyuser').zclip({
            path: '/static/plugins/zclip/ZeroClipboard.swf',
            copy: function () {
                var value = $('#remotecard_user').val();
                if(value != ""){
                    return value;
                }
            },
            afterCopy: function () {//复制成功
//                $('#copyuser').val('复制成功');
                if($('#copyOK').is(':hidden')) {
                    $('#copyOK').show();
                    setTimeout(function() {
                        $('#copyOK').hide();
                    },2000)
                }
            }
        });

        $('#copypass').zclip({
            path: '/static/plugins/zclip/ZeroClipboard.swf',
            copy: function () {
                var value = $('#remotecard_pass').val();
                if(value != ""){
                    return value;
                }
            },
            afterCopy: function () {//复制成功
//                $('#copypass').val('复制成功');
                if($('#copyOK').is(':hidden')) {
                    $('#copyOK').show();
                    setTimeout(function() {
                        $('#copyOK').hide();
                    },2000)
                }
            }
        });
    });

    function msgtips(msg) {
        if (msg) {
            $(".tips").html('<div data-alert class="alert-box alert">' + msg + '</div>').show()
        } else {
            $(".tips").html('').hide();
        }
    }

});