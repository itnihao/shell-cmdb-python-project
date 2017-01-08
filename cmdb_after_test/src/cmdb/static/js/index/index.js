;
var cmdb_index_ops = {
    init: function () {

    },
    eventBind: function () {
        $(document).foundation();
        $(".tooltip-display").each(function () {
            $(this).mouseout(function () {
                $(".tooltip-display-wrap").css('visibility', 'hidden').hide();
            });
            $(this).mouseenter(function () {
                var target = $(this);
                //var top = target.offset().top + target.outerHeight() + 20;
                var top = target.offset().top + 26;
                var left = target.offset().left;
                var content = target.attr("data");
                $(".tooltip-display-wrap .content").html(content);
                $(".tooltip-display-wrap").css('visibility', 'visible').show();
                $(".tooltip-display-wrap").css({
                    'top': (top) ? top : 'auto',
                    'bottom': 'auto',
                    'left': (left) ? left - 120 : 'auto',
                    'right': 'auto'
                });
            });
        });
        try {
            $('#applying').tableScroll({
                height: 230
            });
        }
        catch (e) {

        }

        $('#approving').tableScroll({
            height: 230
        });
        this.draw_stat();
    },
    draw_stat: function () {
        var stat = $("#stat").attr("data").split("#");
        var series = new Array();
        for (var idx in stat) {
            series.push(parseInt(stat[idx]));
        }
        $('.draw_stat').highcharts({
            chart: {
                type: 'column',
                height: 256,
                width: 490
            },
            title: {
                text: ''
            },
            xAxis: {
                categories: [
                    '设备',
                    '主机',
                    'Pool'
                ],
                labels: {
                    align: 'center',
                    style: {
                        fontSize: '13px',
                        fontFamily: 'Verdana, sans-serif'
                    }
                }
            },
            yAxis: {
                min: 0,
                title: {
                    text: ''
                }
            },
            plotOptions: {
                series: {
                    cursor: 'pointer',
                    point: {
                        events: {
                            click: function () {
                                var key = this.category;
                                url = "/cmdb/host/";
                                if (key == "设备") {
                                    url = "/cmdb/device/";
                                } else if (key == "Pool") {
                                    url = "/cmdb/pool/";
                                }
                                window.location.href = url;
                            }
                        }
                    }
                }
            },
            legend: {
                enabled: false
            },
            credits: {
                enabled: false
            },
            tooltip: {
                formatter: function () {
                    var tmp = this.x + ':' + this.y;
                    if (this.x == "设备") {
                        tmp += '台';
                    } else if (this.x == "主机") {
                        tmp += '台';
                    } else if (this.x == "Pool") {
                        tmp += '个';
                    }
                    return tmp;
                }
            },
            series: [
                {
                    data: series,
                    dataLabels: {
                        enabled: true,
//                        rotation: -90,
                        color: '#FFFFFF',
                        x: 4,
                        y: 25,
                        style: {
                            fontSize: '13px',
                            fontFamily: 'Verdana, sans-serif',
                            textShadow: '0 0 3px black'
                        }
                    }
                }
            ]
        });
    }
};
var cmdb_index_zabbixMsg = {
    get_zabbix_msg: function () {
        $.ajax({
            url: 'get_zabbix_triggers',
            type: 'post',
            dataType: 'json',
            success: function (triggers) {
                if (triggers == []) {
                    $("#zabbixBox").hide();
                } else {
                    $("#zabbixBox").show();
                    $('#zabbixMsg').empty();
                    for (var i in triggers) {
                        html = "<tr><td><a href=\"cmdb/host/" + triggers[i].host_id + "\">" + triggers[i].hostname + "</a></td>\
                                <td><a href=" + triggers[i].url + ">" + triggers[i].description + "</a></td>\
                                <td>" + triggers[i].longer + "</td>\
                                <td><a href=\"cmdb/pool/detail/" + triggers[i].pool_id + "\">" + triggers[i].pool + "</a></td>\
                                <td>" + triggers[i].user + "</td></tr>";
                        $('#zabbixMsg').append(html);
                    }
                }

            }
        });
    },
    repeat: function () {
        setInterval(cmdb_index_zabbixMsg.get_zabbix_msg, 10000);
    }
};
$(document).ready(function () {
    cmdb_index_ops.init();
    cmdb_index_ops.eventBind();
    ubuntu_tips.init();
    ubuntu_tips.repeat();
    cmdb_index_zabbixMsg.get_zabbix_msg();
    cmdb_index_zabbixMsg.repeat();
});
