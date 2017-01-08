;
$(document).ready(function () {
    var current_page = parseInt($("#put1").val())
    var all_page = parseInt($("#put2").val());
    $('#resultTable_previous').addClass('disabled');
    $('#resultTable_first').addClass('disabled');

    $(function () {
        if ($('[name="date_s"]').prop('name') == 'date_s') {
            $('[name="date_s"]').datepicker();
        }
    });
    $('#findBtn').click(function () {
        var srh = JSON.stringify(getSearch());
        $.ajax({
            'url': '/cmdb/orders/search',
            'type': 'post',
            'dataType': 'json',
            'data': {'search': srh, 'mod':'search'},
            success: function (res) {
                if (res.tickets) {
                    //chg_search(res);
                    //show_page(res.extend, res.p);
                    current_page = res.current_page;
                    all_page = res.all_page;
                    change_pagination(current_page, all_page, res);
                }

            }
        })
    });

    change_pagination = function (current_page, all_page, dic) {

        if (current_page == all_page && current_page > 1) {
            if (!$('#resultTable_next').hasClass('disabled')) {
                $('#resultTable_next').addClass('disabled')
            }
            if (!$('#resultTable_last').hasClass('disabled')) {
                $('#resultTable_last').addClass('disabled')
            }
            if ($('#resultTable_first').hasClass('disabled')) {
                $('#resultTable_first').removeClass('disabled')
            }
            if ($('#resultTable_previous').hasClass('disabled')) {
                $('#resultTable_previous').removeClass('disabled')
            }
        }
        else if (current_page == 1 && all_page != 1) {
            if (!$('#resultTable_first').hasClass('disabled')) {
                $('#resultTable_first').addClass('disabled')
            }
            if (!$('#resultTable_previous').hasClass('disabled')) {
                $('#resultTable_previous').addClass('disabled')
            }
            if ($('#resultTable_next').hasClass('disabled')) {
                $('#resultTable_next').removeClass('disabled')
            }
            if ($('#resultTable_last').hasClass('disabled')) {
                $('#resultTable_last').removeClass('disabled')
            }
        }
        else if (current_page == 1 && all_page == 1) {
            if (!$('#resultTable_first').hasClass('disabled')) {
                $('#resultTable_first').addClass('disabled')
            }
            if (!$('#resultTable_previous').hasClass('disabled')) {
                $('#resultTable_previous').addClass('disabled')
            }
            if (!$('#resultTable_next').hasClass('disabled')) {
                $('#resultTable_next').addClass('disabled')
            }
            if (!$('#resultTable_last').hasClass('disabled')) {
                $('#resultTable_last').addClass('disabled')
            }
        }
        else {
            if ($('#resultTable_first').hasClass('disabled')) {
                $('#resultTable_first').removeClass('disabled')
            }
            if ($('#resultTable_previous').hasClass('disabled')) {
                $('#resultTable_previous').removeClass('disabled')
            }
            if ($('#resultTable_next').hasClass('disabled')) {
                $('#resultTable_next').removeClass('disabled')
            }
            if ($('#resultTable_last').hasClass('disabled')) {
                $('#resultTable_last').removeClass('disabled')
            }
        }


        $('table > tbody').remove()
        for (var j = 0; j < dic.tickets.length; j++) {
            if (dic.tickets[j].level == 0) {
                str = " <font color='#337ab7;'>" + "默认";
            }
            if (dic.tickets[j].level == 1) {
                str = " <font color='#f0ad4e;'>" + "中";
            }
            if (dic.tickets[j].level == 2) {
                str = " <font color='#d9534f;'>" + "高";
            }
            if (dic.tickets[j].status == 5) {
                stats = "style='background-color: #d9534f;'>" + "驳回"
            }
            if (dic.tickets[j].status == 4) {
                stats = "style='background-color: #777;'>" + "完成"
            }
            if (dic.tickets[j].status == 3) {
                stats = "style='background-color: #337ab7;'>" + "处理中"
            }
            if (dic.tickets[j].status == 2) {
                stats = "style='background-color: #62ab00;'>" + "ops待认领"
            }
            $('#list').append("<tr id=" + j + " ><td>" + dic.tickets[j].id + "</td>"
                + "<td><a href='/cmdb/orders/detail/" + dic.tickets[j].id + "'>"  //window.location.href = '/cmdb/orders/detail'+
                + dic.tickets[j].title + "</a></td>"
                + "<td>" + dic.cat_dic[dic.tickets[j].category_id] + "</td>"
                + "<td>" + dic.user_dic[dic.tickets[j].applier_uid] + "</td>"
                + "<td>" +dic.user_dic[dic.tickets[j].approver_uid] + "</td>"
                + "<td style='font-style: italic;font-weight: bold'>" + str + "</td>"
                + "<td>" + dic.tickets[j].created + "</td>"
                + "<td>" + dic.tickets[j].updated + "</td>"
                + "<td><span class='btn-xs badge'" + stats + "</span></td>"
                + "</tr>")
        }
        $('#resultTable_info').text('分页' + current_page + '/' + all_page);
        $('#resultTable_input').val(current_page);

    };
    var chg_search = function (dic) {
        var str = "";
        var stats = ""
        $('table > tbody').remove()
        for (var j = 0; j < dic.tickets.length; j++) {
            if (dic.tickets[j].level == 0) {
                str = " <font color='green'>" + "一般";
            }
            if (dic.tickets[j].level == 1) {
                str = " <font color='blue'>" + "中級";
            }
            if (dic.tickets[j].level == 2) {
                str = " <font color='red'>" + "高級";
            }
            if (dic.tickets[j].status == 5) {
                stats = "style='background-color: #428bca;'>" + "已驳回"
            }
            if (dic.tickets[j].status == 4) {
                stats = "style='background-color: #428bca;'>" + "已完成"
            }
            if (dic.tickets[j].status == 3) {
                stats = "style='background-color: #5cb85c;'>" + "处理中"
            }
            if (dic.tickets[j].status == 2) {
                stats = "style='background-color: #f0ad4e;'>" + "已提交"
            }
            $('#list').append("<tr id=" + j + " ><td>" + dic.tickets[j].id + "</td>"
                + "<td><a href='url_for('tickets.detail'),id=" + dic.tickets[j].id + "'>"
                + dic.tickets[j].title + "</a></td>"
                + "<td>" + dic.cat_dic[dic.tickets[j].category_id] + "</td>"
                + "<td>" + dic.user_dic[dic.tickets[j].applier_uid] + "</td>"
                + "<td>" + dic.user_dic[dic.tickets[j].approver_uid] + "</td>"
                + "<td>" + str + "</td>"
                + "<td><span class='btn-xs badge'" + stats + "</span></td>"
                + "<td>" + dic.tickets[j].created + "</td>"
                + "<td>" + dic.tickets[j].updated + "</td>"
                + "</tr>")
        }
    };

    var show_page = function (extend, p) {
        $("#p1").remove()
        $("#p2").remove()
        var pre = ""
        var next = ""
        var pa = ""
        if (p.previous) {
            pre = "<li class='arrow'><a href='url_for('orders.search',p = 1)'> &laquo;</a></li>"
        }
        if (p.next) {
            next = "<li class='arrow'><a href='url_for('orders.search',p= " + p.page_num + " >&raquo;</a></li>"
        }
        $("#page").append("<div id='p1' class='col-sm-5 col-md-5 text-right'><label id='resultTable_info'style='margin-top: 20px'> 当前"
            + extend['current_page'] + "/" + extend['total'] + "条</label></div>"
        )
        $("#page").append(" <div id='p2' class='col-sm-7 col-md-7 text-right'><ul class='pagination '>" + pre)
        for (var i = 1; i <= p.pages.length; i++) {
            if (i == p.current) {
                pa = "<li class='current' ><a href='javascript:void(0);'> " + i.toString() + "</a></li> "
            }
            else {
                pa = "<li><a href=' url_for('orders.search',p = " + i.toString() + " '>" + i.toString() + "</a></li> "
            }
            $("#page").append(pa)
        }
        $("#page").append(next + "</ul></div>");
    }

    var getSearch = function () {
        search = {catname: '', creater: '', handler: '', state: '', starttime: '', endtime: ''};
        if ($.trim($('#catname').val())) {
            search.catname = $.trim($('#catname').find("option:selected").text());
        }
        search.creater = $.trim($('#creater').val());
        search.handler = $.trim($('#handler').val());
        search.state = $.trim($('#state_select').val());
        search.starttime = changeDate($.trim($('#start_time').val()));
        search.endtime = changeDate($.trim($('#end_time').val()));
        return search
    };

    function changeDate(date1) {
        spls = date1.split('/');
        if (spls.length > 1) {
            return spls[2] + '-' + spls[0] + '-' + spls[1]
        }
        return date1;
    }

    $("#resetBtn").click(function () {
        location.replace(location.href);
    });
    $(".user").autocomplete({
        source: function (request, response) {
            $.ajax({
                url: "/cmdb/orders/user/autocomplete",
                type: 'POST',
                dataType: "json",
                data: {
                    q: request.term
                },
                success: function (data) {
                    response($.map(data, function (item) {
                        return {
                            label: item.cn_name,
                            value: item.cn_name,
                            id: item.id
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
            $("#user").val(ui.item.value);
            $("#user").attr("data_id", ui.item.id);
            return false;
        }
    });

    $("#resultTable_first").click(function () {
        //var srh = JSON.stringify(getSearch());
        if (1 < current_page && current_page <= all_page) {
            current_page = 1
            $.ajax({
                'url': '/cmdb/orders/search',
                'type': 'post',
                'dataType': 'json',
                'data': {search: JSON.stringify(getSearch()), 'current_page': current_page, 'all_page': all_page,'mod':'page'},
                success: function (res) {
                    if (res.tickets) {
                            current_page = res.current_page;
                            all_page = res.all_page;
                            change_pagination(current_page, all_page, res);

                    }

                }
            })
        }
    })
    $("#resultTable_next").click(function () {
        //var srh = JSON.stringify(getSearch());
        //alert(srh);
        if (current_page < all_page) {
            current_page += 1
            $.ajax({
                'url': '/cmdb/orders/search',
                'type': 'post',
                'dataType': 'json',
                'data': {search: JSON.stringify(getSearch()), 'current_page': current_page, 'all_page': all_page,'mod':'page'},
                success: function (res) {
                    if (res.tickets) {
                            current_page = res.current_page;
                            all_page = res.all_page;
                            change_pagination(current_page, all_page, res);

                    }

                }
            })
        }
    })
    $("#resultTable_previous").click(function () {
        srh = JSON.stringify(getSearch());
        if (1 < current_page && current_page <= all_page) {
            current_page -= 1
            $.ajax({
                'url': '/cmdb/orders/search',
                'type': 'post',
                'dataType': 'json',
                'data': {search: JSON.stringify(getSearch()), 'current_page': current_page, 'all_page': all_page,'mod':'page'},
                success: function (res) {
                    if (res.tickets) {
                            current_page = res.current_page;
                            all_page = res.all_page;
                            change_pagination(current_page, all_page, res);

                    }

                }
            })
        }
    })
    $("#resultTable_last").click(function () {
        srh = JSON.stringify(getSearch());
        if (current_page < all_page) {
            current_page = all_page
            $.ajax({
                'url': '/cmdb/orders/search',
                'type': 'post',
                'dataType': 'json',
                'data': {search: JSON.stringify(getSearch()), 'current_page': current_page, 'all_page': all_page,'mod':'page'},
                success: function (res) {
                    if (res.tickets) {
                            current_page = res.current_page;
                            all_page = res.all_page;
                            change_pagination(current_page, all_page, res);
                    }

                }
            })
        }
    })
    $("#resultTable_goto").click(function () {
        srh = JSON.stringify(getSearch());
        goto_page = $('#resultTable_input').val()
        if (0 < parseInt(goto_page) && parseInt(goto_page) <= all_page && goto_page) {
            current_page = goto_page
            $.ajax({
                'url': '/cmdb/orders/search',
                'type': 'post',
                'dataType': 'json',
                'data': {search: JSON.stringify(getSearch()), 'current_page': current_page, 'all_page': all_page,'mod':'page'},
                success: function (res) {
                    if (res.tickets) {
                            current_page = res.current_page;
                            all_page = res.all_page;
                            change_pagination(current_page, all_page, res);

                    }

                }
            })
        }
    })
});