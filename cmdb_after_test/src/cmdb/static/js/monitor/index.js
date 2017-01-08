;
var monitor_index_ops = {
    init: function () {
        var that = this;
        this.type = $("#type").val();
        this.target_id = $("#target_id").val();
        this.counter = 0;
        this.interval = null;
        this.getPools();
        this.getRacks();
        this.act_loading_list();
        if (this.type == "follow_pool" && this.target_id) {
            $('#time_button').show();
            $(".time").each(function () {
                $(this).click(function () {
                    var _time = $(this).attr("data");
                    monitor_index_ops.draw_data("pool", that.target_id, _time);
                });
            });
            $($(".time").get(0)).click();
        }
        if (this.type == "follow_host") {
            $("#monitor-def-group").addClass("active-nav");
        }
        $("#force_refresh").click(function () {
            monitor_index_ops.act_loading_list();
        });
        if(this.type){
            setInterval(monitor_index_ops.act_loading_list, 60000);
        }
    },
    toggleFollwedHost: function (da, slide_num) {
        show_num = slide_num - 1;
        var element = $("li." + da);
        var size = element.size() - 1;
        if (element.size() > slide_num) {
            var _e = $('<li id="' + da + '"' + 'class="heading" style="text-align:right;margin-right:5px;fonts-size:14px;cursor:pointer" f="o"> + 展开</li>');
            element.filter(':eq(' + size + ')').after(_e);
            var prefix = new RegExp("open=1&" + da);
            if (!(prefix.test(location.href))) {
                element.filter(':gt(' + show_num + ')').hide();
            } else {
                $("#" + da).attr('f', 'h');
                $("#" + da).html("- 收起");
                $('.' + da + ' > a').each(function () {
                    var x = $(this).attr('href');
                    $(this).attr('href', x + '&open=1&' + da);
                });
            }
        }
    },
    slide: function (da, slide_num) {
        show_num = slide_num;
        $("#" + da).click(function () {
            if ($(this).attr('f') == 'h') {
                $(this).attr('f', 'o');
                $('.' + da + ':gt(' + show_num + ')').slideUp();
                $('.' + da + ' > a').each(function () {
                    var x = $(this).attr('href');
                    $(this).attr('href', x.replace('&open=1&' + da, ""));
                });
                $(this).html(" + 展开");
            } else {
                $('.' + da + ':gt(' + show_num + ')').slideDown();
                $('.' + da + ' > a').each(function () {
                    var x = $(this).attr('href');
                    $(this).attr('href', x + '&open=1&' + da);
                });
                $(this).attr('f', 'h');
                $(this).html("- 收起");
            }
        })
    },
    poolInfo: function (path) {
        $.ajax({
            url: '/' + path + '/pools',
            type: "get",
            dataType: 'json',
            success: function (resp) {
                if (!resp.data || !resp.data.length) {
                    return false;
                }
                $("#pools").html('');
                var __m = location.href.match(/pool_id=(\d+)/);
                var pool_id = 0;
                if (__m && __m[1] && __m[1] != 0) {
                    pool_id = __m[1];
                }
                pool_data = resp.data;
                for (var x in pool_data) {
                    var data = pool_data[x];
                    var _element = $("<li class='foll-pool'><a href='/" + path + "/?pool_id=" + data.id + "&type=follow_pool'>" + data.name + "</a></li>");
                    if (pool_id && pool_id == data.id) {
                        _element.addClass('active-nav');
                    }
                    $("#pools").append(_element);
                }
                monitor_index_ops.toggleFollwedHost("foll-pool", 3);
                monitor_index_ops.slide("foll-pool", 3);
                $("#icon-play").trigger('click');
            }
        });
    },
    getPools: function () {
        var href = window.location.href;
        if ((/monitor/).test(href)) {
            monitor_index_ops.poolInfo("monitor");
        } else if ((/logger/).test(href)) {
            monitor_index_ops.poolInfo("logger");
        }
    },
    rackInfo: function (path) {
        $.ajax({
            url: '/' + path + '/racks',
            type: "get",
            dataType: 'json',
            success: function (resp) {
                if (!resp.data || !resp.data.length) {
                    return false;
                }
                var __m = location.href.match(/rack_id=(\d+)/);
                var rack_id = 0;
                if (__m && __m[1] && __m[1] != 0) {
                    rack_id = __m[1];
                }
                $("#racks").html('');
                var pool_data = resp.data;
                for (var x in pool_data) {
                    var data = pool_data[x];
                    var _element = $("<li class='foll-rack'><a href='/" + path + "/?rack_id=" + data.id + "&type=follow_rack'>" + data.idcname + '/' + data.rackname + "</a></li>");
                    if (rack_id && rack_id == data.id) {
                        _element.addClass('active-nav');
                    }
                    $("#racks").append(_element);
                }
                monitor_index_ops.toggleFollwedHost("foll-rack", 3);
                monitor_index_ops.slide("foll-rack", 3);
                $("#icon-play").trigger('click');
            }
        });
    },
    getRacks: function () {
        var href = window.location.href;
        if ((/monitor/).test(href)) {
            monitor_index_ops.rackInfo("monitor");
        } else if ((/logger/).test(href)) {
            monitor_index_ops.rackInfo("logger");
        }
    },
    act_loading_list: function () {
        var that = this;
        var type = monitor_index_ops.type;
        var target_id = parseInt(monitor_index_ops.target_id);
        if(type){
            $.get("/monitor/act_load_monitor?type=" + type + "&id=" + target_id, function (response) {
                if (response.trim() == '') {
                    response = '<tr> <td colspan="6" style="color:Red">您尚未关注任何主机,您可以<a href="/cmdb/host/">进入主机列表</a>选择关注!</td></tr>';
                    $("#table-content").html(response);
                    return false;
                }
                $(".tooltip").remove();
                $("#table-content").hide().html(response).fadeIn();
                monitor_index_ops.get_ratio();
                sortable('.table');
                monitor_index_ops.tooltips();
            });
        }
    },
    tooltips: function () {
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
                    'left': (left) ? left : 'auto',
                    'right': 'auto'
                });
            });
        });
    },
    draw_data: function (type, id, time) {
        var self = this;
        var requrl = "/monitor/get_load_data" + "?type=" + type + "&id=" + id + "&time=" + time;
        $.get(requrl, function (da) {
            if (da.code != 0) {
                alert('查询数据出错!');
                return;
            }
            if (da.data.length <= 0) {
                alert('没有查询到数据!');
                return;
            }
            var _series = [];
            var _time = [];
            for (var i in da.categories) {
                if (da.time == 1) {
                    var time = da.categories[i].substr(11).substr(0, 5);
                } else {
                    var time = da.categories[i].substr(0, 10);
                }
                _time.push(time);
            }
            for (var i in da.data) {
                _series.push({
                    name: da.data[i].name,
                    data: da.data[i].data
                });
            }
            monitor_index_ops.draw("canvas",_series, _time, da.step, da.time);
        }, 'json');
    },
    draw: function (target,data, _time, step, type) {
        $('#'+target).highcharts({
            chart: {
                type: 'spline'
            },
            title: {
                text: data[0].name,
                x: -20 //center
            },
            xAxis: {
                categories: _time,
                tickInterval: step,
                tickWidth: 1,
                tickmarkPlacement: "on",
                labels: {
                    formatter: function () {
                        if (type == 1) {
                            return this.value;
                        } else {
                            return this.value.substr(5);
                        }
                    },
                    align: 'left'
                }
            },
            yAxis: {
                min: 0,
                title: {
                    text: '满载率 (%)'
                },
                plotLines: [
                    {
                        value: 0,
                        width: 1,
                        color: '#808080'
                    }
                ]
            },
            tooltip: {
                valueSuffix: '%',
                useHTML: true,
                //shared: true,
                formatter: function () {
                    var tmpcontent = '<h3 style=";fonts-size:16px;margin:0">' +
                        this.x + "<br/>满载率:" + this.y + "%</h3>";
                    return tmpcontent
                }
            },
            legend: {
                enabled: false
            },
            plotOptions: {
                spline: {
                    lineWidth: 2,
                    marker: {
                        enabled: false
                    }
                }
            },
            //不显示Credit
            credits: {
                enabled: false
            },
            series: data
        });
        //第一次不跳转
        if (monitor_index_ops.counter > 0) {
            monitor_index_ops.myscroll(target+"2", 100);
        }
        monitor_index_ops.counter++;
    },
    myscroll: function (id, extra) {
        var t = $("#" + id).offset().top;
        $(window).scrollTop(t - extra);
    },
    get_ratio: function(){
        var hostids  = new Array();
        $(".hostload").each(function(){
            var classname = $(this).attr("class");
            var host_id = classname.replace("hostload hostload_","");
            host_id = parseInt(host_id);
            if(host_id>0){
                hostids.push(host_id);
            }
        });
        if(hostids.length<=0){
            return false;
        }
        $.ajax({
            url: "/cmdb/host/ratio",
            type: 'POST',
            data:{'ids':hostids.join(",")},
            dataType: "json",
            success: function (res) {
                if(!res){
                    return;
                }
                ratios =res.data[0];
                for(var key in ratios){
                    classname = key;
                    content ='<a data-type="numeric" data-value="'+ratios[key][0]+'" href="" class="tooltip-display" data="采集时间:'+ratios[key][1]+'">'+ratios[key][0]+'%</a>'
                    $("."+classname).html(content);
                }
            }
        });
    }
};

