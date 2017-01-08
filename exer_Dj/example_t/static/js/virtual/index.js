/**
 * Created by root on 16-7-5.
 */
;
var init_ops= {

   // var Colors = Highcharts.getOptions().colors, //['#6fb3e0','#FF1F34','#FF1234','#FF4321','#6546FF'],
   
    
    // show: function () {
    //    $.getJSON("/api/vm_pool",function(result){
    //         alert(result);
    //     });
    // },

    platform: function () {
        var colors = Highcharts.getOptions().colors,//['#6fb3e0','#FF1F34','#FF1234','#FF4321','#6546FF'],
            categories = ['MSIE', 'Firefox', 'Chrome', 'Safari', 'Opera'],
            cate = ['宿主机','虚拟机'],
            //name = 'Browser brands',
            data_wuba=[
                {y:400,
                 color:colors[0]
                 },
                {y:2500,
                 color:colors[2]

                }],
            data_ganji=[
                {y:250,
                 color:colors[0]
                 },
                {y:1200,
                 color:colors[2]

                }],
            data_ajk=[
                {y:60,
                 color:colors[0]
                 },
                {y:200,
                 color:colors[2]

                }],
            data_yingcai=[
                {y:65,
                 color:colors[0]
                 },
                {y:300,
                 color:colors[2]

                }],
            data_plat=[
                {y:775,
                 color:colors[0]
                 },
                {y:4200,
                 color:colors[2]

                }],
            data = [{
                y: 55.11,
                color: colors[0],

            }, {
                y: 21.63,
                color: colors[1],

            }, {
                y: 11.94,
                color: colors[2],

            }, {
                y: 7.15,
                color: colors[3],

            }, {
                y: 2.14,
                color: colors[4],

            }];

        $('#platform').highcharts({
            chart: {
                type: 'column',
                height: 256,
                width: 490
            },
            title: {
                text: ''
            },
            subtitle: {
                text: ''
            },
            xAxis: {
                categories: categories,
                labels: {
                    align: 'center',
                    style: {
                        fontSize: '13px',
                        fontFamily: 'Verdana, sans-serif'
                    }
                }
            },
            yAxis: {
                title: {
                    text: ''
                }
            },
            legend: {
                    enabled: false
                },
            plotOptions: {
                column: {

                    dataLabels: {
                        enabled: true,
                        color: colors[0],
                        style: {
                            fontWeight: 'bold'
                        },
                        formatter: function () {
                            return this.y + '台';
                        }
                    }
                }
            },
            tooltip: {
                formatter: function () {
                    var point = this.point,
                        s = this.x + ':<b>' + this.y + '% market share</b><br/>';

                    return s;
                }
            },
            series: [{
               // name: name,
                data: data_plat

               // color: 'white'
            }],
            //exporting: {
            //    enabled: false
            //}
        });
        $('#wuba_cluster').highcharts({
            chart: {
                type: 'column',
                height: 256,
                width: 490
            },
            title: {
                text: ''
            },
            subtitle: {
                text: ''
            },
            xAxis: {
                categories: cate,
                labels: {
                    align: 'center',
                    style: {
                        fontSize: '13px',
                        fontFamily: 'Verdana, sans-serif'
                    }
                }
            },
            yAxis: {
                title: {
                    text: ''
                }
            },
            legend: {
                    enabled: false
                },
            plotOptions: {
                column: {

                    dataLabels: {
                        enabled: true,
                        color: colors[0],
                        style: {
                            fontSize: '13px',
                            fontWeight: 'bold'
                        },
                        formatter: function () {
                            return this.y + '台';
                        }
                    }
                }
            },
            tooltip: {
                formatter: function () {
                    var point = this.point,
                        s = this.x + ':<b>' + this.y + '台</b><br/>';

                    return s;
                }
            },
            series: [{
               // name: name,
                data: data_wuba

               // color: 'white'
            }],
            //exporting: {
            //    enabled: false
            //}
        });
        $('#ganji_cluster').highcharts({
            chart: {
                type: 'column',
                height: 256,
                width: 490
            },
            title: {
                text: ''
            },
            subtitle: {
                text: ''
            },
            xAxis: {
                categories: cate,
                labels: {
                    align: 'center',
                    style: {
                        fontSize: '13px',
                        fontFamily: 'Verdana, sans-serif'
                    }
                }
            },
            yAxis: {
                title: {
                    text: ''
                }
            },
            legend: {
                    enabled: false
                },
            plotOptions: {
                column: {

                    dataLabels: {
                        enabled: true,
                        color: colors[0],
                        style: {
                            fontSize: '13px',
                            fontWeight: 'bold'
                        },
                        formatter: function () {
                            return this.y + '台';
                        }
                    }
                }
            },
            tooltip: {
                formatter: function () {
                    var point = this.point,
                        s = this.x + ':<b>' + this.y + '台</b><br/>';

                    return s;
                }
            },
            series: [{
               // name: name,
                data: data_ganji
            }]
        });
        $('#ajk_cluster').highcharts({
            chart: {
                type: 'column',
                height: 256,
                width: 490
            },
            title: {
                text: ''
            },
            subtitle: {
                text: ''
            },
            xAxis: {
                categories: cate,
                labels: {
                    align: 'center',
                    style: {
                        fontSize: '13px',
                        fontFamily: 'Verdana, sans-serif'
                    }
                }
            },
            yAxis: {
                title: {
                    text: ''
                }
            },
            legend: {
                    enabled: false
                },
            plotOptions: {
                column: {

                    dataLabels: {
                        enabled: true,
                        color: colors[0],
                        style: {
                            fontSize: '13px',
                            fontWeight: 'bold'
                        },
                        formatter: function () {
                            return this.y + '台';
                        }
                    }
                }
            },
            tooltip: {
                formatter: function () {
                    var point = this.point,
                        s = this.x + ':<b>' + this.y + '台</b><br/>';

                    return s;
                }
            },
            series: [{
               // name: name,
                data: data_ajk
            }]
        });
        $('#yingcai_cluster').highcharts({
            chart: {
                type: 'column',
                height: 256,
                width: 490
            },
            title: {
                text: ''
            },
            subtitle: {
                text: ''
            },
            xAxis: {
                categories: cate,
                labels: {
                    align: 'center',
                    style: {
                        fontSize: '13px',
                        fontFamily: 'Verdana, sans-serif'
                    }
                }
            },
            yAxis: {
                title: {
                    text: ''
                }
            },
            legend: {
                    enabled: false
                },
            plotOptions: {
                column: {

                    dataLabels: {
                        enabled: true,
                        color: colors[0],
                        style: {
                            fontSize: '13px',
                            fontWeight: 'bold'
                        },
                        formatter: function () {
                            return this.y + '台';
                        }
                    }
                }
            },
            tooltip: {
                formatter: function () {
                    var point = this.point,
                        s = this.x + ':<b>' + this.y + '台</b><br/>';

                    return s;
                }
            },
            series: [{
               // name: name,
                data: data_yingcai
            }]
        })
    }
};


    // }u

init_ops.platform(); 