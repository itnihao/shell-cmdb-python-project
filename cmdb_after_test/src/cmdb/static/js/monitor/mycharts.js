;
var mycharts_ops = {
    format_data: function(da){
        if (da.code != 0) {
            return;
        }
        var _series = [];
        var _time = [];
        for (var i in da.data.categories) {
            var time = da.data.categories[i].substr(11).substr(0, 5);
            _time.push(time);
        }
        for (var i in da.data.data) {
            _series.push({
                name: da.data.data[i].name,
                data: da.data.data[i].data
            });
        }
        return {'time':_time,'series':_series};
    },
    draw_spline: function (target, resp) {
        format_resp = mycharts_ops.format_data(resp);
        $('#' + target).highcharts({
            chart: {
                type: 'spline'
            },
            title: {
                text: resp.data.title,
                x: -20 //center
            },
            xAxis: {
                categories: format_resp.time,
                tickInterval: resp.data.step,
                tickWidth: 1,
                tickmarkPlacement: "on",
                labels: {
                    formatter: function () {
                        return this.value;
                    },
                    align: 'left'
                }
            },
            yAxis: {
                min: 0,
                title: {
                    text: ''
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
                positioner: function () {
                    var h_target = $("#"+target);
                    var left = parseInt(h_target.width())-100;
                    return { x: left, y: 0 };
                },
                crosshairs: [{"width": 1,"color": "#888888","zIndex": 5}],
                valueSuffix: resp.data.unit,
                useHTML: true,
                formatter: function () {
                    var tmpcontent = "";
                    if(target == "load"){
                        tmpcontent = '<h3 style=";fonts-size:12px;margin:0">CPU Load<br/>' +
                        this.x + "<br/>Avg:" + this.y + "%</h3>";
                    }else if(target == "iowait"){
                        tmpcontent = '<h3 style=";fonts-size:12px;margin:0">IOWAIT<br/>' +
                        this.x + "<br/>Avg:" + this.y + "%</h3>";
                    }
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
                    },
                    cursor:"pointer"
                }
            },
            credits: {
                enabled: false
            },
            series: format_resp.series
        });
        return $("#"+target).highcharts();
    },
    draw_area: function (target, resp) {
        format_resp = mycharts_ops.format_data(resp);
        $('#' + target).highcharts({
            chart: {
                type: 'areaspline'
            },
            title: {
                text: resp.data.title,
                x: -20 //center
            },
            xAxis: {
                categories: format_resp.time,
                tickInterval: resp.data.step,
                tickWidth: 1,
                tickmarkPlacement: "on",
                labels: {
                    formatter: function () {
                        return this.value;
                    },
                    align: 'left'
                }
            },
            yAxis: {
                min: 0,
                title: {
                    text: ''
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
                positioner: function () {
                    var h_target = $("#"+target);
                    var left = parseInt(h_target.width())-150;
                    return { x: left, y: 0 };
                },
                crosshairs: [{"width": 1,"color": "#888888","zIndex": 5},null],
                valueSuffix: resp.data.unit,
                shared: true
            },
            legend: {
                enabled: true,
                layout: 'horizontal',
                align: 'right',
                verticalAlign: 'top',
                floating: true,
                borderWidth: 0
            },
            plotOptions: {
                areaspline: {
                    stacking: 'normal',
                    fillOpacity: 0.85,
                    lineWidth: 2,
                    trackByArea:true,
                    marker: {
                        enabled: false
                    },
                    cursor:"pointer"
                }
            },
            //不显示Credit
            credits: {
                enabled: false
            },
            series: format_resp.series,
            colors: resp.data.colors
        });
        return $("#"+target).highcharts();
    },
    draw_ratio:function(target,da){
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
        monitor_index_ops.draw(target,_series, _time, da.step, da.time);
    }
};
