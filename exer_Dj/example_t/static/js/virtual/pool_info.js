/**
 * Created by xuepingning on 2016/9/7.
 */

Vue.config.delimiters = ["[[", "]]"];
Vue.config.unsafeDelimiters = ['[[[', ']]]'];

var vue = new Vue({

    el: "#department_pool_info",

    data: {
        test: '123123123123',
        select_department: [],  //选中的部门
        departments: ['新房', '二手房'],          //部门列表
        pool_info: [
            {
                depart: '新房',
                name: 'user-mobile-new',
                monitor: {
                    cpu: 5,
                    network: 900,
                    QPS: 5
                },
                volume: 20,
                max: 50,
                comp: 'user-web'
            }, {
                depart: '二手房',
                name: 'user-mobile-new',
                monitor: {
                    cpu: 10,
                    network: 900,
                    QPS: 12
                },
                volume: 30,
                max: 40,
                comp: 'user-job'
            }

        ],

        methods: {},
    }

});
// $('#date_picker').daterangepicker();

Highcharts.setOptions({
    global: {
        timezoneOffset: -8 * 60
    }
});

var data= {
  "squid": [
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.93.90",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": 0.0
        },
        {
          "timestamp": 1473235500,
          "value": 0.0
        },
        {
          "timestamp": 1473235560,
          "value": 0.0
        },
        {
          "timestamp": 1473235620,
          "value": 0.0
        },
        {
          "timestamp": 1473235680,
          "value": 12288.0
        },
        {
          "timestamp": 1473235740,
          "value": 0.0
        },
        {
          "timestamp": 1473235800,
          "value": 0.0
        },
        {
          "timestamp": 1473235860,
          "value": 0.0
        },
        {
          "timestamp": 1473235920,
          "value": 0.0
        },
        {
          "timestamp": 1473235980,
          "value": 0.0
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": 0.0
        },
        {
          "timestamp": 1473236460,
          "value": 0.0
        },
        {
          "timestamp": 1473236520,
          "value": 0.0
        },
        {
          "timestamp": 1473236580,
          "value": 0.0
        },
        {
          "timestamp": 1473236640,
          "value": 0.0
        },
        {
          "timestamp": 1473236700,
          "value": 0.0
        },
        {
          "timestamp": 1473236760,
          "value": 4096.0
        },
        {
          "timestamp": 1473236820,
          "value": 0.0
        },
        {
          "timestamp": 1473236880,
          "value": 0.0
        },
        {
          "timestamp": 1473236940,
          "value": 0.0
        },
        {
          "timestamp": 1473237000,
          "value": 0.0
        },
        {
          "timestamp": 1473237060,
          "value": 0.0
        },
        {
          "timestamp": 1473237120,
          "value": 0.0
        },
        {
          "timestamp": 1473237180,
          "value": 0.0
        },
        {
          "timestamp": 1473237240,
          "value": 0.0
        },
        {
          "timestamp": 1473237300,
          "value": 0.0
        },
        {
          "timestamp": 1473237360,
          "value": 0.0
        },
        {
          "timestamp": 1473237420,
          "value": 0.0
        },
        {
          "timestamp": 1473237480,
          "value": 0.0
        },
        {
          "timestamp": 1473237540,
          "value": 0.0
        },
        {
          "timestamp": 1473237600,
          "value": 0.0
        },
        {
          "timestamp": 1473237660,
          "value": 0.0
        },
        {
          "timestamp": 1473237720,
          "value": 0.0
        },
        {
          "timestamp": 1473237780,
          "value": 0.0
        },
        {
          "timestamp": 1473237840,
          "value": 4096.0
        },
        {
          "timestamp": 1473237900,
          "value": 0.0
        },
        {
          "timestamp": 1473237960,
          "value": 0.0
        },
        {
          "timestamp": 1473238020,
          "value": 0.0
        },
        {
          "timestamp": 1473238080,
          "value": 0.0
        },
        {
          "timestamp": 1473238140,
          "value": 0.0
        },
        {
          "timestamp": 1473238200,
          "value": 0.0
        },
        {
          "timestamp": 1473238260,
          "value": 0.0
        },
        {
          "timestamp": 1473238320,
          "value": 0.0
        },
        {
          "timestamp": 1473238380,
          "value": 16384.0
        },
        {
          "timestamp": 1473238440,
          "value": null
        },
        {
          "timestamp": 1473238500,
          "value": null
        },
        {
          "timestamp": 1473238560,
          "value": null
        },
        {
          "timestamp": 1473238620,
          "value": null
        },
        {
          "timestamp": 1473238680,
          "value": null
        },
        {
          "timestamp": 1473238740,
          "value": null
        },
        {
          "timestamp": 1473238800,
          "value": null
        },
        {
          "timestamp": 1473238860,
          "value": null
        },
        {
          "timestamp": 1473238920,
          "value": null
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "disk.io.read_bytes/device=sda"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.93.90",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": 99.5
        },
        {
          "timestamp": 1473235500,
          "value": 98.917118
        },
        {
          "timestamp": 1473235560,
          "value": 96.791667
        },
        {
          "timestamp": 1473235620,
          "value": 98.709409
        },
        {
          "timestamp": 1473235680,
          "value": 98.833333
        },
        {
          "timestamp": 1473235740,
          "value": 99.167014
        },
        {
          "timestamp": 1473235800,
          "value": 99.916701
        },
        {
          "timestamp": 1473235860,
          "value": 99.916701
        },
        {
          "timestamp": 1473235920,
          "value": 99.916701
        },
        {
          "timestamp": 1473235980,
          "value": 99.958368
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": 97.792586
        },
        {
          "timestamp": 1473236460,
          "value": 97.792586
        },
        {
          "timestamp": 1473236520,
          "value": 99.958351
        },
        {
          "timestamp": 1473236580,
          "value": 100.0
        },
        {
          "timestamp": 1473236640,
          "value": 97.625989
        },
        {
          "timestamp": 1473236700,
          "value": 97.791667
        },
        {
          "timestamp": 1473236760,
          "value": 97.83243
        },
        {
          "timestamp": 1473236820,
          "value": 99.291962
        },
        {
          "timestamp": 1473236880,
          "value": 99.958368
        },
        {
          "timestamp": 1473236940,
          "value": 97.540642
        },
        {
          "timestamp": 1473237000,
          "value": 99.916736
        },
        {
          "timestamp": 1473237060,
          "value": 99.916701
        },
        {
          "timestamp": 1473237120,
          "value": 99.916701
        },
        {
          "timestamp": 1473237180,
          "value": 99.875156
        },
        {
          "timestamp": 1473237240,
          "value": 99.625156
        },
        {
          "timestamp": 1473237300,
          "value": 99.916736
        },
        {
          "timestamp": 1473237360,
          "value": 99.875052
        },
        {
          "timestamp": 1473237420,
          "value": 99.875104
        },
        {
          "timestamp": 1473237480,
          "value": 99.958351
        },
        {
          "timestamp": 1473237540,
          "value": 99.958333
        },
        {
          "timestamp": 1473237600,
          "value": 99.958333
        },
        {
          "timestamp": 1473237660,
          "value": 99.916736
        },
        {
          "timestamp": 1473237720,
          "value": 97.375
        },
        {
          "timestamp": 1473237780,
          "value": 99.958351
        },
        {
          "timestamp": 1473237840,
          "value": 100.0
        },
        {
          "timestamp": 1473237900,
          "value": 99.916736
        },
        {
          "timestamp": 1473237960,
          "value": 99.916736
        },
        {
          "timestamp": 1473238020,
          "value": 99.958351
        },
        {
          "timestamp": 1473238080,
          "value": 99.958351
        },
        {
          "timestamp": 1473238140,
          "value": 97.709288
        },
        {
          "timestamp": 1473238200,
          "value": 97.666667
        },
        {
          "timestamp": 1473238260,
          "value": 99.916736
        },
        {
          "timestamp": 1473238320,
          "value": 99.958351
        },
        {
          "timestamp": 1473238380,
          "value": 99.916736
        },
        {
          "timestamp": 1473238440,
          "value": 99.958368
        },
        {
          "timestamp": 1473238500,
          "value": null
        },
        {
          "timestamp": 1473238560,
          "value": null
        },
        {
          "timestamp": 1473238620,
          "value": null
        },
        {
          "timestamp": 1473238680,
          "value": null
        },
        {
          "timestamp": 1473238740,
          "value": null
        },
        {
          "timestamp": 1473238800,
          "value": null
        },
        {
          "timestamp": 1473238860,
          "value": null
        },
        {
          "timestamp": 1473238920,
          "value": null
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "cpu.idle"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.93.90",
      "Values": [
        {
          "timestamp": 1473235440,
          "value": 0.0
        },
        {
          "timestamp": 1473235500,
          "value": 12288.0
        },
        {
          "timestamp": 1473235560,
          "value": 0.0
        },
        {
          "timestamp": 1473235620,
          "value": 0.0
        },
        {
          "timestamp": 1473235680,
          "value": 0.0
        },
        {
          "timestamp": 1473235740,
          "value": 98304.0
        },
        {
          "timestamp": 1473235800,
          "value": 12288.0
        },
        {
          "timestamp": 1473235860,
          "value": 0.0
        },
        {
          "timestamp": 1473235920,
          "value": 0.0
        },
        {
          "timestamp": 1473235980,
          "value": 0.0
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": 81920.0
        },
        {
          "timestamp": 1473236460,
          "value": 81920.0
        },
        {
          "timestamp": 1473236520,
          "value": 0.0
        },
        {
          "timestamp": 1473236580,
          "value": 0.0
        },
        {
          "timestamp": 1473236640,
          "value": 0.0
        },
        {
          "timestamp": 1473236700,
          "value": 0.0
        },
        {
          "timestamp": 1473236760,
          "value": 0.0
        },
        {
          "timestamp": 1473236820,
          "value": 0.0
        },
        {
          "timestamp": 1473236880,
          "value": 167936.0
        },
        {
          "timestamp": 1473236940,
          "value": 24576.0
        },
        {
          "timestamp": 1473237000,
          "value": 12288.0
        },
        {
          "timestamp": 1473237060,
          "value": 57344.0
        },
        {
          "timestamp": 1473237120,
          "value": 0.0
        },
        {
          "timestamp": 1473237180,
          "value": 0.0
        },
        {
          "timestamp": 1473237240,
          "value": 0.0
        },
        {
          "timestamp": 1473237300,
          "value": 12288.0
        },
        {
          "timestamp": 1473237360,
          "value": 0.0
        },
        {
          "timestamp": 1473237420,
          "value": 24576.0
        },
        {
          "timestamp": 1473237480,
          "value": 12288.0
        },
        {
          "timestamp": 1473237540,
          "value": 0.0
        },
        {
          "timestamp": 1473237600,
          "value": 0.0
        },
        {
          "timestamp": 1473237660,
          "value": 53248.0
        },
        {
          "timestamp": 1473237720,
          "value": 0.0
        },
        {
          "timestamp": 1473237780,
          "value": 12288.0
        },
        {
          "timestamp": 1473237840,
          "value": 0.0
        },
        {
          "timestamp": 1473237900,
          "value": 65536.0
        },
        {
          "timestamp": 1473237960,
          "value": 0.0
        },
        {
          "timestamp": 1473238020,
          "value": 0.0
        },
        {
          "timestamp": 1473238080,
          "value": 12288.0
        },
        {
          "timestamp": 1473238140,
          "value": 0.0
        },
        {
          "timestamp": 1473238200,
          "value": 12288.0
        },
        {
          "timestamp": 1473238260,
          "value": 0.0
        },
        {
          "timestamp": 1473238320,
          "value": 0.0
        },
        {
          "timestamp": 1473238380,
          "value": 0.0
        },
        {
          "timestamp": 1473238440,
          "value": null
        },
        {
          "timestamp": 1473238500,
          "value": null
        },
        {
          "timestamp": 1473238560,
          "value": null
        },
        {
          "timestamp": 1473238620,
          "value": null
        },
        {
          "timestamp": 1473238680,
          "value": null
        },
        {
          "timestamp": 1473238740,
          "value": null
        },
        {
          "timestamp": 1473238800,
          "value": null
        },
        {
          "timestamp": 1473238860,
          "value": null
        },
        {
          "timestamp": 1473238920,
          "value": null
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "disk.io.write_bytes/device=sda"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.93.97",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": 0.0
        },
        {
          "timestamp": 1473235500,
          "value": 0.0
        },
        {
          "timestamp": 1473235560,
          "value": null
        },
        {
          "timestamp": 1473235620,
          "value": null
        },
        {
          "timestamp": 1473235680,
          "value": null
        },
        {
          "timestamp": 1473235740,
          "value": 0.0
        },
        {
          "timestamp": 1473235800,
          "value": 0.0
        },
        {
          "timestamp": 1473235860,
          "value": 0.0
        },
        {
          "timestamp": 1473235920,
          "value": 0.0
        },
        {
          "timestamp": 1473235980,
          "value": null
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": null
        },
        {
          "timestamp": 1473236520,
          "value": null
        },
        {
          "timestamp": 1473236580,
          "value": 0.0
        },
        {
          "timestamp": 1473236640,
          "value": 0.0
        },
        {
          "timestamp": 1473236700,
          "value": 0.0
        },
        {
          "timestamp": 1473236760,
          "value": 0.0
        },
        {
          "timestamp": 1473236820,
          "value": 0.0
        },
        {
          "timestamp": 1473236880,
          "value": 0.0
        },
        {
          "timestamp": 1473236940,
          "value": 0.0
        },
        {
          "timestamp": 1473237000,
          "value": 0.0
        },
        {
          "timestamp": 1473237060,
          "value": 0.0
        },
        {
          "timestamp": 1473237120,
          "value": 0.0
        },
        {
          "timestamp": 1473237180,
          "value": 0.0
        },
        {
          "timestamp": 1473237240,
          "value": 0.0
        },
        {
          "timestamp": 1473237300,
          "value": null
        },
        {
          "timestamp": 1473237360,
          "value": null
        },
        {
          "timestamp": 1473237420,
          "value": null
        },
        {
          "timestamp": 1473237480,
          "value": 0.0
        },
        {
          "timestamp": 1473237540,
          "value": 0.0
        },
        {
          "timestamp": 1473237600,
          "value": 0.0
        },
        {
          "timestamp": 1473237660,
          "value": 0.0
        },
        {
          "timestamp": 1473237720,
          "value": 0.0
        },
        {
          "timestamp": 1473237780,
          "value": null
        },
        {
          "timestamp": 1473237840,
          "value": 0.0
        },
        {
          "timestamp": 1473237900,
          "value": 0.0
        },
        {
          "timestamp": 1473237960,
          "value": 0.0
        },
        {
          "timestamp": 1473238020,
          "value": 0.0
        },
        {
          "timestamp": 1473238080,
          "value": 0.0
        },
        {
          "timestamp": 1473238140,
          "value": 0.0
        },
        {
          "timestamp": 1473238200,
          "value": 0.0
        },
        {
          "timestamp": 1473238260,
          "value": null
        },
        {
          "timestamp": 1473238320,
          "value": 0.0
        },
        {
          "timestamp": 1473238380,
          "value": 8192.0
        },
        {
          "timestamp": 1473238440,
          "value": null
        },
        {
          "timestamp": 1473238500,
          "value": 0.0
        },
        {
          "timestamp": 1473238560,
          "value": 8192.0
        },
        {
          "timestamp": 1473238620,
          "value": 0.0
        },
        {
          "timestamp": 1473238680,
          "value": 0.0
        },
        {
          "timestamp": 1473238740,
          "value": 0.0
        },
        {
          "timestamp": 1473238800,
          "value": null
        },
        {
          "timestamp": 1473238860,
          "value": null
        },
        {
          "timestamp": 1473238920,
          "value": null
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "disk.io.read_bytes/device=sda"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.93.97",
      "Values": [
        {
          "timestamp": 1473235440,
          "value": 99.916736
        },
        {
          "timestamp": 1473235500,
          "value": 99.916736
        },
        {
          "timestamp": 1473235560,
          "value": null
        },
        {
          "timestamp": 1473235620,
          "value": null
        },
        {
          "timestamp": 1473235680,
          "value": null
        },
        {
          "timestamp": 1473235740,
          "value": 99.872232
        },
        {
          "timestamp": 1473235800,
          "value": 99.583333
        },
        {
          "timestamp": 1473235860,
          "value": 99.916562
        },
        {
          "timestamp": 1473235920,
          "value": 99.916771
        },
        {
          "timestamp": 1473235980,
          "value": null
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": null
        },
        {
          "timestamp": 1473236520,
          "value": 99.79158
        },
        {
          "timestamp": 1473236580,
          "value": 100.0
        },
        {
          "timestamp": 1473236640,
          "value": 100.0
        },
        {
          "timestamp": 1473236700,
          "value": 99.875104
        },
        {
          "timestamp": 1473236760,
          "value": 99.958351
        },
        {
          "timestamp": 1473236820,
          "value": 100.0
        },
        {
          "timestamp": 1473236880,
          "value": 99.958368
        },
        {
          "timestamp": 1473236940,
          "value": 100.0
        },
        {
          "timestamp": 1473237000,
          "value": 99.708576
        },
        {
          "timestamp": 1473237060,
          "value": 96.543107
        },
        {
          "timestamp": 1473237120,
          "value": 97.502082
        },
        {
          "timestamp": 1473237180,
          "value": 99.958351
        },
        {
          "timestamp": 1473237240,
          "value": 99.958351
        },
        {
          "timestamp": 1473237300,
          "value": 100.0
        },
        {
          "timestamp": 1473237360,
          "value": 99.958351
        },
        {
          "timestamp": 1473237420,
          "value": 99.916771
        },
        {
          "timestamp": 1473237480,
          "value": 100.0
        },
        {
          "timestamp": 1473237540,
          "value": 99.958333
        },
        {
          "timestamp": 1473237600,
          "value": 99.916736
        },
        {
          "timestamp": 1473237660,
          "value": 99.875156
        },
        {
          "timestamp": 1473237720,
          "value": 99.958351
        },
        {
          "timestamp": 1473237780,
          "value": 99.958351
        },
        {
          "timestamp": 1473237840,
          "value": 99.916736
        },
        {
          "timestamp": 1473237900,
          "value": 99.916736
        },
        {
          "timestamp": 1473237960,
          "value": 99.958368
        },
        {
          "timestamp": 1473238020,
          "value": 99.958368
        },
        {
          "timestamp": 1473238080,
          "value": 99.958368
        },
        {
          "timestamp": 1473238140,
          "value": 98.208333
        },
        {
          "timestamp": 1473238200,
          "value": 100.0
        },
        {
          "timestamp": 1473238260,
          "value": 99.958351
        },
        {
          "timestamp": 1473238320,
          "value": 98.042482
        },
        {
          "timestamp": 1473238380,
          "value": 99.958368
        },
        {
          "timestamp": 1473238440,
          "value": 99.916805
        },
        {
          "timestamp": 1473238500,
          "value": 99.958368
        },
        {
          "timestamp": 1473238560,
          "value": 99.958333
        },
        {
          "timestamp": 1473238620,
          "value": 97.417743
        },
        {
          "timestamp": 1473238680,
          "value": 99.916771
        },
        {
          "timestamp": 1473238740,
          "value": 100.0
        },
        {
          "timestamp": 1473238800,
          "value": null
        },
        {
          "timestamp": 1473238860,
          "value": null
        },
        {
          "timestamp": 1473238920,
          "value": null
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "cpu.idle"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.93.97",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": 0.0
        },
        {
          "timestamp": 1473235500,
          "value": 0.0
        },
        {
          "timestamp": 1473235560,
          "value": null
        },
        {
          "timestamp": 1473235620,
          "value": null
        },
        {
          "timestamp": 1473235680,
          "value": null
        },
        {
          "timestamp": 1473235740,
          "value": 32768.0
        },
        {
          "timestamp": 1473235800,
          "value": 0.0
        },
        {
          "timestamp": 1473235860,
          "value": 65536.0
        },
        {
          "timestamp": 1473235920,
          "value": 0.0
        },
        {
          "timestamp": 1473235980,
          "value": null
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": null
        },
        {
          "timestamp": 1473236520,
          "value": null
        },
        {
          "timestamp": 1473236580,
          "value": 65536.0
        },
        {
          "timestamp": 1473236640,
          "value": 65536.0
        },
        {
          "timestamp": 1473236700,
          "value": 94208.0
        },
        {
          "timestamp": 1473236760,
          "value": 65536.0
        },
        {
          "timestamp": 1473236820,
          "value": 77824.0
        },
        {
          "timestamp": 1473236880,
          "value": 0.0
        },
        {
          "timestamp": 1473236940,
          "value": 32768.0
        },
        {
          "timestamp": 1473237000,
          "value": 0.0
        },
        {
          "timestamp": 1473237060,
          "value": 0.0
        },
        {
          "timestamp": 1473237120,
          "value": 81920.0
        },
        {
          "timestamp": 1473237180,
          "value": 184320.0
        },
        {
          "timestamp": 1473237240,
          "value": 61440.0
        },
        {
          "timestamp": 1473237300,
          "value": null
        },
        {
          "timestamp": 1473237360,
          "value": null
        },
        {
          "timestamp": 1473237420,
          "value": null
        },
        {
          "timestamp": 1473237480,
          "value": 0.0
        },
        {
          "timestamp": 1473237540,
          "value": 0.0
        },
        {
          "timestamp": 1473237600,
          "value": 0.0
        },
        {
          "timestamp": 1473237660,
          "value": 12288.0
        },
        {
          "timestamp": 1473237720,
          "value": 0.0
        },
        {
          "timestamp": 1473237780,
          "value": 0.0
        },
        {
          "timestamp": 1473237840,
          "value": 0.0
        },
        {
          "timestamp": 1473237900,
          "value": 0.0
        },
        {
          "timestamp": 1473237960,
          "value": 0.0
        },
        {
          "timestamp": 1473238020,
          "value": 0.0
        },
        {
          "timestamp": 1473238080,
          "value": 139264.0
        },
        {
          "timestamp": 1473238140,
          "value": 32768.0
        },
        {
          "timestamp": 1473238200,
          "value": 122880.0
        },
        {
          "timestamp": 1473238260,
          "value": null
        },
        {
          "timestamp": 1473238320,
          "value": 53248.0
        },
        {
          "timestamp": 1473238380,
          "value": 0.0
        },
        {
          "timestamp": 1473238440,
          "value": null
        },
        {
          "timestamp": 1473238500,
          "value": 98304.0
        },
        {
          "timestamp": 1473238560,
          "value": 0.0
        },
        {
          "timestamp": 1473238620,
          "value": 12288.0
        },
        {
          "timestamp": 1473238680,
          "value": 0.0
        },
        {
          "timestamp": 1473238740,
          "value": 0.0
        },
        {
          "timestamp": 1473238800,
          "value": null
        },
        {
          "timestamp": 1473238860,
          "value": null
        },
        {
          "timestamp": 1473238920,
          "value": null
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "disk.io.write_bytes/device=sda"
    }
  ],
  "lb": [
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.104.212",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": null
        },
        {
          "timestamp": 1473235500,
          "value": null
        },
        {
          "timestamp": 1473235560,
          "value": null
        },
        {
          "timestamp": 1473235620,
          "value": null
        },
        {
          "timestamp": 1473235680,
          "value": null
        },
        {
          "timestamp": 1473235740,
          "value": null
        },
        {
          "timestamp": 1473235800,
          "value": null
        },
        {
          "timestamp": 1473235860,
          "value": null
        },
        {
          "timestamp": 1473235920,
          "value": null
        },
        {
          "timestamp": 1473235980,
          "value": null
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": 0.0
        },
        {
          "timestamp": 1473236220,
          "value": 0.0
        },
        {
          "timestamp": 1473236280,
          "value": 0.0
        },
        {
          "timestamp": 1473236340,
          "value": 0.0
        },
        {
          "timestamp": 1473236400,
          "value": 0.0
        },
        {
          "timestamp": 1473236460,
          "value": 0.0
        },
        {
          "timestamp": 1473236520,
          "value": 0.0
        },
        {
          "timestamp": 1473236580,
          "value": 0.0
        },
        {
          "timestamp": 1473236640,
          "value": 0.0
        },
        {
          "timestamp": 1473236700,
          "value": 0.0
        },
        {
          "timestamp": 1473236760,
          "value": 0.0
        },
        {
          "timestamp": 1473236820,
          "value": 0.0
        },
        {
          "timestamp": 1473236880,
          "value": 0.0
        },
        {
          "timestamp": 1473236940,
          "value": 0.0
        },
        {
          "timestamp": 1473237000,
          "value": 0.0
        },
        {
          "timestamp": 1473237060,
          "value": 0.0
        },
        {
          "timestamp": 1473237120,
          "value": 0.0
        },
        {
          "timestamp": 1473237180,
          "value": 0.0
        },
        {
          "timestamp": 1473237240,
          "value": 0.0
        },
        {
          "timestamp": 1473237300,
          "value": 0.0
        },
        {
          "timestamp": 1473237360,
          "value": 0.0
        },
        {
          "timestamp": 1473237420,
          "value": 0.0
        },
        {
          "timestamp": 1473237480,
          "value": 0.0
        },
        {
          "timestamp": 1473237540,
          "value": 0.0
        },
        {
          "timestamp": 1473237600,
          "value": 0.0
        },
        {
          "timestamp": 1473237660,
          "value": 0.0
        },
        {
          "timestamp": 1473237720,
          "value": 0.0
        },
        {
          "timestamp": 1473237780,
          "value": 0.0
        },
        {
          "timestamp": 1473237840,
          "value": null
        },
        {
          "timestamp": 1473237900,
          "value": 0.0
        },
        {
          "timestamp": 1473237960,
          "value": 0.0
        },
        {
          "timestamp": 1473238020,
          "value": 0.0
        },
        {
          "timestamp": 1473238080,
          "value": null
        },
        {
          "timestamp": 1473238140,
          "value": 0.0
        },
        {
          "timestamp": 1473238200,
          "value": 0.0
        },
        {
          "timestamp": 1473238260,
          "value": 0.0
        },
        {
          "timestamp": 1473238320,
          "value": 0.0
        },
        {
          "timestamp": 1473238380,
          "value": 0.0
        },
        {
          "timestamp": 1473238440,
          "value": 0.0
        },
        {
          "timestamp": 1473238500,
          "value": 0.0
        },
        {
          "timestamp": 1473238560,
          "value": null
        },
        {
          "timestamp": 1473238620,
          "value": 0.0
        },
        {
          "timestamp": 1473238680,
          "value": 0.0
        },
        {
          "timestamp": 1473238740,
          "value": null
        },
        {
          "timestamp": 1473238800,
          "value": 0.0
        },
        {
          "timestamp": 1473238860,
          "value": 0.0
        },
        {
          "timestamp": 1473238920,
          "value": 0.0
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "disk.io.read_bytes/device=sda"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.104.212",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": null
        },
        {
          "timestamp": 1473235500,
          "value": null
        },
        {
          "timestamp": 1473235560,
          "value": null
        },
        {
          "timestamp": 1473235620,
          "value": null
        },
        {
          "timestamp": 1473235680,
          "value": null
        },
        {
          "timestamp": 1473235740,
          "value": null
        },
        {
          "timestamp": 1473235800,
          "value": null
        },
        {
          "timestamp": 1473235860,
          "value": null
        },
        {
          "timestamp": 1473235920,
          "value": null
        },
        {
          "timestamp": 1473235980,
          "value": null
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": 92.921734
        },
        {
          "timestamp": 1473236220,
          "value": 87.550829
        },
        {
          "timestamp": 1473236280,
          "value": 93.878826
        },
        {
          "timestamp": 1473236340,
          "value": 91.195754
        },
        {
          "timestamp": 1473236400,
          "value": 94.283037
        },
        {
          "timestamp": 1473236460,
          "value": 88.29421
        },
        {
          "timestamp": 1473236520,
          "value": 87.347322
        },
        {
          "timestamp": 1473236580,
          "value": 86.708464
        },
        {
          "timestamp": 1473236640,
          "value": 87.918623
        },
        {
          "timestamp": 1473236700,
          "value": 88.253671
        },
        {
          "timestamp": 1473236760,
          "value": 87.51955
        },
        {
          "timestamp": 1473236820,
          "value": 88.25
        },
        {
          "timestamp": 1473236880,
          "value": 85.826278
        },
        {
          "timestamp": 1473236940,
          "value": 90.650407
        },
        {
          "timestamp": 1473237000,
          "value": 95.47864
        },
        {
          "timestamp": 1473237060,
          "value": 94.776353
        },
        {
          "timestamp": 1473237120,
          "value": 87.272727
        },
        {
          "timestamp": 1473237180,
          "value": 91.8125
        },
        {
          "timestamp": 1473237240,
          "value": 90.334689
        },
        {
          "timestamp": 1473237300,
          "value": 93.212387
        },
        {
          "timestamp": 1473237360,
          "value": 86.103286
        },
        {
          "timestamp": 1473237420,
          "value": 85.9199
        },
        {
          "timestamp": 1473237480,
          "value": 91.395494
        },
        {
          "timestamp": 1473237540,
          "value": 85.409476
        },
        {
          "timestamp": 1473237600,
          "value": 92.596064
        },
        {
          "timestamp": 1473237660,
          "value": 92.057536
        },
        {
          "timestamp": 1473237720,
          "value": 88.89584
        },
        {
          "timestamp": 1473237780,
          "value": 94.340213
        },
        {
          "timestamp": 1473237840,
          "value": null
        },
        {
          "timestamp": 1473237900,
          "value": 93.174703
        },
        {
          "timestamp": 1473237960,
          "value": 89.188342
        },
        {
          "timestamp": 1473238020,
          "value": 94.467021
        },
        {
          "timestamp": 1473238080,
          "value": null
        },
        {
          "timestamp": 1473238140,
          "value": 92.002499
        },
        {
          "timestamp": 1473238200,
          "value": 86.658315
        },
        {
          "timestamp": 1473238260,
          "value": 94.284822
        },
        {
          "timestamp": 1473238320,
          "value": 88.923655
        },
        {
          "timestamp": 1473238380,
          "value": 93.556459
        },
        {
          "timestamp": 1473238440,
          "value": 93.847595
        },
        {
          "timestamp": 1473238500,
          "value": 92.604199
        },
        {
          "timestamp": 1473238560,
          "value": null
        },
        {
          "timestamp": 1473238620,
          "value": 91.216005
        },
        {
          "timestamp": 1473238680,
          "value": 91.324773
        },
        {
          "timestamp": 1473238740,
          "value": null
        },
        {
          "timestamp": 1473238800,
          "value": 93.779306
        },
        {
          "timestamp": 1473238860,
          "value": 84.44722
        },
        {
          "timestamp": 1473238920,
          "value": 81.524467
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "cpu.idle"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.104.212",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": null
        },
        {
          "timestamp": 1473235500,
          "value": null
        },
        {
          "timestamp": 1473235560,
          "value": null
        },
        {
          "timestamp": 1473235620,
          "value": null
        },
        {
          "timestamp": 1473235680,
          "value": null
        },
        {
          "timestamp": 1473235740,
          "value": null
        },
        {
          "timestamp": 1473235800,
          "value": null
        },
        {
          "timestamp": 1473235860,
          "value": null
        },
        {
          "timestamp": 1473235920,
          "value": null
        },
        {
          "timestamp": 1473235980,
          "value": null
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": 0.0
        },
        {
          "timestamp": 1473236220,
          "value": 0.0
        },
        {
          "timestamp": 1473236280,
          "value": 0.0
        },
        {
          "timestamp": 1473236340,
          "value": 0.0
        },
        {
          "timestamp": 1473236400,
          "value": 0.0
        },
        {
          "timestamp": 1473236460,
          "value": 0.0
        },
        {
          "timestamp": 1473236520,
          "value": 0.0
        },
        {
          "timestamp": 1473236580,
          "value": 4096.0
        },
        {
          "timestamp": 1473236640,
          "value": 0.0
        },
        {
          "timestamp": 1473236700,
          "value": 0.0
        },
        {
          "timestamp": 1473236760,
          "value": 0.0
        },
        {
          "timestamp": 1473236820,
          "value": 0.0
        },
        {
          "timestamp": 1473236880,
          "value": 0.0
        },
        {
          "timestamp": 1473236940,
          "value": 0.0
        },
        {
          "timestamp": 1473237000,
          "value": 0.0
        },
        {
          "timestamp": 1473237060,
          "value": 0.0
        },
        {
          "timestamp": 1473237120,
          "value": 0.0
        },
        {
          "timestamp": 1473237180,
          "value": 0.0
        },
        {
          "timestamp": 1473237240,
          "value": 0.0
        },
        {
          "timestamp": 1473237300,
          "value": 0.0
        },
        {
          "timestamp": 1473237360,
          "value": 4096.0
        },
        {
          "timestamp": 1473237420,
          "value": 4096.0
        },
        {
          "timestamp": 1473237480,
          "value": 0.0
        },
        {
          "timestamp": 1473237540,
          "value": 0.0
        },
        {
          "timestamp": 1473237600,
          "value": 0.0
        },
        {
          "timestamp": 1473237660,
          "value": 0.0
        },
        {
          "timestamp": 1473237720,
          "value": 8192.0
        },
        {
          "timestamp": 1473237780,
          "value": 0.0
        },
        {
          "timestamp": 1473237840,
          "value": null
        },
        {
          "timestamp": 1473237900,
          "value": 0.0
        },
        {
          "timestamp": 1473237960,
          "value": 4096.0
        },
        {
          "timestamp": 1473238020,
          "value": 0.0
        },
        {
          "timestamp": 1473238080,
          "value": null
        },
        {
          "timestamp": 1473238140,
          "value": 0.0
        },
        {
          "timestamp": 1473238200,
          "value": 0.0
        },
        {
          "timestamp": 1473238260,
          "value": 0.0
        },
        {
          "timestamp": 1473238320,
          "value": 0.0
        },
        {
          "timestamp": 1473238380,
          "value": 0.0
        },
        {
          "timestamp": 1473238440,
          "value": 0.0
        },
        {
          "timestamp": 1473238500,
          "value": 0.0
        },
        {
          "timestamp": 1473238560,
          "value": null
        },
        {
          "timestamp": 1473238620,
          "value": 0.0
        },
        {
          "timestamp": 1473238680,
          "value": 0.0
        },
        {
          "timestamp": 1473238740,
          "value": null
        },
        {
          "timestamp": 1473238800,
          "value": 0.0
        },
        {
          "timestamp": 1473238860,
          "value": 0.0
        },
        {
          "timestamp": 1473238920,
          "value": 0.0
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "disk.io.write_bytes/device=sda"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.122.130",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": null
        },
        {
          "timestamp": 1473235500,
          "value": null
        },
        {
          "timestamp": 1473235560,
          "value": 0.0
        },
        {
          "timestamp": 1473235620,
          "value": null
        },
        {
          "timestamp": 1473235680,
          "value": null
        },
        {
          "timestamp": 1473235740,
          "value": null
        },
        {
          "timestamp": 1473235800,
          "value": null
        },
        {
          "timestamp": 1473235860,
          "value": null
        },
        {
          "timestamp": 1473235920,
          "value": null
        },
        {
          "timestamp": 1473235980,
          "value": null
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": null
        },
        {
          "timestamp": 1473236520,
          "value": null
        },
        {
          "timestamp": 1473236580,
          "value": null
        },
        {
          "timestamp": 1473236640,
          "value": 0.0
        },
        {
          "timestamp": 1473236700,
          "value": 0.0
        },
        {
          "timestamp": 1473236760,
          "value": 0.0
        },
        {
          "timestamp": 1473236820,
          "value": 0.0
        },
        {
          "timestamp": 1473236880,
          "value": 0.0
        },
        {
          "timestamp": 1473236940,
          "value": 0.0
        },
        {
          "timestamp": 1473237000,
          "value": 0.0
        },
        {
          "timestamp": 1473237060,
          "value": 0.0
        },
        {
          "timestamp": 1473237120,
          "value": 0.0
        },
        {
          "timestamp": 1473237180,
          "value": 0.0
        },
        {
          "timestamp": 1473237240,
          "value": 0.0
        },
        {
          "timestamp": 1473237300,
          "value": 0.0
        },
        {
          "timestamp": 1473237360,
          "value": 0.0
        },
        {
          "timestamp": 1473237420,
          "value": 0.0
        },
        {
          "timestamp": 1473237480,
          "value": 0.0
        },
        {
          "timestamp": 1473237540,
          "value": 0.0
        },
        {
          "timestamp": 1473237600,
          "value": 0.0
        },
        {
          "timestamp": 1473237660,
          "value": 0.0
        },
        {
          "timestamp": 1473237720,
          "value": 0.0
        },
        {
          "timestamp": 1473237780,
          "value": 0.0
        },
        {
          "timestamp": 1473237840,
          "value": 0.0
        },
        {
          "timestamp": 1473237900,
          "value": 0.0
        },
        {
          "timestamp": 1473237960,
          "value": 0.0
        },
        {
          "timestamp": 1473238020,
          "value": 0.0
        },
        {
          "timestamp": 1473238080,
          "value": 0.0
        },
        {
          "timestamp": 1473238140,
          "value": 0.0
        },
        {
          "timestamp": 1473238200,
          "value": 0.0
        },
        {
          "timestamp": 1473238260,
          "value": 0.0
        },
        {
          "timestamp": 1473238320,
          "value": 0.0
        },
        {
          "timestamp": 1473238380,
          "value": 0.0
        },
        {
          "timestamp": 1473238440,
          "value": 0.0
        },
        {
          "timestamp": 1473238500,
          "value": null
        },
        {
          "timestamp": 1473238560,
          "value": 0.0
        },
        {
          "timestamp": 1473238620,
          "value": 0.0
        },
        {
          "timestamp": 1473238680,
          "value": null
        },
        {
          "timestamp": 1473238740,
          "value": null
        },
        {
          "timestamp": 1473238800,
          "value": null
        },
        {
          "timestamp": 1473238860,
          "value": null
        },
        {
          "timestamp": 1473238920,
          "value": null
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "disk.io.read_bytes/device=sda"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.122.130",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": null
        },
        {
          "timestamp": 1473235500,
          "value": null
        },
        {
          "timestamp": 1473235560,
          "value": 97.917534
        },
        {
          "timestamp": 1473235620,
          "value": null
        },
        {
          "timestamp": 1473235680,
          "value": null
        },
        {
          "timestamp": 1473235740,
          "value": null
        },
        {
          "timestamp": 1473235800,
          "value": null
        },
        {
          "timestamp": 1473235860,
          "value": null
        },
        {
          "timestamp": 1473235920,
          "value": null
        },
        {
          "timestamp": 1473235980,
          "value": null
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": null
        },
        {
          "timestamp": 1473236520,
          "value": null
        },
        {
          "timestamp": 1473236580,
          "value": null
        },
        {
          "timestamp": 1473236640,
          "value": 97.789825
        },
        {
          "timestamp": 1473236700,
          "value": 95.116861
        },
        {
          "timestamp": 1473236760,
          "value": 97.581318
        },
        {
          "timestamp": 1473236820,
          "value": 97.829716
        },
        {
          "timestamp": 1473236880,
          "value": 97.582326
        },
        {
          "timestamp": 1473236940,
          "value": 97.748123
        },
        {
          "timestamp": 1473237000,
          "value": 89.506689
        },
        {
          "timestamp": 1473237060,
          "value": 97.704508
        },
        {
          "timestamp": 1473237120,
          "value": 97.625
        },
        {
          "timestamp": 1473237180,
          "value": 97.539616
        },
        {
          "timestamp": 1473237240,
          "value": 98.122653
        },
        {
          "timestamp": 1473237300,
          "value": 97.705465
        },
        {
          "timestamp": 1473237360,
          "value": 97.787056
        },
        {
          "timestamp": 1473237420,
          "value": 97.707378
        },
        {
          "timestamp": 1473237480,
          "value": 97.288277
        },
        {
          "timestamp": 1473237540,
          "value": 97.668609
        },
        {
          "timestamp": 1473237600,
          "value": 98.162839
        },
        {
          "timestamp": 1473237660,
          "value": 95.875
        },
        {
          "timestamp": 1473237720,
          "value": 96.040017
        },
        {
          "timestamp": 1473237780,
          "value": 97.287145
        },
        {
          "timestamp": 1473237840,
          "value": 96.544546
        },
        {
          "timestamp": 1473237900,
          "value": 97.955778
        },
        {
          "timestamp": 1473237960,
          "value": 97.955778
        },
        {
          "timestamp": 1473238020,
          "value": 97.706422
        },
        {
          "timestamp": 1473238080,
          "value": 97.078464
        },
        {
          "timestamp": 1473238140,
          "value": 97.87234
        },
        {
          "timestamp": 1473238200,
          "value": 97.706422
        },
        {
          "timestamp": 1473238260,
          "value": 98.0
        },
        {
          "timestamp": 1473238320,
          "value": 98.082534
        },
        {
          "timestamp": 1473238380,
          "value": 97.792586
        },
        {
          "timestamp": 1473238440,
          "value": 97.540642
        },
        {
          "timestamp": 1473238500,
          "value": null
        },
        {
          "timestamp": 1473238560,
          "value": 97.873228
        },
        {
          "timestamp": 1473238620,
          "value": 97.87234
        },
        {
          "timestamp": 1473238680,
          "value": null
        },
        {
          "timestamp": 1473238740,
          "value": null
        },
        {
          "timestamp": 1473238800,
          "value": null
        },
        {
          "timestamp": 1473238860,
          "value": null
        },
        {
          "timestamp": 1473238920,
          "value": null
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "cpu.idle"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.122.130",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": null
        },
        {
          "timestamp": 1473235500,
          "value": null
        },
        {
          "timestamp": 1473235560,
          "value": 73728.0
        },
        {
          "timestamp": 1473235620,
          "value": null
        },
        {
          "timestamp": 1473235680,
          "value": null
        },
        {
          "timestamp": 1473235740,
          "value": null
        },
        {
          "timestamp": 1473235800,
          "value": null
        },
        {
          "timestamp": 1473235860,
          "value": null
        },
        {
          "timestamp": 1473235920,
          "value": null
        },
        {
          "timestamp": 1473235980,
          "value": null
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": null
        },
        {
          "timestamp": 1473236520,
          "value": null
        },
        {
          "timestamp": 1473236580,
          "value": null
        },
        {
          "timestamp": 1473236640,
          "value": 24576.0
        },
        {
          "timestamp": 1473236700,
          "value": 8192.0
        },
        {
          "timestamp": 1473236760,
          "value": 16384.0
        },
        {
          "timestamp": 1473236820,
          "value": 131072.0
        },
        {
          "timestamp": 1473236880,
          "value": 12288.0
        },
        {
          "timestamp": 1473236940,
          "value": 73728.0
        },
        {
          "timestamp": 1473237000,
          "value": 12288.0
        },
        {
          "timestamp": 1473237060,
          "value": 12288.0
        },
        {
          "timestamp": 1473237120,
          "value": 102400.0
        },
        {
          "timestamp": 1473237180,
          "value": 12288.0
        },
        {
          "timestamp": 1473237240,
          "value": 12288.0
        },
        {
          "timestamp": 1473237300,
          "value": 0.0
        },
        {
          "timestamp": 1473237360,
          "value": 0.0
        },
        {
          "timestamp": 1473237420,
          "value": 0.0
        },
        {
          "timestamp": 1473237480,
          "value": 0.0
        },
        {
          "timestamp": 1473237540,
          "value": 98304.0
        },
        {
          "timestamp": 1473237600,
          "value": 0.0
        },
        {
          "timestamp": 1473237660,
          "value": 12288.0
        },
        {
          "timestamp": 1473237720,
          "value": 139264.0
        },
        {
          "timestamp": 1473237780,
          "value": 12288.0
        },
        {
          "timestamp": 1473237840,
          "value": 12288.0
        },
        {
          "timestamp": 1473237900,
          "value": 12288.0
        },
        {
          "timestamp": 1473237960,
          "value": 12288.0
        },
        {
          "timestamp": 1473238020,
          "value": 12288.0
        },
        {
          "timestamp": 1473238080,
          "value": 12288.0
        },
        {
          "timestamp": 1473238140,
          "value": 73728.0
        },
        {
          "timestamp": 1473238200,
          "value": 16384.0
        },
        {
          "timestamp": 1473238260,
          "value": 12288.0
        },
        {
          "timestamp": 1473238320,
          "value": 12288.0
        },
        {
          "timestamp": 1473238380,
          "value": null
        },
        {
          "timestamp": 1473238440,
          "value": 12288.0
        },
        {
          "timestamp": 1473238500,
          "value": null
        },
        {
          "timestamp": 1473238560,
          "value": 12288.0
        },
        {
          "timestamp": 1473238620,
          "value": 12288.0
        },
        {
          "timestamp": 1473238680,
          "value": null
        },
        {
          "timestamp": 1473238740,
          "value": null
        },
        {
          "timestamp": 1473238800,
          "value": null
        },
        {
          "timestamp": 1473238860,
          "value": null
        },
        {
          "timestamp": 1473238920,
          "value": null
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "disk.io.write_bytes/device=sda"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.122.131",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": null
        },
        {
          "timestamp": 1473235500,
          "value": null
        },
        {
          "timestamp": 1473235560,
          "value": 0.0
        },
        {
          "timestamp": 1473235620,
          "value": null
        },
        {
          "timestamp": 1473235680,
          "value": null
        },
        {
          "timestamp": 1473235740,
          "value": null
        },
        {
          "timestamp": 1473235800,
          "value": null
        },
        {
          "timestamp": 1473235860,
          "value": 0.0
        },
        {
          "timestamp": 1473235920,
          "value": 0.0
        },
        {
          "timestamp": 1473235980,
          "value": 0.0
        },
        {
          "timestamp": 1473236040,
          "value": 0.0
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": 0.0
        },
        {
          "timestamp": 1473236520,
          "value": 0.0
        },
        {
          "timestamp": 1473236580,
          "value": 0.0
        },
        {
          "timestamp": 1473236640,
          "value": 0.0
        },
        {
          "timestamp": 1473236700,
          "value": 0.0
        },
        {
          "timestamp": 1473236760,
          "value": 0.0
        },
        {
          "timestamp": 1473236820,
          "value": 0.0
        },
        {
          "timestamp": 1473236880,
          "value": 0.0
        },
        {
          "timestamp": 1473236940,
          "value": 0.0
        },
        {
          "timestamp": 1473237000,
          "value": 0.0
        },
        {
          "timestamp": 1473237060,
          "value": 0.0
        },
        {
          "timestamp": 1473237120,
          "value": 0.0
        },
        {
          "timestamp": 1473237180,
          "value": 0.0
        },
        {
          "timestamp": 1473237240,
          "value": 0.0
        },
        {
          "timestamp": 1473237300,
          "value": 0.0
        },
        {
          "timestamp": 1473237360,
          "value": 0.0
        },
        {
          "timestamp": 1473237420,
          "value": 0.0
        },
        {
          "timestamp": 1473237480,
          "value": 0.0
        },
        {
          "timestamp": 1473237540,
          "value": 0.0
        },
        {
          "timestamp": 1473237600,
          "value": 0.0
        },
        {
          "timestamp": 1473237660,
          "value": 0.0
        },
        {
          "timestamp": 1473237720,
          "value": 0.0
        },
        {
          "timestamp": 1473237780,
          "value": 0.0
        },
        {
          "timestamp": 1473237840,
          "value": 0.0
        },
        {
          "timestamp": 1473237900,
          "value": 0.0
        },
        {
          "timestamp": 1473237960,
          "value": 0.0
        },
        {
          "timestamp": 1473238020,
          "value": 0.0
        },
        {
          "timestamp": 1473238080,
          "value": 0.0
        },
        {
          "timestamp": 1473238140,
          "value": 0.0
        },
        {
          "timestamp": 1473238200,
          "value": 0.0
        },
        {
          "timestamp": 1473238260,
          "value": 0.0
        },
        {
          "timestamp": 1473238320,
          "value": 0.0
        },
        {
          "timestamp": 1473238380,
          "value": 0.0
        },
        {
          "timestamp": 1473238440,
          "value": null
        },
        {
          "timestamp": 1473238500,
          "value": null
        },
        {
          "timestamp": 1473238560,
          "value": null
        },
        {
          "timestamp": 1473238620,
          "value": null
        },
        {
          "timestamp": 1473238680,
          "value": null
        },
        {
          "timestamp": 1473238740,
          "value": null
        },
        {
          "timestamp": 1473238800,
          "value": 0.0
        },
        {
          "timestamp": 1473238860,
          "value": 0.0
        },
        {
          "timestamp": 1473238920,
          "value": 0.0
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "disk.io.read_bytes/device=sda"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.122.131",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": null
        },
        {
          "timestamp": 1473235500,
          "value": null
        },
        {
          "timestamp": 1473235560,
          "value": 96.413678
        },
        {
          "timestamp": 1473235620,
          "value": null
        },
        {
          "timestamp": 1473235680,
          "value": null
        },
        {
          "timestamp": 1473235740,
          "value": null
        },
        {
          "timestamp": 1473235800,
          "value": null
        },
        {
          "timestamp": 1473235860,
          "value": 95.162636
        },
        {
          "timestamp": 1473235920,
          "value": 95.371143
        },
        {
          "timestamp": 1473235980,
          "value": 96.328744
        },
        {
          "timestamp": 1473236040,
          "value": 96.331805
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": 89.862328
        },
        {
          "timestamp": 1473236520,
          "value": 94.625
        },
        {
          "timestamp": 1473236580,
          "value": 96.118531
        },
        {
          "timestamp": 1473236640,
          "value": 96.118531
        },
        {
          "timestamp": 1473236700,
          "value": 96.285476
        },
        {
          "timestamp": 1473236760,
          "value": 96.080067
        },
        {
          "timestamp": 1473236820,
          "value": 97.332222
        },
        {
          "timestamp": 1473236880,
          "value": 96.623593
        },
        {
          "timestamp": 1473236940,
          "value": 96.331805
        },
        {
          "timestamp": 1473237000,
          "value": 87.996654
        },
        {
          "timestamp": 1473237060,
          "value": 96.617954
        },
        {
          "timestamp": 1473237120,
          "value": 96.123385
        },
        {
          "timestamp": 1473237180,
          "value": 97.998332
        },
        {
          "timestamp": 1473237240,
          "value": 97.496871
        },
        {
          "timestamp": 1473237300,
          "value": 96.953255
        },
        {
          "timestamp": 1473237360,
          "value": 95.494368
        },
        {
          "timestamp": 1473237420,
          "value": 95.371143
        },
        {
          "timestamp": 1473237480,
          "value": 97.039199
        },
        {
          "timestamp": 1473237540,
          "value": 92.940685
        },
        {
          "timestamp": 1473237600,
          "value": 95.869837
        },
        {
          "timestamp": 1473237660,
          "value": 96.540225
        },
        {
          "timestamp": 1473237720,
          "value": 96.822742
        },
        {
          "timestamp": 1473237780,
          "value": 95.283806
        },
        {
          "timestamp": 1473237840,
          "value": 96.872394
        },
        {
          "timestamp": 1473237900,
          "value": 97.20717
        },
        {
          "timestamp": 1473237960,
          "value": 97.1202
        },
        {
          "timestamp": 1473238020,
          "value": 96.787651
        },
        {
          "timestamp": 1473238080,
          "value": null
        },
        {
          "timestamp": 1473238140,
          "value": 97.082118
        },
        {
          "timestamp": 1473238200,
          "value": 96.832013
        },
        {
          "timestamp": 1473238260,
          "value": 97.41559
        },
        {
          "timestamp": 1473238320,
          "value": 96.871089
        },
        {
          "timestamp": 1473238380,
          "value": 97.039199
        },
        {
          "timestamp": 1473238440,
          "value": 96.580484
        },
        {
          "timestamp": 1473238500,
          "value": null
        },
        {
          "timestamp": 1473238560,
          "value": null
        },
        {
          "timestamp": 1473238620,
          "value": null
        },
        {
          "timestamp": 1473238680,
          "value": null
        },
        {
          "timestamp": 1473238740,
          "value": null
        },
        {
          "timestamp": 1473238800,
          "value": 92.58794
        },
        {
          "timestamp": 1473238860,
          "value": 88.657214
        },
        {
          "timestamp": 1473238920,
          "value": 91.075897
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "cpu.idle"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.122.131",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": null
        },
        {
          "timestamp": 1473235500,
          "value": null
        },
        {
          "timestamp": 1473235560,
          "value": 4096.0
        },
        {
          "timestamp": 1473235620,
          "value": null
        },
        {
          "timestamp": 1473235680,
          "value": null
        },
        {
          "timestamp": 1473235740,
          "value": null
        },
        {
          "timestamp": 1473235800,
          "value": null
        },
        {
          "timestamp": 1473235860,
          "value": 4096.0
        },
        {
          "timestamp": 1473235920,
          "value": 24576.0
        },
        {
          "timestamp": 1473235980,
          "value": 77824.0
        },
        {
          "timestamp": 1473236040,
          "value": 24576.0
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": 24576.0
        },
        {
          "timestamp": 1473236520,
          "value": 20480.0
        },
        {
          "timestamp": 1473236580,
          "value": 12288.0
        },
        {
          "timestamp": 1473236640,
          "value": 12288.0
        },
        {
          "timestamp": 1473236700,
          "value": 77824.0
        },
        {
          "timestamp": 1473236760,
          "value": 4096.0
        },
        {
          "timestamp": 1473236820,
          "value": 0.0
        },
        {
          "timestamp": 1473236880,
          "value": 0.0
        },
        {
          "timestamp": 1473236940,
          "value": 0.0
        },
        {
          "timestamp": 1473237000,
          "value": 90112.0
        },
        {
          "timestamp": 1473237060,
          "value": 90112.0
        },
        {
          "timestamp": 1473237120,
          "value": 147456.0
        },
        {
          "timestamp": 1473237180,
          "value": 147456.0
        },
        {
          "timestamp": 1473237240,
          "value": 24576.0
        },
        {
          "timestamp": 1473237300,
          "value": 155648.0
        },
        {
          "timestamp": 1473237360,
          "value": 20480.0
        },
        {
          "timestamp": 1473237420,
          "value": 20480.0
        },
        {
          "timestamp": 1473237480,
          "value": 28672.0
        },
        {
          "timestamp": 1473237540,
          "value": 20480.0
        },
        {
          "timestamp": 1473237600,
          "value": 24576.0
        },
        {
          "timestamp": 1473237660,
          "value": 90112.0
        },
        {
          "timestamp": 1473237720,
          "value": 4096.0
        },
        {
          "timestamp": 1473237780,
          "value": 4096.0
        },
        {
          "timestamp": 1473237840,
          "value": 4096.0
        },
        {
          "timestamp": 1473237900,
          "value": 90112.0
        },
        {
          "timestamp": 1473237960,
          "value": 4096.0
        },
        {
          "timestamp": 1473238020,
          "value": 4096.0
        },
        {
          "timestamp": 1473238080,
          "value": 4096.0
        },
        {
          "timestamp": 1473238140,
          "value": 0.0
        },
        {
          "timestamp": 1473238200,
          "value": 126976.0
        },
        {
          "timestamp": 1473238260,
          "value": 0.0
        },
        {
          "timestamp": 1473238320,
          "value": 0.0
        },
        {
          "timestamp": 1473238380,
          "value": 20480.0
        },
        {
          "timestamp": 1473238440,
          "value": null
        },
        {
          "timestamp": 1473238500,
          "value": null
        },
        {
          "timestamp": 1473238560,
          "value": null
        },
        {
          "timestamp": 1473238620,
          "value": null
        },
        {
          "timestamp": 1473238680,
          "value": null
        },
        {
          "timestamp": 1473238740,
          "value": null
        },
        {
          "timestamp": 1473238800,
          "value": 58650624.0
        },
        {
          "timestamp": 1473238860,
          "value": 147456.0
        },
        {
          "timestamp": 1473238920,
          "value": 4096.0
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "disk.io.write_bytes/device=sda"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.122.133",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": 0.0
        },
        {
          "timestamp": 1473235500,
          "value": 0.0
        },
        {
          "timestamp": 1473235560,
          "value": 0.0
        },
        {
          "timestamp": 1473235620,
          "value": 0.0
        },
        {
          "timestamp": 1473235680,
          "value": 0.0
        },
        {
          "timestamp": 1473235740,
          "value": 0.0
        },
        {
          "timestamp": 1473235800,
          "value": 0.0
        },
        {
          "timestamp": 1473235860,
          "value": 0.0
        },
        {
          "timestamp": 1473235920,
          "value": 0.0
        },
        {
          "timestamp": 1473235980,
          "value": null
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": null
        },
        {
          "timestamp": 1473236520,
          "value": null
        },
        {
          "timestamp": 1473236580,
          "value": null
        },
        {
          "timestamp": 1473236640,
          "value": 0.0
        },
        {
          "timestamp": 1473236700,
          "value": 0.0
        },
        {
          "timestamp": 1473236760,
          "value": 0.0
        },
        {
          "timestamp": 1473236820,
          "value": 0.0
        },
        {
          "timestamp": 1473236880,
          "value": 0.0
        },
        {
          "timestamp": 1473236940,
          "value": 0.0
        },
        {
          "timestamp": 1473237000,
          "value": 0.0
        },
        {
          "timestamp": 1473237060,
          "value": 0.0
        },
        {
          "timestamp": 1473237120,
          "value": 0.0
        },
        {
          "timestamp": 1473237180,
          "value": 0.0
        },
        {
          "timestamp": 1473237240,
          "value": 0.0
        },
        {
          "timestamp": 1473237300,
          "value": 0.0
        },
        {
          "timestamp": 1473237360,
          "value": 0.0
        },
        {
          "timestamp": 1473237420,
          "value": 0.0
        },
        {
          "timestamp": 1473237480,
          "value": 0.0
        },
        {
          "timestamp": 1473237540,
          "value": 0.0
        },
        {
          "timestamp": 1473237600,
          "value": 0.0
        },
        {
          "timestamp": 1473237660,
          "value": 0.0
        },
        {
          "timestamp": 1473237720,
          "value": 0.0
        },
        {
          "timestamp": 1473237780,
          "value": null
        },
        {
          "timestamp": 1473237840,
          "value": 0.0
        },
        {
          "timestamp": 1473237900,
          "value": 0.0
        },
        {
          "timestamp": 1473237960,
          "value": 0.0
        },
        {
          "timestamp": 1473238020,
          "value": 0.0
        },
        {
          "timestamp": 1473238080,
          "value": null
        },
        {
          "timestamp": 1473238140,
          "value": 0.0
        },
        {
          "timestamp": 1473238200,
          "value": 0.0
        },
        {
          "timestamp": 1473238260,
          "value": 0.0
        },
        {
          "timestamp": 1473238320,
          "value": 0.0
        },
        {
          "timestamp": 1473238380,
          "value": 0.0
        },
        {
          "timestamp": 1473238440,
          "value": null
        },
        {
          "timestamp": 1473238500,
          "value": 0.0
        },
        {
          "timestamp": 1473238560,
          "value": 0.0
        },
        {
          "timestamp": 1473238620,
          "value": null
        },
        {
          "timestamp": 1473238680,
          "value": null
        },
        {
          "timestamp": 1473238740,
          "value": null
        },
        {
          "timestamp": 1473238800,
          "value": null
        },
        {
          "timestamp": 1473238860,
          "value": null
        },
        {
          "timestamp": 1473238920,
          "value": null
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "disk.io.read_bytes/device=sda"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.122.133",
      "Values": [
        {
          "timestamp": 1473235440,
          "value": 91.113892
        },
        {
          "timestamp": 1473235500,
          "value": 90.916702
        },
        {
          "timestamp": 1473235560,
          "value": 94.041667
        },
        {
          "timestamp": 1473235620,
          "value": 95.210329
        },
        {
          "timestamp": 1473235680,
          "value": 96.370463
        },
        {
          "timestamp": 1473235740,
          "value": 94.747812
        },
        {
          "timestamp": 1473235800,
          "value": 95.409015
        },
        {
          "timestamp": 1473235860,
          "value": 94.341995
        },
        {
          "timestamp": 1473235920,
          "value": 94.286906
        },
        {
          "timestamp": 1473235980,
          "value": null
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": null
        },
        {
          "timestamp": 1473236520,
          "value": null
        },
        {
          "timestamp": 1473236580,
          "value": null
        },
        {
          "timestamp": 1473236640,
          "value": 94.822547
        },
        {
          "timestamp": 1473236700,
          "value": 94.029228
        },
        {
          "timestamp": 1473236760,
          "value": 94.829024
        },
        {
          "timestamp": 1473236820,
          "value": 94.260578
        },
        {
          "timestamp": 1473236880,
          "value": 94.741235
        },
        {
          "timestamp": 1473236940,
          "value": 94.370309
        },
        {
          "timestamp": 1473237000,
          "value": 85.157233
        },
        {
          "timestamp": 1473237060,
          "value": 94.284522
        },
        {
          "timestamp": 1473237120,
          "value": 93.502707
        },
        {
          "timestamp": 1473237180,
          "value": 96.410684
        },
        {
          "timestamp": 1473237240,
          "value": 95.702962
        },
        {
          "timestamp": 1473237300,
          "value": 94.745621
        },
        {
          "timestamp": 1473237360,
          "value": 95.075125
        },
        {
          "timestamp": 1473237420,
          "value": 91.102757
        },
        {
          "timestamp": 1473237480,
          "value": 93.820459
        },
        {
          "timestamp": 1473237540,
          "value": 94.41201
        },
        {
          "timestamp": 1473237600,
          "value": 95.208333
        },
        {
          "timestamp": 1473237660,
          "value": 95.11074
        },
        {
          "timestamp": 1473237720,
          "value": 94.402673
        },
        {
          "timestamp": 1473237780,
          "value": 95.498124
        },
        {
          "timestamp": 1473237840,
          "value": 94.495413
        },
        {
          "timestamp": 1473237900,
          "value": 94.54394
        },
        {
          "timestamp": 1473237960,
          "value": 93.742178
        },
        {
          "timestamp": 1473238020,
          "value": 94.785148
        },
        {
          "timestamp": 1473238080,
          "value": 96.076795
        },
        {
          "timestamp": 1473238140,
          "value": 94.407346
        },
        {
          "timestamp": 1473238200,
          "value": 92.56785
        },
        {
          "timestamp": 1473238260,
          "value": 94.983278
        },
        {
          "timestamp": 1473238320,
          "value": 93.53628
        },
        {
          "timestamp": 1473238380,
          "value": 95.150502
        },
        {
          "timestamp": 1473238440,
          "value": 91.740788
        },
        {
          "timestamp": 1473238500,
          "value": 91.740788
        },
        {
          "timestamp": 1473238560,
          "value": 94.991653
        },
        {
          "timestamp": 1473238620,
          "value": null
        },
        {
          "timestamp": 1473238680,
          "value": null
        },
        {
          "timestamp": 1473238740,
          "value": null
        },
        {
          "timestamp": 1473238800,
          "value": null
        },
        {
          "timestamp": 1473238860,
          "value": null
        },
        {
          "timestamp": 1473238920,
          "value": null
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "cpu.idle"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.122.133",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": 135168.0
        },
        {
          "timestamp": 1473235500,
          "value": 65536.0
        },
        {
          "timestamp": 1473235560,
          "value": 61440.0
        },
        {
          "timestamp": 1473235620,
          "value": 53248.0
        },
        {
          "timestamp": 1473235680,
          "value": 151552.0
        },
        {
          "timestamp": 1473235740,
          "value": 53248.0
        },
        {
          "timestamp": 1473235800,
          "value": 53248.0
        },
        {
          "timestamp": 1473235860,
          "value": 0.0
        },
        {
          "timestamp": 1473235920,
          "value": 65536.0
        },
        {
          "timestamp": 1473235980,
          "value": null
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": null
        },
        {
          "timestamp": 1473236520,
          "value": null
        },
        {
          "timestamp": 1473236580,
          "value": null
        },
        {
          "timestamp": 1473236640,
          "value": 49152.0
        },
        {
          "timestamp": 1473236700,
          "value": 0.0
        },
        {
          "timestamp": 1473236760,
          "value": 57344.0
        },
        {
          "timestamp": 1473236820,
          "value": 53248.0
        },
        {
          "timestamp": 1473236880,
          "value": 57344.0
        },
        {
          "timestamp": 1473236940,
          "value": 61440.0
        },
        {
          "timestamp": 1473237000,
          "value": 0.0
        },
        {
          "timestamp": 1473237060,
          "value": 0.0
        },
        {
          "timestamp": 1473237120,
          "value": 57344.0
        },
        {
          "timestamp": 1473237180,
          "value": 53248.0
        },
        {
          "timestamp": 1473237240,
          "value": 53248.0
        },
        {
          "timestamp": 1473237300,
          "value": 53248.0
        },
        {
          "timestamp": 1473237360,
          "value": 57344.0
        },
        {
          "timestamp": 1473237420,
          "value": 53248.0
        },
        {
          "timestamp": 1473237480,
          "value": 49152.0
        },
        {
          "timestamp": 1473237540,
          "value": 53248.0
        },
        {
          "timestamp": 1473237600,
          "value": 65536.0
        },
        {
          "timestamp": 1473237660,
          "value": 53248.0
        },
        {
          "timestamp": 1473237720,
          "value": 61440.0
        },
        {
          "timestamp": 1473237780,
          "value": 61440.0
        },
        {
          "timestamp": 1473237840,
          "value": 61440.0
        },
        {
          "timestamp": 1473237900,
          "value": 57344.0
        },
        {
          "timestamp": 1473237960,
          "value": 53248.0
        },
        {
          "timestamp": 1473238020,
          "value": 57344.0
        },
        {
          "timestamp": 1473238080,
          "value": null
        },
        {
          "timestamp": 1473238140,
          "value": 12288.0
        },
        {
          "timestamp": 1473238200,
          "value": 111071232.0
        },
        {
          "timestamp": 1473238260,
          "value": 106311680.0
        },
        {
          "timestamp": 1473238320,
          "value": 106192896.0
        },
        {
          "timestamp": 1473238380,
          "value": 105930752.0
        },
        {
          "timestamp": 1473238440,
          "value": null
        },
        {
          "timestamp": 1473238500,
          "value": 28672.0
        },
        {
          "timestamp": 1473238560,
          "value": 106020864.0
        },
        {
          "timestamp": 1473238620,
          "value": null
        },
        {
          "timestamp": 1473238680,
          "value": null
        },
        {
          "timestamp": 1473238740,
          "value": null
        },
        {
          "timestamp": 1473238800,
          "value": null
        },
        {
          "timestamp": 1473238860,
          "value": null
        },
        {
          "timestamp": 1473238920,
          "value": null
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "disk.io.write_bytes/device=sda"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.122.66",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": 0.0
        },
        {
          "timestamp": 1473235500,
          "value": null
        },
        {
          "timestamp": 1473235560,
          "value": null
        },
        {
          "timestamp": 1473235620,
          "value": null
        },
        {
          "timestamp": 1473235680,
          "value": null
        },
        {
          "timestamp": 1473235740,
          "value": null
        },
        {
          "timestamp": 1473235800,
          "value": null
        },
        {
          "timestamp": 1473235860,
          "value": null
        },
        {
          "timestamp": 1473235920,
          "value": null
        },
        {
          "timestamp": 1473235980,
          "value": null
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": null
        },
        {
          "timestamp": 1473236520,
          "value": null
        },
        {
          "timestamp": 1473236580,
          "value": 0.0
        },
        {
          "timestamp": 1473236640,
          "value": 0.0
        },
        {
          "timestamp": 1473236700,
          "value": 0.0
        },
        {
          "timestamp": 1473236760,
          "value": 0.0
        },
        {
          "timestamp": 1473236820,
          "value": 0.0
        },
        {
          "timestamp": 1473236880,
          "value": 0.0
        },
        {
          "timestamp": 1473236940,
          "value": 0.0
        },
        {
          "timestamp": 1473237000,
          "value": 0.0
        },
        {
          "timestamp": 1473237060,
          "value": 0.0
        },
        {
          "timestamp": 1473237120,
          "value": 0.0
        },
        {
          "timestamp": 1473237180,
          "value": 0.0
        },
        {
          "timestamp": 1473237240,
          "value": 0.0
        },
        {
          "timestamp": 1473237300,
          "value": 0.0
        },
        {
          "timestamp": 1473237360,
          "value": 0.0
        },
        {
          "timestamp": 1473237420,
          "value": 0.0
        },
        {
          "timestamp": 1473237480,
          "value": 0.0
        },
        {
          "timestamp": 1473237540,
          "value": 0.0
        },
        {
          "timestamp": 1473237600,
          "value": 0.0
        },
        {
          "timestamp": 1473237660,
          "value": 0.0
        },
        {
          "timestamp": 1473237720,
          "value": 0.0
        },
        {
          "timestamp": 1473237780,
          "value": 0.0
        },
        {
          "timestamp": 1473237840,
          "value": 0.0
        },
        {
          "timestamp": 1473237900,
          "value": 0.0
        },
        {
          "timestamp": 1473237960,
          "value": 0.0
        },
        {
          "timestamp": 1473238020,
          "value": 0.0
        },
        {
          "timestamp": 1473238080,
          "value": 0.0
        },
        {
          "timestamp": 1473238140,
          "value": 0.0
        },
        {
          "timestamp": 1473238200,
          "value": 0.0
        },
        {
          "timestamp": 1473238260,
          "value": 0.0
        },
        {
          "timestamp": 1473238320,
          "value": 0.0
        },
        {
          "timestamp": 1473238380,
          "value": 0.0
        },
        {
          "timestamp": 1473238440,
          "value": 0.0
        },
        {
          "timestamp": 1473238500,
          "value": 0.0
        },
        {
          "timestamp": 1473238560,
          "value": null
        },
        {
          "timestamp": 1473238620,
          "value": 0.0
        },
        {
          "timestamp": 1473238680,
          "value": 0.0
        },
        {
          "timestamp": 1473238740,
          "value": 0.0
        },
        {
          "timestamp": 1473238800,
          "value": 0.0
        },
        {
          "timestamp": 1473238860,
          "value": 0.0
        },
        {
          "timestamp": 1473238920,
          "value": 0.0
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "disk.io.read_bytes/device=sda"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.122.66",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": 97.706422
        },
        {
          "timestamp": 1473235500,
          "value": null
        },
        {
          "timestamp": 1473235560,
          "value": null
        },
        {
          "timestamp": 1473235620,
          "value": null
        },
        {
          "timestamp": 1473235680,
          "value": null
        },
        {
          "timestamp": 1473235740,
          "value": null
        },
        {
          "timestamp": 1473235800,
          "value": null
        },
        {
          "timestamp": 1473235860,
          "value": null
        },
        {
          "timestamp": 1473235920,
          "value": null
        },
        {
          "timestamp": 1473235980,
          "value": null
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": null
        },
        {
          "timestamp": 1473236520,
          "value": null
        },
        {
          "timestamp": 1473236580,
          "value": 97.581318
        },
        {
          "timestamp": 1473236640,
          "value": 97.581318
        },
        {
          "timestamp": 1473236700,
          "value": 97.574237
        },
        {
          "timestamp": 1473236760,
          "value": 97.497915
        },
        {
          "timestamp": 1473236820,
          "value": 97.744361
        },
        {
          "timestamp": 1473236880,
          "value": 97.495826
        },
        {
          "timestamp": 1473236940,
          "value": 97.831526
        },
        {
          "timestamp": 1473237000,
          "value": 89.409795
        },
        {
          "timestamp": 1473237060,
          "value": 97.235023
        },
        {
          "timestamp": 1473237120,
          "value": 97.790746
        },
        {
          "timestamp": 1473237180,
          "value": 97.495826
        },
        {
          "timestamp": 1473237240,
          "value": 97.75
        },
        {
          "timestamp": 1473237300,
          "value": 97.948074
        },
        {
          "timestamp": 1473237360,
          "value": 97.664721
        },
        {
          "timestamp": 1473237420,
          "value": 97.322176
        },
        {
          "timestamp": 1473237480,
          "value": 97.457274
        },
        {
          "timestamp": 1473237540,
          "value": 97.904443
        },
        {
          "timestamp": 1473237600,
          "value": 97.663746
        },
        {
          "timestamp": 1473237660,
          "value": 96.818753
        },
        {
          "timestamp": 1473237720,
          "value": 98.038397
        },
        {
          "timestamp": 1473237780,
          "value": 95.268007
        },
        {
          "timestamp": 1473237840,
          "value": 97.541667
        },
        {
          "timestamp": 1473237900,
          "value": 97.696817
        },
        {
          "timestamp": 1473237960,
          "value": 97.706422
        },
        {
          "timestamp": 1473238020,
          "value": 97.623019
        },
        {
          "timestamp": 1473238080,
          "value": 97.912317
        },
        {
          "timestamp": 1473238140,
          "value": 97.706422
        },
        {
          "timestamp": 1473238200,
          "value": 97.706422
        },
        {
          "timestamp": 1473238260,
          "value": 97.276917
        },
        {
          "timestamp": 1473238320,
          "value": 97.459392
        },
        {
          "timestamp": 1473238380,
          "value": 97.696817
        },
        {
          "timestamp": 1473238440,
          "value": 97.665694
        },
        {
          "timestamp": 1473238500,
          "value": 97.068677
        },
        {
          "timestamp": 1473238560,
          "value": null
        },
        {
          "timestamp": 1473238620,
          "value": 97.705465
        },
        {
          "timestamp": 1473238680,
          "value": 97.914929
        },
        {
          "timestamp": 1473238740,
          "value": 96.573339
        },
        {
          "timestamp": 1473238800,
          "value": 93.891213
        },
        {
          "timestamp": 1473238860,
          "value": 93.859649
        },
        {
          "timestamp": 1473238920,
          "value": 93.789079
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "cpu.idle"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.122.66",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": 0.0
        },
        {
          "timestamp": 1473235500,
          "value": null
        },
        {
          "timestamp": 1473235560,
          "value": null
        },
        {
          "timestamp": 1473235620,
          "value": null
        },
        {
          "timestamp": 1473235680,
          "value": null
        },
        {
          "timestamp": 1473235740,
          "value": null
        },
        {
          "timestamp": 1473235800,
          "value": null
        },
        {
          "timestamp": 1473235860,
          "value": null
        },
        {
          "timestamp": 1473235920,
          "value": null
        },
        {
          "timestamp": 1473235980,
          "value": null
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": null
        },
        {
          "timestamp": 1473236520,
          "value": null
        },
        {
          "timestamp": 1473236580,
          "value": 61440.0
        },
        {
          "timestamp": 1473236640,
          "value": 61440.0
        },
        {
          "timestamp": 1473236700,
          "value": 0.0
        },
        {
          "timestamp": 1473236760,
          "value": 0.0
        },
        {
          "timestamp": 1473236820,
          "value": 0.0
        },
        {
          "timestamp": 1473236880,
          "value": 0.0
        },
        {
          "timestamp": 1473236940,
          "value": 0.0
        },
        {
          "timestamp": 1473237000,
          "value": 0.0
        },
        {
          "timestamp": 1473237060,
          "value": 0.0
        },
        {
          "timestamp": 1473237120,
          "value": 0.0
        },
        {
          "timestamp": 1473237180,
          "value": 0.0
        },
        {
          "timestamp": 1473237240,
          "value": 0.0
        },
        {
          "timestamp": 1473237300,
          "value": 73728.0
        },
        {
          "timestamp": 1473237360,
          "value": 73728.0
        },
        {
          "timestamp": 1473237420,
          "value": 73728.0
        },
        {
          "timestamp": 1473237480,
          "value": 0.0
        },
        {
          "timestamp": 1473237540,
          "value": 0.0
        },
        {
          "timestamp": 1473237600,
          "value": 0.0
        },
        {
          "timestamp": 1473237660,
          "value": 94208.0
        },
        {
          "timestamp": 1473237720,
          "value": 0.0
        },
        {
          "timestamp": 1473237780,
          "value": 0.0
        },
        {
          "timestamp": 1473237840,
          "value": 0.0
        },
        {
          "timestamp": 1473237900,
          "value": 0.0
        },
        {
          "timestamp": 1473237960,
          "value": 0.0
        },
        {
          "timestamp": 1473238020,
          "value": 94208.0
        },
        {
          "timestamp": 1473238080,
          "value": 94208.0
        },
        {
          "timestamp": 1473238140,
          "value": 0.0
        },
        {
          "timestamp": 1473238200,
          "value": 0.0
        },
        {
          "timestamp": 1473238260,
          "value": 0.0
        },
        {
          "timestamp": 1473238320,
          "value": 0.0
        },
        {
          "timestamp": 1473238380,
          "value": 0.0
        },
        {
          "timestamp": 1473238440,
          "value": 0.0
        },
        {
          "timestamp": 1473238500,
          "value": 0.0
        },
        {
          "timestamp": 1473238560,
          "value": 49152.0
        },
        {
          "timestamp": 1473238620,
          "value": 49152.0
        },
        {
          "timestamp": 1473238680,
          "value": 0.0
        },
        {
          "timestamp": 1473238740,
          "value": 0.0
        },
        {
          "timestamp": 1473238800,
          "value": 0.0
        },
        {
          "timestamp": 1473238860,
          "value": 0.0
        },
        {
          "timestamp": 1473238920,
          "value": 0.0
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "disk.io.write_bytes/device=sda"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.122.67",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": null
        },
        {
          "timestamp": 1473235500,
          "value": null
        },
        {
          "timestamp": 1473235560,
          "value": null
        },
        {
          "timestamp": 1473235620,
          "value": null
        },
        {
          "timestamp": 1473235680,
          "value": null
        },
        {
          "timestamp": 1473235740,
          "value": null
        },
        {
          "timestamp": 1473235800,
          "value": null
        },
        {
          "timestamp": 1473235860,
          "value": null
        },
        {
          "timestamp": 1473235920,
          "value": null
        },
        {
          "timestamp": 1473235980,
          "value": null
        },
        {
          "timestamp": 1473236040,
          "value": 0.0
        },
        {
          "timestamp": 1473236100,
          "value": 0.0
        },
        {
          "timestamp": 1473236160,
          "value": 0.0
        },
        {
          "timestamp": 1473236220,
          "value": 0.0
        },
        {
          "timestamp": 1473236280,
          "value": 0.0
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": null
        },
        {
          "timestamp": 1473236520,
          "value": null
        },
        {
          "timestamp": 1473236580,
          "value": null
        },
        {
          "timestamp": 1473236640,
          "value": null
        },
        {
          "timestamp": 1473236700,
          "value": 0.0
        },
        {
          "timestamp": 1473236760,
          "value": 0.0
        },
        {
          "timestamp": 1473236820,
          "value": 0.0
        },
        {
          "timestamp": 1473236880,
          "value": 0.0
        },
        {
          "timestamp": 1473236940,
          "value": 0.0
        },
        {
          "timestamp": 1473237000,
          "value": 0.0
        },
        {
          "timestamp": 1473237060,
          "value": 0.0
        },
        {
          "timestamp": 1473237120,
          "value": 0.0
        },
        {
          "timestamp": 1473237180,
          "value": 0.0
        },
        {
          "timestamp": 1473237240,
          "value": 0.0
        },
        {
          "timestamp": 1473237300,
          "value": 0.0
        },
        {
          "timestamp": 1473237360,
          "value": 0.0
        },
        {
          "timestamp": 1473237420,
          "value": 0.0
        },
        {
          "timestamp": 1473237480,
          "value": 0.0
        },
        {
          "timestamp": 1473237540,
          "value": 0.0
        },
        {
          "timestamp": 1473237600,
          "value": 0.0
        },
        {
          "timestamp": 1473237660,
          "value": 0.0
        },
        {
          "timestamp": 1473237720,
          "value": 0.0
        },
        {
          "timestamp": 1473237780,
          "value": 0.0
        },
        {
          "timestamp": 1473237840,
          "value": 0.0
        },
        {
          "timestamp": 1473237900,
          "value": 0.0
        },
        {
          "timestamp": 1473237960,
          "value": 0.0
        },
        {
          "timestamp": 1473238020,
          "value": 0.0
        },
        {
          "timestamp": 1473238080,
          "value": 0.0
        },
        {
          "timestamp": 1473238140,
          "value": 0.0
        },
        {
          "timestamp": 1473238200,
          "value": 0.0
        },
        {
          "timestamp": 1473238260,
          "value": 0.0
        },
        {
          "timestamp": 1473238320,
          "value": 0.0
        },
        {
          "timestamp": 1473238380,
          "value": 0.0
        },
        {
          "timestamp": 1473238440,
          "value": 0.0
        },
        {
          "timestamp": 1473238500,
          "value": 0.0
        },
        {
          "timestamp": 1473238560,
          "value": 0.0
        },
        {
          "timestamp": 1473238620,
          "value": 0.0
        },
        {
          "timestamp": 1473238680,
          "value": 0.0
        },
        {
          "timestamp": 1473238740,
          "value": 0.0
        },
        {
          "timestamp": 1473238800,
          "value": null
        },
        {
          "timestamp": 1473238860,
          "value": null
        },
        {
          "timestamp": 1473238920,
          "value": null
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "disk.io.read_bytes/device=sda"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.122.67",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": null
        },
        {
          "timestamp": 1473235500,
          "value": null
        },
        {
          "timestamp": 1473235560,
          "value": null
        },
        {
          "timestamp": 1473235620,
          "value": null
        },
        {
          "timestamp": 1473235680,
          "value": null
        },
        {
          "timestamp": 1473235740,
          "value": null
        },
        {
          "timestamp": 1473235800,
          "value": null
        },
        {
          "timestamp": 1473235860,
          "value": null
        },
        {
          "timestamp": 1473235920,
          "value": null
        },
        {
          "timestamp": 1473235980,
          "value": null
        },
        {
          "timestamp": 1473236040,
          "value": 96.16347
        },
        {
          "timestamp": 1473236100,
          "value": 96.958333
        },
        {
          "timestamp": 1473236160,
          "value": 96.452421
        },
        {
          "timestamp": 1473236220,
          "value": 95.90985
        },
        {
          "timestamp": 1473236280,
          "value": 95.57596
        },
        {
          "timestamp": 1473236340,
          "value": 96.121768
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": null
        },
        {
          "timestamp": 1473236520,
          "value": null
        },
        {
          "timestamp": 1473236580,
          "value": null
        },
        {
          "timestamp": 1473236640,
          "value": null
        },
        {
          "timestamp": 1473236700,
          "value": 95.409015
        },
        {
          "timestamp": 1473236760,
          "value": 94.620517
        },
        {
          "timestamp": 1473236820,
          "value": 95.075125
        },
        {
          "timestamp": 1473236880,
          "value": 96.24374
        },
        {
          "timestamp": 1473236940,
          "value": 96.245307
        },
        {
          "timestamp": 1473237000,
          "value": 84.309623
        },
        {
          "timestamp": 1473237060,
          "value": 94.989562
        },
        {
          "timestamp": 1473237120,
          "value": 95.994994
        },
        {
          "timestamp": 1473237180,
          "value": 95.710121
        },
        {
          "timestamp": 1473237240,
          "value": 96.658312
        },
        {
          "timestamp": 1473237300,
          "value": 96.577629
        },
        {
          "timestamp": 1473237360,
          "value": 96.449457
        },
        {
          "timestamp": 1473237420,
          "value": 96.453901
        },
        {
          "timestamp": 1473237480,
          "value": 96.288574
        },
        {
          "timestamp": 1473237540,
          "value": 97.0
        },
        {
          "timestamp": 1473237600,
          "value": 97.36952
        },
        {
          "timestamp": 1473237660,
          "value": 96.367432
        },
        {
          "timestamp": 1473237720,
          "value": 95.367279
        },
        {
          "timestamp": 1473237780,
          "value": 96.453901
        },
        {
          "timestamp": 1473237840,
          "value": 96.208333
        },
        {
          "timestamp": 1473237900,
          "value": 96.9596
        },
        {
          "timestamp": 1473237960,
          "value": 93.736952
        },
        {
          "timestamp": 1473238020,
          "value": 94.03172
        },
        {
          "timestamp": 1473238080,
          "value": null
        },
        {
          "timestamp": 1473238140,
          "value": 96.663887
        },
        {
          "timestamp": 1473238200,
          "value": 94.708333
        },
        {
          "timestamp": 1473238260,
          "value": 96.494157
        },
        {
          "timestamp": 1473238320,
          "value": 96.452421
        },
        {
          "timestamp": 1473238380,
          "value": 94.743429
        },
        {
          "timestamp": 1473238440,
          "value": 94.321503
        },
        {
          "timestamp": 1473238500,
          "value": 96.456857
        },
        {
          "timestamp": 1473238560,
          "value": 96.700084
        },
        {
          "timestamp": 1473238620,
          "value": 96.783626
        },
        {
          "timestamp": 1473238680,
          "value": 94.725738
        },
        {
          "timestamp": 1473238740,
          "value": 95.619524
        },
        {
          "timestamp": 1473238800,
          "value": null
        },
        {
          "timestamp": 1473238860,
          "value": null
        },
        {
          "timestamp": 1473238920,
          "value": null
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "cpu.idle"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.122.67",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": null
        },
        {
          "timestamp": 1473235500,
          "value": null
        },
        {
          "timestamp": 1473235560,
          "value": null
        },
        {
          "timestamp": 1473235620,
          "value": null
        },
        {
          "timestamp": 1473235680,
          "value": null
        },
        {
          "timestamp": 1473235740,
          "value": null
        },
        {
          "timestamp": 1473235800,
          "value": null
        },
        {
          "timestamp": 1473235860,
          "value": null
        },
        {
          "timestamp": 1473235920,
          "value": null
        },
        {
          "timestamp": 1473235980,
          "value": null
        },
        {
          "timestamp": 1473236040,
          "value": 4096.0
        },
        {
          "timestamp": 1473236100,
          "value": 8192.0
        },
        {
          "timestamp": 1473236160,
          "value": 8192.0
        },
        {
          "timestamp": 1473236220,
          "value": 4096.0
        },
        {
          "timestamp": 1473236280,
          "value": 4096.0
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": null
        },
        {
          "timestamp": 1473236520,
          "value": null
        },
        {
          "timestamp": 1473236580,
          "value": null
        },
        {
          "timestamp": 1473236640,
          "value": null
        },
        {
          "timestamp": 1473236700,
          "value": 4096.0
        },
        {
          "timestamp": 1473236760,
          "value": 8192.0
        },
        {
          "timestamp": 1473236820,
          "value": 8192.0
        },
        {
          "timestamp": 1473236880,
          "value": 0.0
        },
        {
          "timestamp": 1473236940,
          "value": 32768.0
        },
        {
          "timestamp": 1473237000,
          "value": 0.0
        },
        {
          "timestamp": 1473237060,
          "value": 4096.0
        },
        {
          "timestamp": 1473237120,
          "value": 81920.0
        },
        {
          "timestamp": 1473237180,
          "value": 4096.0
        },
        {
          "timestamp": 1473237240,
          "value": 0.0
        },
        {
          "timestamp": 1473237300,
          "value": 176128.0
        },
        {
          "timestamp": 1473237360,
          "value": 176128.0
        },
        {
          "timestamp": 1473237420,
          "value": 57344.0
        },
        {
          "timestamp": 1473237480,
          "value": 20480.0
        },
        {
          "timestamp": 1473237540,
          "value": 65536.0
        },
        {
          "timestamp": 1473237600,
          "value": 286720.0
        },
        {
          "timestamp": 1473237660,
          "value": 28672.0
        },
        {
          "timestamp": 1473237720,
          "value": 4096.0
        },
        {
          "timestamp": 1473237780,
          "value": 131072.0
        },
        {
          "timestamp": 1473237840,
          "value": 4096.0
        },
        {
          "timestamp": 1473237900,
          "value": 4096.0
        },
        {
          "timestamp": 1473237960,
          "value": 4096.0
        },
        {
          "timestamp": 1473238020,
          "value": 4096.0
        },
        {
          "timestamp": 1473238080,
          "value": null
        },
        {
          "timestamp": 1473238140,
          "value": 176128.0
        },
        {
          "timestamp": 1473238200,
          "value": 135168.0
        },
        {
          "timestamp": 1473238260,
          "value": 0.0
        },
        {
          "timestamp": 1473238320,
          "value": 135168.0
        },
        {
          "timestamp": 1473238380,
          "value": 4096.0
        },
        {
          "timestamp": 1473238440,
          "value": 8192.0
        },
        {
          "timestamp": 1473238500,
          "value": 4096.0
        },
        {
          "timestamp": 1473238560,
          "value": 40960.0
        },
        {
          "timestamp": 1473238620,
          "value": 0.0
        },
        {
          "timestamp": 1473238680,
          "value": 32768.0
        },
        {
          "timestamp": 1473238740,
          "value": 151552.0
        },
        {
          "timestamp": 1473238800,
          "value": null
        },
        {
          "timestamp": 1473238860,
          "value": null
        },
        {
          "timestamp": 1473238920,
          "value": null
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "disk.io.write_bytes/device=sda"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.122.68",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": 0.0
        },
        {
          "timestamp": 1473235500,
          "value": 0.0
        },
        {
          "timestamp": 1473235560,
          "value": 0.0
        },
        {
          "timestamp": 1473235620,
          "value": null
        },
        {
          "timestamp": 1473235680,
          "value": null
        },
        {
          "timestamp": 1473235740,
          "value": null
        },
        {
          "timestamp": 1473235800,
          "value": 0.0
        },
        {
          "timestamp": 1473235860,
          "value": 0.0
        },
        {
          "timestamp": 1473235920,
          "value": null
        },
        {
          "timestamp": 1473235980,
          "value": null
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": null
        },
        {
          "timestamp": 1473236520,
          "value": null
        },
        {
          "timestamp": 1473236580,
          "value": null
        },
        {
          "timestamp": 1473236640,
          "value": 0.0
        },
        {
          "timestamp": 1473236700,
          "value": 0.0
        },
        {
          "timestamp": 1473236760,
          "value": 0.0
        },
        {
          "timestamp": 1473236820,
          "value": 0.0
        },
        {
          "timestamp": 1473236880,
          "value": 0.0
        },
        {
          "timestamp": 1473236940,
          "value": 0.0
        },
        {
          "timestamp": 1473237000,
          "value": 0.0
        },
        {
          "timestamp": 1473237060,
          "value": 0.0
        },
        {
          "timestamp": 1473237120,
          "value": 0.0
        },
        {
          "timestamp": 1473237180,
          "value": 0.0
        },
        {
          "timestamp": 1473237240,
          "value": 0.0
        },
        {
          "timestamp": 1473237300,
          "value": 0.0
        },
        {
          "timestamp": 1473237360,
          "value": 0.0
        },
        {
          "timestamp": 1473237420,
          "value": 0.0
        },
        {
          "timestamp": 1473237480,
          "value": 0.0
        },
        {
          "timestamp": 1473237540,
          "value": 0.0
        },
        {
          "timestamp": 1473237600,
          "value": 0.0
        },
        {
          "timestamp": 1473237660,
          "value": 0.0
        },
        {
          "timestamp": 1473237720,
          "value": 0.0
        },
        {
          "timestamp": 1473237780,
          "value": 0.0
        },
        {
          "timestamp": 1473237840,
          "value": 0.0
        },
        {
          "timestamp": 1473237900,
          "value": 0.0
        },
        {
          "timestamp": 1473237960,
          "value": 0.0
        },
        {
          "timestamp": 1473238020,
          "value": 4096.0
        },
        {
          "timestamp": 1473238080,
          "value": 4096.0
        },
        {
          "timestamp": 1473238140,
          "value": 0.0
        },
        {
          "timestamp": 1473238200,
          "value": 8192.0
        },
        {
          "timestamp": 1473238260,
          "value": 4096.0
        },
        {
          "timestamp": 1473238320,
          "value": 0.0
        },
        {
          "timestamp": 1473238380,
          "value": null
        },
        {
          "timestamp": 1473238440,
          "value": 4096.0
        },
        {
          "timestamp": 1473238500,
          "value": null
        },
        {
          "timestamp": 1473238560,
          "value": 0.0
        },
        {
          "timestamp": 1473238620,
          "value": 0.0
        },
        {
          "timestamp": 1473238680,
          "value": null
        },
        {
          "timestamp": 1473238740,
          "value": null
        },
        {
          "timestamp": 1473238800,
          "value": null
        },
        {
          "timestamp": 1473238860,
          "value": null
        },
        {
          "timestamp": 1473238920,
          "value": null
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "disk.io.read_bytes/device=sda"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.122.68",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": 90.15436
        },
        {
          "timestamp": 1473235500,
          "value": 91.405924
        },
        {
          "timestamp": 1473235560,
          "value": 90.125
        },
        {
          "timestamp": 1473235620,
          "value": null
        },
        {
          "timestamp": 1473235680,
          "value": null
        },
        {
          "timestamp": 1473235740,
          "value": null
        },
        {
          "timestamp": 1473235800,
          "value": 94.912427
        },
        {
          "timestamp": 1473235860,
          "value": 96.075157
        },
        {
          "timestamp": 1473235920,
          "value": null
        },
        {
          "timestamp": 1473235980,
          "value": null
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": null
        },
        {
          "timestamp": 1473236520,
          "value": null
        },
        {
          "timestamp": 1473236580,
          "value": 95.828118
        },
        {
          "timestamp": 1473236640,
          "value": 95.829858
        },
        {
          "timestamp": 1473236700,
          "value": 96.541667
        },
        {
          "timestamp": 1473236760,
          "value": 96.24374
        },
        {
          "timestamp": 1473236820,
          "value": 96.121768
        },
        {
          "timestamp": 1473236880,
          "value": 96.498541
        },
        {
          "timestamp": 1473236940,
          "value": 94.83118
        },
        {
          "timestamp": 1473237000,
          "value": 87.526162
        },
        {
          "timestamp": 1473237060,
          "value": 95.791667
        },
        {
          "timestamp": 1473237120,
          "value": 95.829858
        },
        {
          "timestamp": 1473237180,
          "value": 96.702838
        },
        {
          "timestamp": 1473237240,
          "value": 93.533584
        },
        {
          "timestamp": 1473237300,
          "value": 95.75
        },
        {
          "timestamp": 1473237360,
          "value": 96.617954
        },
        {
          "timestamp": 1473237420,
          "value": 94.655532
        },
        {
          "timestamp": 1473237480,
          "value": 96.12015
        },
        {
          "timestamp": 1473237540,
          "value": 95.913261
        },
        {
          "timestamp": 1473237600,
          "value": 96.078431
        },
        {
          "timestamp": 1473237660,
          "value": 96.036713
        },
        {
          "timestamp": 1473237720,
          "value": 95.710121
        },
        {
          "timestamp": 1473237780,
          "value": 94.870726
        },
        {
          "timestamp": 1473237840,
          "value": 94.666667
        },
        {
          "timestamp": 1473237900,
          "value": 95.993322
        },
        {
          "timestamp": 1473237960,
          "value": 96.617954
        },
        {
          "timestamp": 1473238020,
          "value": 95.414756
        },
        {
          "timestamp": 1473238080,
          "value": 94.618273
        },
        {
          "timestamp": 1473238140,
          "value": 95.19833
        },
        {
          "timestamp": 1473238200,
          "value": 95.824635
        },
        {
          "timestamp": 1473238260,
          "value": 96.5762
        },
        {
          "timestamp": 1473238320,
          "value": 96.206753
        },
        {
          "timestamp": 1473238380,
          "value": null
        },
        {
          "timestamp": 1473238440,
          "value": 93.502707
        },
        {
          "timestamp": 1473238500,
          "value": null
        },
        {
          "timestamp": 1473238560,
          "value": 95.236105
        },
        {
          "timestamp": 1473238620,
          "value": 95.5
        },
        {
          "timestamp": 1473238680,
          "value": null
        },
        {
          "timestamp": 1473238740,
          "value": null
        },
        {
          "timestamp": 1473238800,
          "value": null
        },
        {
          "timestamp": 1473238860,
          "value": null
        },
        {
          "timestamp": 1473238920,
          "value": null
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "cpu.idle"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.122.68",
      "Values": [
        {
          "timestamp": 1473235440,
          "value": 49152.0
        },
        {
          "timestamp": 1473235500,
          "value": 53248.0
        },
        {
          "timestamp": 1473235560,
          "value": 53248.0
        },
        {
          "timestamp": 1473235620,
          "value": null
        },
        {
          "timestamp": 1473235680,
          "value": null
        },
        {
          "timestamp": 1473235740,
          "value": null
        },
        {
          "timestamp": 1473235800,
          "value": 0.0
        },
        {
          "timestamp": 1473235860,
          "value": 0.0
        },
        {
          "timestamp": 1473235920,
          "value": null
        },
        {
          "timestamp": 1473235980,
          "value": null
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": null
        },
        {
          "timestamp": 1473236520,
          "value": null
        },
        {
          "timestamp": 1473236580,
          "value": null
        },
        {
          "timestamp": 1473236640,
          "value": 0.0
        },
        {
          "timestamp": 1473236700,
          "value": 0.0
        },
        {
          "timestamp": 1473236760,
          "value": 0.0
        },
        {
          "timestamp": 1473236820,
          "value": 110592.0
        },
        {
          "timestamp": 1473236880,
          "value": 0.0
        },
        {
          "timestamp": 1473236940,
          "value": 0.0
        },
        {
          "timestamp": 1473237000,
          "value": 0.0
        },
        {
          "timestamp": 1473237060,
          "value": 0.0
        },
        {
          "timestamp": 1473237120,
          "value": 0.0
        },
        {
          "timestamp": 1473237180,
          "value": 0.0
        },
        {
          "timestamp": 1473237240,
          "value": 0.0
        },
        {
          "timestamp": 1473237300,
          "value": 86016.0
        },
        {
          "timestamp": 1473237360,
          "value": 0.0
        },
        {
          "timestamp": 1473237420,
          "value": 0.0
        },
        {
          "timestamp": 1473237480,
          "value": 0.0
        },
        {
          "timestamp": 1473237540,
          "value": 0.0
        },
        {
          "timestamp": 1473237600,
          "value": 0.0
        },
        {
          "timestamp": 1473237660,
          "value": 0.0
        },
        {
          "timestamp": 1473237720,
          "value": 0.0
        },
        {
          "timestamp": 1473237780,
          "value": 0.0
        },
        {
          "timestamp": 1473237840,
          "value": 0.0
        },
        {
          "timestamp": 1473237900,
          "value": 114716672.0
        },
        {
          "timestamp": 1473237960,
          "value": 114716672.0
        },
        {
          "timestamp": 1473238020,
          "value": 111296512.0
        },
        {
          "timestamp": 1473238080,
          "value": 0.0
        },
        {
          "timestamp": 1473238140,
          "value": 0.0
        },
        {
          "timestamp": 1473238200,
          "value": 113246208.0
        },
        {
          "timestamp": 1473238260,
          "value": 113553408.0
        },
        {
          "timestamp": 1473238320,
          "value": 114814976.0
        },
        {
          "timestamp": 1473238380,
          "value": 113967104.0
        },
        {
          "timestamp": 1473238440,
          "value": 113967104.0
        },
        {
          "timestamp": 1473238500,
          "value": 110706688.0
        },
        {
          "timestamp": 1473238560,
          "value": 110706688.0
        },
        {
          "timestamp": 1473238620,
          "value": 108167168.0
        },
        {
          "timestamp": 1473238680,
          "value": null
        },
        {
          "timestamp": 1473238740,
          "value": null
        },
        {
          "timestamp": 1473238800,
          "value": null
        },
        {
          "timestamp": 1473238860,
          "value": null
        },
        {
          "timestamp": 1473238920,
          "value": null
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "disk.io.write_bytes/device=sda"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.122.69",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": null
        },
        {
          "timestamp": 1473235500,
          "value": null
        },
        {
          "timestamp": 1473235560,
          "value": null
        },
        {
          "timestamp": 1473235620,
          "value": null
        },
        {
          "timestamp": 1473235680,
          "value": null
        },
        {
          "timestamp": 1473235740,
          "value": null
        },
        {
          "timestamp": 1473235800,
          "value": null
        },
        {
          "timestamp": 1473235860,
          "value": null
        },
        {
          "timestamp": 1473235920,
          "value": null
        },
        {
          "timestamp": 1473235980,
          "value": null
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": 0.0
        },
        {
          "timestamp": 1473236520,
          "value": 0.0
        },
        {
          "timestamp": 1473236580,
          "value": 0.0
        },
        {
          "timestamp": 1473236640,
          "value": 0.0
        },
        {
          "timestamp": 1473236700,
          "value": null
        },
        {
          "timestamp": 1473236760,
          "value": null
        },
        {
          "timestamp": 1473236820,
          "value": null
        },
        {
          "timestamp": 1473236880,
          "value": 0.0
        },
        {
          "timestamp": 1473236940,
          "value": 0.0
        },
        {
          "timestamp": 1473237000,
          "value": 0.0
        },
        {
          "timestamp": 1473237060,
          "value": 0.0
        },
        {
          "timestamp": 1473237120,
          "value": 0.0
        },
        {
          "timestamp": 1473237180,
          "value": 0.0
        },
        {
          "timestamp": 1473237240,
          "value": 0.0
        },
        {
          "timestamp": 1473237300,
          "value": 0.0
        },
        {
          "timestamp": 1473237360,
          "value": 0.0
        },
        {
          "timestamp": 1473237420,
          "value": 0.0
        },
        {
          "timestamp": 1473237480,
          "value": 0.0
        },
        {
          "timestamp": 1473237540,
          "value": 0.0
        },
        {
          "timestamp": 1473237600,
          "value": 0.0
        },
        {
          "timestamp": 1473237660,
          "value": 0.0
        },
        {
          "timestamp": 1473237720,
          "value": 0.0
        },
        {
          "timestamp": 1473237780,
          "value": 0.0
        },
        {
          "timestamp": 1473237840,
          "value": null
        },
        {
          "timestamp": 1473237900,
          "value": 0.0
        },
        {
          "timestamp": 1473237960,
          "value": 0.0
        },
        {
          "timestamp": 1473238020,
          "value": 0.0
        },
        {
          "timestamp": 1473238080,
          "value": null
        },
        {
          "timestamp": 1473238140,
          "value": 0.0
        },
        {
          "timestamp": 1473238200,
          "value": 0.0
        },
        {
          "timestamp": 1473238260,
          "value": 0.0
        },
        {
          "timestamp": 1473238320,
          "value": 0.0
        },
        {
          "timestamp": 1473238380,
          "value": 0.0
        },
        {
          "timestamp": 1473238440,
          "value": 0.0
        },
        {
          "timestamp": 1473238500,
          "value": 0.0
        },
        {
          "timestamp": 1473238560,
          "value": 0.0
        },
        {
          "timestamp": 1473238620,
          "value": 0.0
        },
        {
          "timestamp": 1473238680,
          "value": 0.0
        },
        {
          "timestamp": 1473238740,
          "value": null
        },
        {
          "timestamp": 1473238800,
          "value": null
        },
        {
          "timestamp": 1473238860,
          "value": null
        },
        {
          "timestamp": 1473238920,
          "value": null
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "disk.io.read_bytes/device=sda"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.122.69",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": null
        },
        {
          "timestamp": 1473235500,
          "value": null
        },
        {
          "timestamp": 1473235560,
          "value": null
        },
        {
          "timestamp": 1473235620,
          "value": null
        },
        {
          "timestamp": 1473235680,
          "value": null
        },
        {
          "timestamp": 1473235740,
          "value": null
        },
        {
          "timestamp": 1473235800,
          "value": null
        },
        {
          "timestamp": 1473235860,
          "value": null
        },
        {
          "timestamp": 1473235920,
          "value": null
        },
        {
          "timestamp": 1473235980,
          "value": null
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": 95.90985
        },
        {
          "timestamp": 1473236520,
          "value": 92.230576
        },
        {
          "timestamp": 1473236580,
          "value": 94.576554
        },
        {
          "timestamp": 1473236640,
          "value": 93.403361
        },
        {
          "timestamp": 1473236700,
          "value": 93.403361
        },
        {
          "timestamp": 1473236760,
          "value": 93.955815
        },
        {
          "timestamp": 1473236820,
          "value": 93.955815
        },
        {
          "timestamp": 1473236880,
          "value": 96.370463
        },
        {
          "timestamp": 1473236940,
          "value": 94.70392
        },
        {
          "timestamp": 1473237000,
          "value": 85.588605
        },
        {
          "timestamp": 1473237060,
          "value": 94.358546
        },
        {
          "timestamp": 1473237120,
          "value": 94.034209
        },
        {
          "timestamp": 1473237180,
          "value": 94.506866
        },
        {
          "timestamp": 1473237240,
          "value": 94.70392
        },
        {
          "timestamp": 1473237300,
          "value": 96.446488
        },
        {
          "timestamp": 1473237360,
          "value": 94.785148
        },
        {
          "timestamp": 1473237420,
          "value": 92.035029
        },
        {
          "timestamp": 1473237480,
          "value": 95.702962
        },
        {
          "timestamp": 1473237540,
          "value": 94.451398
        },
        {
          "timestamp": 1473237600,
          "value": 94.57429
        },
        {
          "timestamp": 1473237660,
          "value": 94.70171
        },
        {
          "timestamp": 1473237720,
          "value": 94.073456
        },
        {
          "timestamp": 1473237780,
          "value": 94.152293
        },
        {
          "timestamp": 1473237840,
          "value": 94.697286
        },
        {
          "timestamp": 1473237900,
          "value": 93.830763
        },
        {
          "timestamp": 1473237960,
          "value": 94.27736
        },
        {
          "timestamp": 1473238020,
          "value": 94.906054
        },
        {
          "timestamp": 1473238080,
          "value": null
        },
        {
          "timestamp": 1473238140,
          "value": 94.198664
        },
        {
          "timestamp": 1473238200,
          "value": 93.119266
        },
        {
          "timestamp": 1473238260,
          "value": 96.158664
        },
        {
          "timestamp": 1473238320,
          "value": 95.446951
        },
        {
          "timestamp": 1473238380,
          "value": 93.825615
        },
        {
          "timestamp": 1473238440,
          "value": 93.375
        },
        {
          "timestamp": 1473238500,
          "value": 95.154553
        },
        {
          "timestamp": 1473238560,
          "value": 94.493116
        },
        {
          "timestamp": 1473238620,
          "value": 95.035461
        },
        {
          "timestamp": 1473238680,
          "value": 91.022965
        },
        {
          "timestamp": 1473238740,
          "value": null
        },
        {
          "timestamp": 1473238800,
          "value": null
        },
        {
          "timestamp": 1473238860,
          "value": null
        },
        {
          "timestamp": 1473238920,
          "value": null
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "cpu.idle"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.122.69",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": null
        },
        {
          "timestamp": 1473235500,
          "value": null
        },
        {
          "timestamp": 1473235560,
          "value": null
        },
        {
          "timestamp": 1473235620,
          "value": null
        },
        {
          "timestamp": 1473235680,
          "value": null
        },
        {
          "timestamp": 1473235740,
          "value": null
        },
        {
          "timestamp": 1473235800,
          "value": null
        },
        {
          "timestamp": 1473235860,
          "value": null
        },
        {
          "timestamp": 1473235920,
          "value": null
        },
        {
          "timestamp": 1473235980,
          "value": null
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": 0.0
        },
        {
          "timestamp": 1473236520,
          "value": 0.0
        },
        {
          "timestamp": 1473236580,
          "value": 0.0
        },
        {
          "timestamp": 1473236640,
          "value": 0.0
        },
        {
          "timestamp": 1473236700,
          "value": null
        },
        {
          "timestamp": 1473236760,
          "value": null
        },
        {
          "timestamp": 1473236820,
          "value": null
        },
        {
          "timestamp": 1473236880,
          "value": 102400.0
        },
        {
          "timestamp": 1473236940,
          "value": 0.0
        },
        {
          "timestamp": 1473237000,
          "value": 0.0
        },
        {
          "timestamp": 1473237060,
          "value": 0.0
        },
        {
          "timestamp": 1473237120,
          "value": 0.0
        },
        {
          "timestamp": 1473237180,
          "value": 106496.0
        },
        {
          "timestamp": 1473237240,
          "value": 110592.0
        },
        {
          "timestamp": 1473237300,
          "value": 4096.0
        },
        {
          "timestamp": 1473237360,
          "value": 4096.0
        },
        {
          "timestamp": 1473237420,
          "value": 131072.0
        },
        {
          "timestamp": 1473237480,
          "value": 0.0
        },
        {
          "timestamp": 1473237540,
          "value": 126976.0
        },
        {
          "timestamp": 1473237600,
          "value": 0.0
        },
        {
          "timestamp": 1473237660,
          "value": 0.0
        },
        {
          "timestamp": 1473237720,
          "value": 0.0
        },
        {
          "timestamp": 1473237780,
          "value": 147456.0
        },
        {
          "timestamp": 1473237840,
          "value": 139264.0
        },
        {
          "timestamp": 1473237900,
          "value": 139264.0
        },
        {
          "timestamp": 1473237960,
          "value": 0.0
        },
        {
          "timestamp": 1473238020,
          "value": 0.0
        },
        {
          "timestamp": 1473238080,
          "value": null
        },
        {
          "timestamp": 1473238140,
          "value": 0.0
        },
        {
          "timestamp": 1473238200,
          "value": 0.0
        },
        {
          "timestamp": 1473238260,
          "value": 135168.0
        },
        {
          "timestamp": 1473238320,
          "value": 0.0
        },
        {
          "timestamp": 1473238380,
          "value": 0.0
        },
        {
          "timestamp": 1473238440,
          "value": 90112.0
        },
        {
          "timestamp": 1473238500,
          "value": 0.0
        },
        {
          "timestamp": 1473238560,
          "value": 4096.0
        },
        {
          "timestamp": 1473238620,
          "value": 106496.0
        },
        {
          "timestamp": 1473238680,
          "value": 4096.0
        },
        {
          "timestamp": 1473238740,
          "value": null
        },
        {
          "timestamp": 1473238800,
          "value": null
        },
        {
          "timestamp": 1473238860,
          "value": null
        },
        {
          "timestamp": 1473238920,
          "value": null
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "disk.io.write_bytes/device=sda"
    }
  ],
  "dns": [
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.92.206",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": 0.0
        },
        {
          "timestamp": 1473235500,
          "value": 0.0
        },
        {
          "timestamp": 1473235560,
          "value": 0.0
        },
        {
          "timestamp": 1473235620,
          "value": 0.0
        },
        {
          "timestamp": 1473235680,
          "value": 0.0
        },
        {
          "timestamp": 1473235740,
          "value": 0.0
        },
        {
          "timestamp": 1473235800,
          "value": 0.0
        },
        {
          "timestamp": 1473235860,
          "value": 0.0
        },
        {
          "timestamp": 1473235920,
          "value": 0.0
        },
        {
          "timestamp": 1473235980,
          "value": 0.0
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": null
        },
        {
          "timestamp": 1473236520,
          "value": null
        },
        {
          "timestamp": 1473236580,
          "value": null
        },
        {
          "timestamp": 1473236640,
          "value": 0.0
        },
        {
          "timestamp": 1473236700,
          "value": 0.0
        },
        {
          "timestamp": 1473236760,
          "value": 0.0
        },
        {
          "timestamp": 1473236820,
          "value": 0.0
        },
        {
          "timestamp": 1473236880,
          "value": 0.0
        },
        {
          "timestamp": 1473236940,
          "value": 0.0
        },
        {
          "timestamp": 1473237000,
          "value": 0.0
        },
        {
          "timestamp": 1473237060,
          "value": 0.0
        },
        {
          "timestamp": 1473237120,
          "value": 0.0
        },
        {
          "timestamp": 1473237180,
          "value": 0.0
        },
        {
          "timestamp": 1473237240,
          "value": 0.0
        },
        {
          "timestamp": 1473237300,
          "value": 0.0
        },
        {
          "timestamp": 1473237360,
          "value": 0.0
        },
        {
          "timestamp": 1473237420,
          "value": 0.0
        },
        {
          "timestamp": 1473237480,
          "value": 0.0
        },
        {
          "timestamp": 1473237540,
          "value": 0.0
        },
        {
          "timestamp": 1473237600,
          "value": 0.0
        },
        {
          "timestamp": 1473237660,
          "value": 0.0
        },
        {
          "timestamp": 1473237720,
          "value": 0.0
        },
        {
          "timestamp": 1473237780,
          "value": 0.0
        },
        {
          "timestamp": 1473237840,
          "value": 0.0
        },
        {
          "timestamp": 1473237900,
          "value": 0.0
        },
        {
          "timestamp": 1473237960,
          "value": 0.0
        },
        {
          "timestamp": 1473238020,
          "value": 0.0
        },
        {
          "timestamp": 1473238080,
          "value": 0.0
        },
        {
          "timestamp": 1473238140,
          "value": 0.0
        },
        {
          "timestamp": 1473238200,
          "value": 0.0
        },
        {
          "timestamp": 1473238260,
          "value": 0.0
        },
        {
          "timestamp": 1473238320,
          "value": 0.0
        },
        {
          "timestamp": 1473238380,
          "value": null
        },
        {
          "timestamp": 1473238440,
          "value": 0.0
        },
        {
          "timestamp": 1473238500,
          "value": 0.0
        },
        {
          "timestamp": 1473238560,
          "value": 0.0
        },
        {
          "timestamp": 1473238620,
          "value": 0.0
        },
        {
          "timestamp": 1473238680,
          "value": 0.0
        },
        {
          "timestamp": 1473238740,
          "value": null
        },
        {
          "timestamp": 1473238800,
          "value": null
        },
        {
          "timestamp": 1473238860,
          "value": 0.0
        },
        {
          "timestamp": 1473238920,
          "value": 0.0
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "disk.io.read_bytes/device=sda"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.92.206",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": 95.3125
        },
        {
          "timestamp": 1473235500,
          "value": 95.59375
        },
        {
          "timestamp": 1473235560,
          "value": 98.437012
        },
        {
          "timestamp": 1473235620,
          "value": 98.718349
        },
        {
          "timestamp": 1473235680,
          "value": 98.592871
        },
        {
          "timestamp": 1473235740,
          "value": 98.341158
        },
        {
          "timestamp": 1473235800,
          "value": 96.655205
        },
        {
          "timestamp": 1473235860,
          "value": 96.655205
        },
        {
          "timestamp": 1473235920,
          "value": 98.53125
        },
        {
          "timestamp": 1473235980,
          "value": 98.53125
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": null
        },
        {
          "timestamp": 1473236520,
          "value": null
        },
        {
          "timestamp": 1473236580,
          "value": null
        },
        {
          "timestamp": 1473236640,
          "value": 98.780488
        },
        {
          "timestamp": 1473236700,
          "value": 98.780488
        },
        {
          "timestamp": 1473236760,
          "value": 97.589984
        },
        {
          "timestamp": 1473236820,
          "value": 95.44035
        },
        {
          "timestamp": 1473236880,
          "value": 99.219969
        },
        {
          "timestamp": 1473236940,
          "value": 98.65583
        },
        {
          "timestamp": 1473237000,
          "value": 98.562051
        },
        {
          "timestamp": 1473237060,
          "value": 98.467792
        },
        {
          "timestamp": 1473237120,
          "value": 98.968105
        },
        {
          "timestamp": 1473237180,
          "value": 98.530331
        },
        {
          "timestamp": 1473237240,
          "value": 98.59331
        },
        {
          "timestamp": 1473237300,
          "value": 98.500937
        },
        {
          "timestamp": 1473237360,
          "value": 96.8125
        },
        {
          "timestamp": 1473237420,
          "value": 96.375
        },
        {
          "timestamp": 1473237480,
          "value": 95.434647
        },
        {
          "timestamp": 1473237540,
          "value": 98.84375
        },
        {
          "timestamp": 1473237600,
          "value": 97.52816
        },
        {
          "timestamp": 1473237660,
          "value": 98.53125
        },
        {
          "timestamp": 1473237720,
          "value": 98.40625
        },
        {
          "timestamp": 1473237780,
          "value": 98.68709
        },
        {
          "timestamp": 1473237840,
          "value": 98.53125
        },
        {
          "timestamp": 1473237900,
          "value": 98.937168
        },
        {
          "timestamp": 1473237960,
          "value": 98.905566
        },
        {
          "timestamp": 1473238020,
          "value": 95.841151
        },
        {
          "timestamp": 1473238080,
          "value": 98.971001
        },
        {
          "timestamp": 1473238140,
          "value": 96.530166
        },
        {
          "timestamp": 1473238200,
          "value": 98.594628
        },
        {
          "timestamp": 1473238260,
          "value": 96.15625
        },
        {
          "timestamp": 1473238320,
          "value": 98.748436
        },
        {
          "timestamp": 1473238380,
          "value": null
        },
        {
          "timestamp": 1473238440,
          "value": 97.873671
        },
        {
          "timestamp": 1473238500,
          "value": 98.844111
        },
        {
          "timestamp": 1473238560,
          "value": 98.718349
        },
        {
          "timestamp": 1473238620,
          "value": 94.182046
        },
        {
          "timestamp": 1473238680,
          "value": 97.625
        },
        {
          "timestamp": 1473238740,
          "value": null
        },
        {
          "timestamp": 1473238800,
          "value": null
        },
        {
          "timestamp": 1473238860,
          "value": 98.999687
        },
        {
          "timestamp": 1473238920,
          "value": 98.62457
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "cpu.idle"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.92.206",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": 32768.0
        },
        {
          "timestamp": 1473235500,
          "value": 0.0
        },
        {
          "timestamp": 1473235560,
          "value": 32768.0
        },
        {
          "timestamp": 1473235620,
          "value": 32768.0
        },
        {
          "timestamp": 1473235680,
          "value": 114688.0
        },
        {
          "timestamp": 1473235740,
          "value": 32768.0
        },
        {
          "timestamp": 1473235800,
          "value": 131072.0
        },
        {
          "timestamp": 1473235860,
          "value": 131072.0
        },
        {
          "timestamp": 1473235920,
          "value": 32768.0
        },
        {
          "timestamp": 1473235980,
          "value": 32768.0
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": null
        },
        {
          "timestamp": 1473236520,
          "value": null
        },
        {
          "timestamp": 1473236580,
          "value": null
        },
        {
          "timestamp": 1473236640,
          "value": 0.0
        },
        {
          "timestamp": 1473236700,
          "value": 0.0
        },
        {
          "timestamp": 1473236760,
          "value": 94208.0
        },
        {
          "timestamp": 1473236820,
          "value": 0.0
        },
        {
          "timestamp": 1473236880,
          "value": 32768.0
        },
        {
          "timestamp": 1473236940,
          "value": 32768.0
        },
        {
          "timestamp": 1473237000,
          "value": 32768.0
        },
        {
          "timestamp": 1473237060,
          "value": 32768.0
        },
        {
          "timestamp": 1473237120,
          "value": 32768.0
        },
        {
          "timestamp": 1473237180,
          "value": 102400.0
        },
        {
          "timestamp": 1473237240,
          "value": 32768.0
        },
        {
          "timestamp": 1473237300,
          "value": 131072.0
        },
        {
          "timestamp": 1473237360,
          "value": null
        },
        {
          "timestamp": 1473237420,
          "value": 0.0
        },
        {
          "timestamp": 1473237480,
          "value": 32768.0
        },
        {
          "timestamp": 1473237540,
          "value": 0.0
        },
        {
          "timestamp": 1473237600,
          "value": 65536.0
        },
        {
          "timestamp": 1473237660,
          "value": 32768.0
        },
        {
          "timestamp": 1473237720,
          "value": 32768.0
        },
        {
          "timestamp": 1473237780,
          "value": null
        },
        {
          "timestamp": 1473237840,
          "value": 32768.0
        },
        {
          "timestamp": 1473237900,
          "value": 114688.0
        },
        {
          "timestamp": 1473237960,
          "value": 0.0
        },
        {
          "timestamp": 1473238020,
          "value": 0.0
        },
        {
          "timestamp": 1473238080,
          "value": 151552.0
        },
        {
          "timestamp": 1473238140,
          "value": 0.0
        },
        {
          "timestamp": 1473238200,
          "value": 32768.0
        },
        {
          "timestamp": 1473238260,
          "value": 32768.0
        },
        {
          "timestamp": 1473238320,
          "value": 32768.0
        },
        {
          "timestamp": 1473238380,
          "value": 32768.0
        },
        {
          "timestamp": 1473238440,
          "value": 126976.0
        },
        {
          "timestamp": 1473238500,
          "value": 0.0
        },
        {
          "timestamp": 1473238560,
          "value": 32768.0
        },
        {
          "timestamp": 1473238620,
          "value": 32768.0
        },
        {
          "timestamp": 1473238680,
          "value": 0.0
        },
        {
          "timestamp": 1473238740,
          "value": null
        },
        {
          "timestamp": 1473238800,
          "value": null
        },
        {
          "timestamp": 1473238860,
          "value": 0.0
        },
        {
          "timestamp": 1473238920,
          "value": 172032.0
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "disk.io.write_bytes/device=sda"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.93.88",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": 0.0
        },
        {
          "timestamp": 1473235500,
          "value": 0.0
        },
        {
          "timestamp": 1473235560,
          "value": 0.0
        },
        {
          "timestamp": 1473235620,
          "value": 0.0
        },
        {
          "timestamp": 1473235680,
          "value": 0.0
        },
        {
          "timestamp": 1473235740,
          "value": 0.0
        },
        {
          "timestamp": 1473235800,
          "value": 0.0
        },
        {
          "timestamp": 1473235860,
          "value": 0.0
        },
        {
          "timestamp": 1473235920,
          "value": 0.0
        },
        {
          "timestamp": 1473235980,
          "value": 0.0
        },
        {
          "timestamp": 1473236040,
          "value": 0.0
        },
        {
          "timestamp": 1473236100,
          "value": 0.0
        },
        {
          "timestamp": 1473236160,
          "value": 0.0
        },
        {
          "timestamp": 1473236220,
          "value": 0.0
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": null
        },
        {
          "timestamp": 1473236520,
          "value": null
        },
        {
          "timestamp": 1473236580,
          "value": 0.0
        },
        {
          "timestamp": 1473236640,
          "value": 0.0
        },
        {
          "timestamp": 1473236700,
          "value": 0.0
        },
        {
          "timestamp": 1473236760,
          "value": 0.0
        },
        {
          "timestamp": 1473236820,
          "value": 0.0
        },
        {
          "timestamp": 1473236880,
          "value": 0.0
        },
        {
          "timestamp": 1473236940,
          "value": 0.0
        },
        {
          "timestamp": 1473237000,
          "value": 0.0
        },
        {
          "timestamp": 1473237060,
          "value": 0.0
        },
        {
          "timestamp": 1473237120,
          "value": 0.0
        },
        {
          "timestamp": 1473237180,
          "value": 0.0
        },
        {
          "timestamp": 1473237240,
          "value": 0.0
        },
        {
          "timestamp": 1473237300,
          "value": 0.0
        },
        {
          "timestamp": 1473237360,
          "value": 0.0
        },
        {
          "timestamp": 1473237420,
          "value": 0.0
        },
        {
          "timestamp": 1473237480,
          "value": null
        },
        {
          "timestamp": 1473237540,
          "value": 0.0
        },
        {
          "timestamp": 1473237600,
          "value": 0.0
        },
        {
          "timestamp": 1473237660,
          "value": 0.0
        },
        {
          "timestamp": 1473237720,
          "value": 0.0
        },
        {
          "timestamp": 1473237780,
          "value": null
        },
        {
          "timestamp": 1473237840,
          "value": null
        },
        {
          "timestamp": 1473237900,
          "value": 0.0
        },
        {
          "timestamp": 1473237960,
          "value": 0.0
        },
        {
          "timestamp": 1473238020,
          "value": 0.0
        },
        {
          "timestamp": 1473238080,
          "value": null
        },
        {
          "timestamp": 1473238140,
          "value": 0.0
        },
        {
          "timestamp": 1473238200,
          "value": 0.0
        },
        {
          "timestamp": 1473238260,
          "value": 0.0
        },
        {
          "timestamp": 1473238320,
          "value": 0.0
        },
        {
          "timestamp": 1473238380,
          "value": 0.0
        },
        {
          "timestamp": 1473238440,
          "value": 0.0
        },
        {
          "timestamp": 1473238500,
          "value": 0.0
        },
        {
          "timestamp": 1473238560,
          "value": 0.0
        },
        {
          "timestamp": 1473238620,
          "value": null
        },
        {
          "timestamp": 1473238680,
          "value": null
        },
        {
          "timestamp": 1473238740,
          "value": 0.0
        },
        {
          "timestamp": 1473238800,
          "value": 0.0
        },
        {
          "timestamp": 1473238860,
          "value": 0.0
        },
        {
          "timestamp": 1473238920,
          "value": 0.0
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "disk.io.read_bytes/device=sda"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.93.88",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": 98.166667
        },
        {
          "timestamp": 1473235500,
          "value": 97.870564
        },
        {
          "timestamp": 1473235560,
          "value": 98.375
        },
        {
          "timestamp": 1473235620,
          "value": 97.830622
        },
        {
          "timestamp": 1473235680,
          "value": 97.745303
        },
        {
          "timestamp": 1473235740,
          "value": 98.626145
        },
        {
          "timestamp": 1473235800,
          "value": 98.373645
        },
        {
          "timestamp": 1473235860,
          "value": 98.2881
        },
        {
          "timestamp": 1473235920,
          "value": 98.498749
        },
        {
          "timestamp": 1473235980,
          "value": 98.498749
        },
        {
          "timestamp": 1473236040,
          "value": 97.291667
        },
        {
          "timestamp": 1473236100,
          "value": 97.621035
        },
        {
          "timestamp": 1473236160,
          "value": 97.621035
        },
        {
          "timestamp": 1473236220,
          "value": 98.707795
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": null
        },
        {
          "timestamp": 1473236520,
          "value": null
        },
        {
          "timestamp": 1473236580,
          "value": 97.96173
        },
        {
          "timestamp": 1473236640,
          "value": 98.455115
        },
        {
          "timestamp": 1473236700,
          "value": 97.998332
        },
        {
          "timestamp": 1473236760,
          "value": 98.416007
        },
        {
          "timestamp": 1473236820,
          "value": 98.497496
        },
        {
          "timestamp": 1473236880,
          "value": 98.623853
        },
        {
          "timestamp": 1473236940,
          "value": 98.458975
        },
        {
          "timestamp": 1473237000,
          "value": 98.458333
        },
        {
          "timestamp": 1473237060,
          "value": 98.623853
        },
        {
          "timestamp": 1473237120,
          "value": 98.332639
        },
        {
          "timestamp": 1473237180,
          "value": 98.24781
        },
        {
          "timestamp": 1473237240,
          "value": 98.539841
        },
        {
          "timestamp": 1473237300,
          "value": 99.040867
        },
        {
          "timestamp": 1473237360,
          "value": 98.54045
        },
        {
          "timestamp": 1473237420,
          "value": 98.332639
        },
        {
          "timestamp": 1473237480,
          "value": 98.332639
        },
        {
          "timestamp": 1473237540,
          "value": 98.043297
        },
        {
          "timestamp": 1473237600,
          "value": 98.123436
        },
        {
          "timestamp": 1473237660,
          "value": 98.249271
        },
        {
          "timestamp": 1473237720,
          "value": 98.164372
        },
        {
          "timestamp": 1473237780,
          "value": 98.24854
        },
        {
          "timestamp": 1473237840,
          "value": 98.07853
        },
        {
          "timestamp": 1473237900,
          "value": 98.07853
        },
        {
          "timestamp": 1473237960,
          "value": 98.664998
        },
        {
          "timestamp": 1473238020,
          "value": 98.331943
        },
        {
          "timestamp": 1473238080,
          "value": 98.622129
        },
        {
          "timestamp": 1473238140,
          "value": 98.748957
        },
        {
          "timestamp": 1473238200,
          "value": 98.334027
        },
        {
          "timestamp": 1473238260,
          "value": 98.333333
        },
        {
          "timestamp": 1473238320,
          "value": 98.499375
        },
        {
          "timestamp": 1473238380,
          "value": 98.582152
        },
        {
          "timestamp": 1473238440,
          "value": 98.582152
        },
        {
          "timestamp": 1473238500,
          "value": 98.498749
        },
        {
          "timestamp": 1473238560,
          "value": 98.373645
        },
        {
          "timestamp": 1473238620,
          "value": null
        },
        {
          "timestamp": 1473238680,
          "value": null
        },
        {
          "timestamp": 1473238740,
          "value": 98.416007
        },
        {
          "timestamp": 1473238800,
          "value": 98.415346
        },
        {
          "timestamp": 1473238860,
          "value": 98.375677
        },
        {
          "timestamp": 1473238920,
          "value": 98.499375
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "cpu.idle"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.93.88",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": 49152.0
        },
        {
          "timestamp": 1473235500,
          "value": 237568.0
        },
        {
          "timestamp": 1473235560,
          "value": 98304.0
        },
        {
          "timestamp": 1473235620,
          "value": 212992.0
        },
        {
          "timestamp": 1473235680,
          "value": 192512.0
        },
        {
          "timestamp": 1473235740,
          "value": 217088.0
        },
        {
          "timestamp": 1473235800,
          "value": 98304.0
        },
        {
          "timestamp": 1473235860,
          "value": 311296.0
        },
        {
          "timestamp": 1473235920,
          "value": 147456.0
        },
        {
          "timestamp": 1473235980,
          "value": 147456.0
        },
        {
          "timestamp": 1473236040,
          "value": 348160.0
        },
        {
          "timestamp": 1473236100,
          "value": 237568.0
        },
        {
          "timestamp": 1473236160,
          "value": 237568.0
        },
        {
          "timestamp": 1473236220,
          "value": 49152.0
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": null
        },
        {
          "timestamp": 1473236520,
          "value": null
        },
        {
          "timestamp": 1473236580,
          "value": 118784.0
        },
        {
          "timestamp": 1473236640,
          "value": 0.0
        },
        {
          "timestamp": 1473236700,
          "value": 102400.0
        },
        {
          "timestamp": 1473236760,
          "value": 237568.0
        },
        {
          "timestamp": 1473236820,
          "value": 98304.0
        },
        {
          "timestamp": 1473236880,
          "value": 233472.0
        },
        {
          "timestamp": 1473236940,
          "value": 106496.0
        },
        {
          "timestamp": 1473237000,
          "value": 98304.0
        },
        {
          "timestamp": 1473237060,
          "value": 98304.0
        },
        {
          "timestamp": 1473237120,
          "value": 106496.0
        },
        {
          "timestamp": 1473237180,
          "value": 229376.0
        },
        {
          "timestamp": 1473237240,
          "value": 98304.0
        },
        {
          "timestamp": 1473237300,
          "value": 98304.0
        },
        {
          "timestamp": 1473237360,
          "value": 98304.0
        },
        {
          "timestamp": 1473237420,
          "value": 147456.0
        },
        {
          "timestamp": 1473237480,
          "value": 163840.0
        },
        {
          "timestamp": 1473237540,
          "value": 163840.0
        },
        {
          "timestamp": 1473237600,
          "value": 286720.0
        },
        {
          "timestamp": 1473237660,
          "value": 110592.0
        },
        {
          "timestamp": 1473237720,
          "value": 221184.0
        },
        {
          "timestamp": 1473237780,
          "value": null
        },
        {
          "timestamp": 1473237840,
          "value": null
        },
        {
          "timestamp": 1473237900,
          "value": 266240.0
        },
        {
          "timestamp": 1473237960,
          "value": 57344.0
        },
        {
          "timestamp": 1473238020,
          "value": 212992.0
        },
        {
          "timestamp": 1473238080,
          "value": null
        },
        {
          "timestamp": 1473238140,
          "value": 69632.0
        },
        {
          "timestamp": 1473238200,
          "value": 151552.0
        },
        {
          "timestamp": 1473238260,
          "value": 204800.0
        },
        {
          "timestamp": 1473238320,
          "value": 126976.0
        },
        {
          "timestamp": 1473238380,
          "value": 126976.0
        },
        {
          "timestamp": 1473238440,
          "value": 249856.0
        },
        {
          "timestamp": 1473238500,
          "value": 126976.0
        },
        {
          "timestamp": 1473238560,
          "value": 126976.0
        },
        {
          "timestamp": 1473238620,
          "value": null
        },
        {
          "timestamp": 1473238680,
          "value": null
        },
        {
          "timestamp": 1473238740,
          "value": 159744.0
        },
        {
          "timestamp": 1473238800,
          "value": 77824.0
        },
        {
          "timestamp": 1473238860,
          "value": 294912.0
        },
        {
          "timestamp": 1473238920,
          "value": 126976.0
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "disk.io.write_bytes/device=sda"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.93.92",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": null
        },
        {
          "timestamp": 1473235500,
          "value": 0.0
        },
        {
          "timestamp": 1473235560,
          "value": 0.0
        },
        {
          "timestamp": 1473235620,
          "value": 0.0
        },
        {
          "timestamp": 1473235680,
          "value": 0.0
        },
        {
          "timestamp": 1473235740,
          "value": 0.0
        },
        {
          "timestamp": 1473235800,
          "value": 0.0
        },
        {
          "timestamp": 1473235860,
          "value": 0.0
        },
        {
          "timestamp": 1473235920,
          "value": 0.0
        },
        {
          "timestamp": 1473235980,
          "value": null
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": 0.0
        },
        {
          "timestamp": 1473236460,
          "value": 0.0
        },
        {
          "timestamp": 1473236520,
          "value": 0.0
        },
        {
          "timestamp": 1473236580,
          "value": 0.0
        },
        {
          "timestamp": 1473236640,
          "value": 0.0
        },
        {
          "timestamp": 1473236700,
          "value": 0.0
        },
        {
          "timestamp": 1473236760,
          "value": 0.0
        },
        {
          "timestamp": 1473236820,
          "value": 0.0
        },
        {
          "timestamp": 1473236880,
          "value": 0.0
        },
        {
          "timestamp": 1473236940,
          "value": 0.0
        },
        {
          "timestamp": 1473237000,
          "value": 0.0
        },
        {
          "timestamp": 1473237060,
          "value": 0.0
        },
        {
          "timestamp": 1473237120,
          "value": 0.0
        },
        {
          "timestamp": 1473237180,
          "value": 0.0
        },
        {
          "timestamp": 1473237240,
          "value": 0.0
        },
        {
          "timestamp": 1473237300,
          "value": 0.0
        },
        {
          "timestamp": 1473237360,
          "value": 0.0
        },
        {
          "timestamp": 1473237420,
          "value": 0.0
        },
        {
          "timestamp": 1473237480,
          "value": 0.0
        },
        {
          "timestamp": 1473237540,
          "value": 0.0
        },
        {
          "timestamp": 1473237600,
          "value": 0.0
        },
        {
          "timestamp": 1473237660,
          "value": 0.0
        },
        {
          "timestamp": 1473237720,
          "value": 0.0
        },
        {
          "timestamp": 1473237780,
          "value": 0.0
        },
        {
          "timestamp": 1473237840,
          "value": 0.0
        },
        {
          "timestamp": 1473237900,
          "value": 0.0
        },
        {
          "timestamp": 1473237960,
          "value": 0.0
        },
        {
          "timestamp": 1473238020,
          "value": 0.0
        },
        {
          "timestamp": 1473238080,
          "value": null
        },
        {
          "timestamp": 1473238140,
          "value": 0.0
        },
        {
          "timestamp": 1473238200,
          "value": 0.0
        },
        {
          "timestamp": 1473238260,
          "value": 0.0
        },
        {
          "timestamp": 1473238320,
          "value": 0.0
        },
        {
          "timestamp": 1473238380,
          "value": null
        },
        {
          "timestamp": 1473238440,
          "value": 0.0
        },
        {
          "timestamp": 1473238500,
          "value": null
        },
        {
          "timestamp": 1473238560,
          "value": null
        },
        {
          "timestamp": 1473238620,
          "value": 0.0
        },
        {
          "timestamp": 1473238680,
          "value": null
        },
        {
          "timestamp": 1473238740,
          "value": null
        },
        {
          "timestamp": 1473238800,
          "value": null
        },
        {
          "timestamp": 1473238860,
          "value": 0.0
        },
        {
          "timestamp": 1473238920,
          "value": null
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "disk.io.read_bytes/device=sda"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.93.92",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": null
        },
        {
          "timestamp": 1473235500,
          "value": 98.999583
        },
        {
          "timestamp": 1473235560,
          "value": 99.249687
        },
        {
          "timestamp": 1473235620,
          "value": 99.000416
        },
        {
          "timestamp": 1473235680,
          "value": 98.915763
        },
        {
          "timestamp": 1473235740,
          "value": 98.874062
        },
        {
          "timestamp": 1473235800,
          "value": 99.082186
        },
        {
          "timestamp": 1473235860,
          "value": 99.0
        },
        {
          "timestamp": 1473235920,
          "value": 98.875
        },
        {
          "timestamp": 1473235980,
          "value": null
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": 98.999166
        },
        {
          "timestamp": 1473236460,
          "value": 98.999166
        },
        {
          "timestamp": 1473236520,
          "value": 99.0
        },
        {
          "timestamp": 1473236580,
          "value": 98.83236
        },
        {
          "timestamp": 1473236640,
          "value": 98.791163
        },
        {
          "timestamp": 1473236700,
          "value": 99.125
        },
        {
          "timestamp": 1473236760,
          "value": 99.081803
        },
        {
          "timestamp": 1473236820,
          "value": 99.082186
        },
        {
          "timestamp": 1473236880,
          "value": 98.958333
        },
        {
          "timestamp": 1473236940,
          "value": 99.041667
        },
        {
          "timestamp": 1473237000,
          "value": 98.873592
        },
        {
          "timestamp": 1473237060,
          "value": 98.999583
        },
        {
          "timestamp": 1473237120,
          "value": 98.916667
        },
        {
          "timestamp": 1473237180,
          "value": 99.040867
        },
        {
          "timestamp": 1473237240,
          "value": 99.082951
        },
        {
          "timestamp": 1473237300,
          "value": 99.040867
        },
        {
          "timestamp": 1473237360,
          "value": 98.916215
        },
        {
          "timestamp": 1473237420,
          "value": 98.460899
        },
        {
          "timestamp": 1473237480,
          "value": 99.165972
        },
        {
          "timestamp": 1473237540,
          "value": 98.496868
        },
        {
          "timestamp": 1473237600,
          "value": 99.248748
        },
        {
          "timestamp": 1473237660,
          "value": 99.208003
        },
        {
          "timestamp": 1473237720,
          "value": 99.040867
        },
        {
          "timestamp": 1473237780,
          "value": 99.040867
        },
        {
          "timestamp": 1473237840,
          "value": 98.254364
        },
        {
          "timestamp": 1473237900,
          "value": 98.917118
        },
        {
          "timestamp": 1473237960,
          "value": 97.916667
        },
        {
          "timestamp": 1473238020,
          "value": 99.040467
        },
        {
          "timestamp": 1473238080,
          "value": 99.041667
        },
        {
          "timestamp": 1473238140,
          "value": 98.999583
        },
        {
          "timestamp": 1473238200,
          "value": 99.040467
        },
        {
          "timestamp": 1473238260,
          "value": 98.875
        },
        {
          "timestamp": 1473238320,
          "value": 98.916215
        },
        {
          "timestamp": 1473238380,
          "value": null
        },
        {
          "timestamp": 1473238440,
          "value": 98.123436
        },
        {
          "timestamp": 1473238500,
          "value": null
        },
        {
          "timestamp": 1473238560,
          "value": null
        },
        {
          "timestamp": 1473238620,
          "value": 98.666111
        },
        {
          "timestamp": 1473238680,
          "value": null
        },
        {
          "timestamp": 1473238740,
          "value": null
        },
        {
          "timestamp": 1473238800,
          "value": null
        },
        {
          "timestamp": 1473238860,
          "value": 98.582743
        },
        {
          "timestamp": 1473238920,
          "value": null
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "cpu.idle"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.93.92",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": null
        },
        {
          "timestamp": 1473235500,
          "value": 73728.0
        },
        {
          "timestamp": 1473235560,
          "value": 69632.0
        },
        {
          "timestamp": 1473235620,
          "value": 8192.0
        },
        {
          "timestamp": 1473235680,
          "value": 49152.0
        },
        {
          "timestamp": 1473235740,
          "value": 94208.0
        },
        {
          "timestamp": 1473235800,
          "value": 0.0
        },
        {
          "timestamp": 1473235860,
          "value": 73728.0
        },
        {
          "timestamp": 1473235920,
          "value": 65536.0
        },
        {
          "timestamp": 1473235980,
          "value": null
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": 102400.0
        },
        {
          "timestamp": 1473236460,
          "value": 102400.0
        },
        {
          "timestamp": 1473236520,
          "value": 0.0
        },
        {
          "timestamp": 1473236580,
          "value": 245760.0
        },
        {
          "timestamp": 1473236640,
          "value": 106496.0
        },
        {
          "timestamp": 1473236700,
          "value": 53248.0
        },
        {
          "timestamp": 1473236760,
          "value": 36864.0
        },
        {
          "timestamp": 1473236820,
          "value": 106496.0
        },
        {
          "timestamp": 1473236880,
          "value": 131072.0
        },
        {
          "timestamp": 1473236940,
          "value": 102400.0
        },
        {
          "timestamp": 1473237000,
          "value": 36864.0
        },
        {
          "timestamp": 1473237060,
          "value": 36864.0
        },
        {
          "timestamp": 1473237120,
          "value": 16384.0
        },
        {
          "timestamp": 1473237180,
          "value": 16384.0
        },
        {
          "timestamp": 1473237240,
          "value": 16384.0
        },
        {
          "timestamp": 1473237300,
          "value": 16384.0
        },
        {
          "timestamp": 1473237360,
          "value": 16384.0
        },
        {
          "timestamp": 1473237420,
          "value": 16384.0
        },
        {
          "timestamp": 1473237480,
          "value": 12288.0
        },
        {
          "timestamp": 1473237540,
          "value": 53248.0
        },
        {
          "timestamp": 1473237600,
          "value": 135168.0
        },
        {
          "timestamp": 1473237660,
          "value": 16384.0
        },
        {
          "timestamp": 1473237720,
          "value": 49152.0
        },
        {
          "timestamp": 1473237780,
          "value": 73728.0
        },
        {
          "timestamp": 1473237840,
          "value": 139264.0
        },
        {
          "timestamp": 1473237900,
          "value": 126976.0
        },
        {
          "timestamp": 1473237960,
          "value": 294912.0
        },
        {
          "timestamp": 1473238020,
          "value": 159744.0
        },
        {
          "timestamp": 1473238080,
          "value": null
        },
        {
          "timestamp": 1473238140,
          "value": 143360.0
        },
        {
          "timestamp": 1473238200,
          "value": 0.0
        },
        {
          "timestamp": 1473238260,
          "value": 0.0
        },
        {
          "timestamp": 1473238320,
          "value": 0.0
        },
        {
          "timestamp": 1473238380,
          "value": 0.0
        },
        {
          "timestamp": 1473238440,
          "value": 36864.0
        },
        {
          "timestamp": 1473238500,
          "value": null
        },
        {
          "timestamp": 1473238560,
          "value": null
        },
        {
          "timestamp": 1473238620,
          "value": 73728.0
        },
        {
          "timestamp": 1473238680,
          "value": null
        },
        {
          "timestamp": 1473238740,
          "value": null
        },
        {
          "timestamp": 1473238800,
          "value": null
        },
        {
          "timestamp": 1473238860,
          "value": 61440.0
        },
        {
          "timestamp": 1473238920,
          "value": null
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "disk.io.write_bytes/device=sda"
    }
  ],
  "cmdb": [
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.93.95",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": null
        },
        {
          "timestamp": 1473235500,
          "value": null
        },
        {
          "timestamp": 1473235560,
          "value": null
        },
        {
          "timestamp": 1473235620,
          "value": null
        },
        {
          "timestamp": 1473235680,
          "value": null
        },
        {
          "timestamp": 1473235740,
          "value": null
        },
        {
          "timestamp": 1473235800,
          "value": null
        },
        {
          "timestamp": 1473235860,
          "value": null
        },
        {
          "timestamp": 1473235920,
          "value": 0.0
        },
        {
          "timestamp": 1473235980,
          "value": 0.0
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": null
        },
        {
          "timestamp": 1473236520,
          "value": 0.0
        },
        {
          "timestamp": 1473236580,
          "value": 0.0
        },
        {
          "timestamp": 1473236640,
          "value": 0.0
        },
        {
          "timestamp": 1473236700,
          "value": 0.0
        },
        {
          "timestamp": 1473236760,
          "value": 0.0
        },
        {
          "timestamp": 1473236820,
          "value": 0.0
        },
        {
          "timestamp": 1473236880,
          "value": 0.0
        },
        {
          "timestamp": 1473236940,
          "value": 0.0
        },
        {
          "timestamp": 1473237000,
          "value": 0.0
        },
        {
          "timestamp": 1473237060,
          "value": 0.0
        },
        {
          "timestamp": 1473237120,
          "value": 0.0
        },
        {
          "timestamp": 1473237180,
          "value": 0.0
        },
        {
          "timestamp": 1473237240,
          "value": 0.0
        },
        {
          "timestamp": 1473237300,
          "value": 0.0
        },
        {
          "timestamp": 1473237360,
          "value": 0.0
        },
        {
          "timestamp": 1473237420,
          "value": 0.0
        },
        {
          "timestamp": 1473237480,
          "value": 0.0
        },
        {
          "timestamp": 1473237540,
          "value": 0.0
        },
        {
          "timestamp": 1473237600,
          "value": 0.0
        },
        {
          "timestamp": 1473237660,
          "value": null
        },
        {
          "timestamp": 1473237720,
          "value": 0.0
        },
        {
          "timestamp": 1473237780,
          "value": 0.0
        },
        {
          "timestamp": 1473237840,
          "value": 0.0
        },
        {
          "timestamp": 1473237900,
          "value": 0.0
        },
        {
          "timestamp": 1473237960,
          "value": 0.0
        },
        {
          "timestamp": 1473238020,
          "value": 0.0
        },
        {
          "timestamp": 1473238080,
          "value": 0.0
        },
        {
          "timestamp": 1473238140,
          "value": 0.0
        },
        {
          "timestamp": 1473238200,
          "value": 0.0
        },
        {
          "timestamp": 1473238260,
          "value": 0.0
        },
        {
          "timestamp": 1473238320,
          "value": 0.0
        },
        {
          "timestamp": 1473238380,
          "value": 0.0
        },
        {
          "timestamp": 1473238440,
          "value": null
        },
        {
          "timestamp": 1473238500,
          "value": 0.0
        },
        {
          "timestamp": 1473238560,
          "value": null
        },
        {
          "timestamp": 1473238620,
          "value": 0.0
        },
        {
          "timestamp": 1473238680,
          "value": 0.0
        },
        {
          "timestamp": 1473238740,
          "value": 0.0
        },
        {
          "timestamp": 1473238800,
          "value": null
        },
        {
          "timestamp": 1473238860,
          "value": 0.0
        },
        {
          "timestamp": 1473238920,
          "value": 0.0
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "disk.io.read_bytes/device=sda"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.93.95",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": null
        },
        {
          "timestamp": 1473235500,
          "value": null
        },
        {
          "timestamp": 1473235560,
          "value": null
        },
        {
          "timestamp": 1473235620,
          "value": null
        },
        {
          "timestamp": 1473235680,
          "value": null
        },
        {
          "timestamp": 1473235740,
          "value": null
        },
        {
          "timestamp": 1473235800,
          "value": null
        },
        {
          "timestamp": 1473235860,
          "value": null
        },
        {
          "timestamp": 1473235920,
          "value": 97.666667
        },
        {
          "timestamp": 1473235980,
          "value": 100.0
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": null
        },
        {
          "timestamp": 1473236520,
          "value": 97.25229
        },
        {
          "timestamp": 1473236580,
          "value": 100.0
        },
        {
          "timestamp": 1473236640,
          "value": 96.875
        },
        {
          "timestamp": 1473236700,
          "value": 96.875
        },
        {
          "timestamp": 1473236760,
          "value": 97.541667
        },
        {
          "timestamp": 1473236820,
          "value": 99.833333
        },
        {
          "timestamp": 1473236880,
          "value": 98.000833
        },
        {
          "timestamp": 1473236940,
          "value": 99.750208
        },
        {
          "timestamp": 1473237000,
          "value": 96.752706
        },
        {
          "timestamp": 1473237060,
          "value": 99.875052
        },
        {
          "timestamp": 1473237120,
          "value": 98.083333
        },
        {
          "timestamp": 1473237180,
          "value": 99.875052
        },
        {
          "timestamp": 1473237240,
          "value": 98.333333
        },
        {
          "timestamp": 1473237300,
          "value": 96.876302
        },
        {
          "timestamp": 1473237360,
          "value": 96.833333
        },
        {
          "timestamp": 1473237420,
          "value": 99.916736
        },
        {
          "timestamp": 1473237480,
          "value": 96.834652
        },
        {
          "timestamp": 1473237540,
          "value": 99.833333
        },
        {
          "timestamp": 1473237600,
          "value": 96.875
        },
        {
          "timestamp": 1473237660,
          "value": 99.833403
        },
        {
          "timestamp": 1473237720,
          "value": 98.958333
        },
        {
          "timestamp": 1473237780,
          "value": 99.833333
        },
        {
          "timestamp": 1473237840,
          "value": 99.166667
        },
        {
          "timestamp": 1473237900,
          "value": 96.583333
        },
        {
          "timestamp": 1473237960,
          "value": 96.833333
        },
        {
          "timestamp": 1473238020,
          "value": 100.0
        },
        {
          "timestamp": 1473238080,
          "value": 97.209496
        },
        {
          "timestamp": 1473238140,
          "value": 100.0
        },
        {
          "timestamp": 1473238200,
          "value": 96.583333
        },
        {
          "timestamp": 1473238260,
          "value": 99.958351
        },
        {
          "timestamp": 1473238320,
          "value": 97.5
        },
        {
          "timestamp": 1473238380,
          "value": 99.833333
        },
        {
          "timestamp": 1473238440,
          "value": 99.000416
        },
        {
          "timestamp": 1473238500,
          "value": 96.543107
        },
        {
          "timestamp": 1473238560,
          "value": null
        },
        {
          "timestamp": 1473238620,
          "value": 99.791753
        },
        {
          "timestamp": 1473238680,
          "value": 97.0
        },
        {
          "timestamp": 1473238740,
          "value": 99.958351
        },
        {
          "timestamp": 1473238800,
          "value": null
        },
        {
          "timestamp": 1473238860,
          "value": 99.833333
        },
        {
          "timestamp": 1473238920,
          "value": 98.293089
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "cpu.idle"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.93.95",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": null
        },
        {
          "timestamp": 1473235500,
          "value": null
        },
        {
          "timestamp": 1473235560,
          "value": null
        },
        {
          "timestamp": 1473235620,
          "value": null
        },
        {
          "timestamp": 1473235680,
          "value": null
        },
        {
          "timestamp": 1473235740,
          "value": null
        },
        {
          "timestamp": 1473235800,
          "value": null
        },
        {
          "timestamp": 1473235860,
          "value": null
        },
        {
          "timestamp": 1473235920,
          "value": 1.916667
        },
        {
          "timestamp": 1473235980,
          "value": 0.0
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": null
        },
        {
          "timestamp": 1473236520,
          "value": 2.164863
        },
        {
          "timestamp": 1473236580,
          "value": 0.0
        },
        {
          "timestamp": 1473236640,
          "value": 3.041667
        },
        {
          "timestamp": 1473236700,
          "value": 3.041667
        },
        {
          "timestamp": 1473236760,
          "value": 2.0
        },
        {
          "timestamp": 1473236820,
          "value": 0.0
        },
        {
          "timestamp": 1473236880,
          "value": 1.79092
        },
        {
          "timestamp": 1473236940,
          "value": 0.041632
        },
        {
          "timestamp": 1473237000,
          "value": 3.122398
        },
        {
          "timestamp": 1473237060,
          "value": 0.041649
        },
        {
          "timestamp": 1473237120,
          "value": 1.75
        },
        {
          "timestamp": 1473237180,
          "value": 0.041649
        },
        {
          "timestamp": 1473237240,
          "value": 1.416667
        },
        {
          "timestamp": 1473237300,
          "value": 3.0404
        },
        {
          "timestamp": 1473237360,
          "value": 2.583333
        },
        {
          "timestamp": 1473237420,
          "value": 0.041632
        },
        {
          "timestamp": 1473237480,
          "value": 2.540608
        },
        {
          "timestamp": 1473237540,
          "value": 0.0
        },
        {
          "timestamp": 1473237600,
          "value": 3.041667
        },
        {
          "timestamp": 1473237660,
          "value": 0.041649
        },
        {
          "timestamp": 1473237720,
          "value": 0.958333
        },
        {
          "timestamp": 1473237780,
          "value": 0.041667
        },
        {
          "timestamp": 1473237840,
          "value": 0.75
        },
        {
          "timestamp": 1473237900,
          "value": 3.125
        },
        {
          "timestamp": 1473237960,
          "value": 2.625
        },
        {
          "timestamp": 1473238020,
          "value": 0.0
        },
        {
          "timestamp": 1473238080,
          "value": 2.290712
        },
        {
          "timestamp": 1473238140,
          "value": 0.0
        },
        {
          "timestamp": 1473238200,
          "value": 3.083333
        },
        {
          "timestamp": 1473238260,
          "value": 0.0
        },
        {
          "timestamp": 1473238320,
          "value": 2.125
        },
        {
          "timestamp": 1473238380,
          "value": 0.041667
        },
        {
          "timestamp": 1473238440,
          "value": 0.791337
        },
        {
          "timestamp": 1473238500,
          "value": 3.123698
        },
        {
          "timestamp": 1473238560,
          "value": null
        },
        {
          "timestamp": 1473238620,
          "value": 0.041649
        },
        {
          "timestamp": 1473238680,
          "value": 2.5
        },
        {
          "timestamp": 1473238740,
          "value": 0.041649
        },
        {
          "timestamp": 1473238800,
          "value": null
        },
        {
          "timestamp": 1473238860,
          "value": 0.041667
        },
        {
          "timestamp": 1473238920,
          "value": 1.540383
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "cpu.user"
    },
    {
      "dstype": "GAUGE",
      "step": 60,
      "endpoint": "10.126.93.95",
      "Values": [
        {
          "timestamp": 1473235380,
          "value": null
        },
        {
          "timestamp": 1473235440,
          "value": null
        },
        {
          "timestamp": 1473235500,
          "value": null
        },
        {
          "timestamp": 1473235560,
          "value": null
        },
        {
          "timestamp": 1473235620,
          "value": null
        },
        {
          "timestamp": 1473235680,
          "value": null
        },
        {
          "timestamp": 1473235740,
          "value": null
        },
        {
          "timestamp": 1473235800,
          "value": null
        },
        {
          "timestamp": 1473235860,
          "value": null
        },
        {
          "timestamp": 1473235920,
          "value": 0.0
        },
        {
          "timestamp": 1473235980,
          "value": 86016.0
        },
        {
          "timestamp": 1473236040,
          "value": null
        },
        {
          "timestamp": 1473236100,
          "value": null
        },
        {
          "timestamp": 1473236160,
          "value": null
        },
        {
          "timestamp": 1473236220,
          "value": null
        },
        {
          "timestamp": 1473236280,
          "value": null
        },
        {
          "timestamp": 1473236340,
          "value": null
        },
        {
          "timestamp": 1473236400,
          "value": null
        },
        {
          "timestamp": 1473236460,
          "value": null
        },
        {
          "timestamp": 1473236520,
          "value": 0.0
        },
        {
          "timestamp": 1473236580,
          "value": 0.0
        },
        {
          "timestamp": 1473236640,
          "value": 0.0
        },
        {
          "timestamp": 1473236700,
          "value": 0.0
        },
        {
          "timestamp": 1473236760,
          "value": 98304.0
        },
        {
          "timestamp": 1473236820,
          "value": 0.0
        },
        {
          "timestamp": 1473236880,
          "value": 0.0
        },
        {
          "timestamp": 1473236940,
          "value": 0.0
        },
        {
          "timestamp": 1473237000,
          "value": 0.0
        },
        {
          "timestamp": 1473237060,
          "value": 0.0
        },
        {
          "timestamp": 1473237120,
          "value": 163840.0
        },
        {
          "timestamp": 1473237180,
          "value": 0.0
        },
        {
          "timestamp": 1473237240,
          "value": 0.0
        },
        {
          "timestamp": 1473237300,
          "value": 45056.0
        },
        {
          "timestamp": 1473237360,
          "value": 0.0
        },
        {
          "timestamp": 1473237420,
          "value": 0.0
        },
        {
          "timestamp": 1473237480,
          "value": 73728.0
        },
        {
          "timestamp": 1473237540,
          "value": 0.0
        },
        {
          "timestamp": 1473237600,
          "value": 106496.0
        },
        {
          "timestamp": 1473237660,
          "value": 0.0
        },
        {
          "timestamp": 1473237720,
          "value": 0.0
        },
        {
          "timestamp": 1473237780,
          "value": 0.0
        },
        {
          "timestamp": 1473237840,
          "value": 122880.0
        },
        {
          "timestamp": 1473237900,
          "value": 57344.0
        },
        {
          "timestamp": 1473237960,
          "value": 0.0
        },
        {
          "timestamp": 1473238020,
          "value": 0.0
        },
        {
          "timestamp": 1473238080,
          "value": 0.0
        },
        {
          "timestamp": 1473238140,
          "value": 49152.0
        },
        {
          "timestamp": 1473238200,
          "value": 790528.0
        },
        {
          "timestamp": 1473238260,
          "value": 49152.0
        },
        {
          "timestamp": 1473238320,
          "value": 45056.0
        },
        {
          "timestamp": 1473238380,
          "value": 49152.0
        },
        {
          "timestamp": 1473238440,
          "value": null
        },
        {
          "timestamp": 1473238500,
          "value": 0.0
        },
        {
          "timestamp": 1473238560,
          "value": null
        },
        {
          "timestamp": 1473238620,
          "value": 0.0
        },
        {
          "timestamp": 1473238680,
          "value": 0.0
        },
        {
          "timestamp": 1473238740,
          "value": 0.0
        },
        {
          "timestamp": 1473238800,
          "value": null
        },
        {
          "timestamp": 1473238860,
          "value": 0.0
        },
        {
          "timestamp": 1473238920,
          "value": 139264.0
        },
        {
          "timestamp": 1473238980,
          "value": null
        }
      ],
      "counter": "disk.io.write_bytes/device=sda"
    }
  ]
};

 $('#pool').highcharts({
         chart: {
            zoomType: 'x'
        },
        title: {
            text: 'disk.io.read_bytes/device=sda'
        },
        xAxis: {
            type: 'datetime'
        },
        yAxis: {
            title: {
                text: ' '
            }
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            area: {
                fillColor: {
                    linearGradient: {
                        x1: 0,
                        y1: 0,
                        x2: 0,
                        y2: 1
                    },
                    stops: [
                        [0, Highcharts.getOptions().colors[0]],
                        [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                    ]
                },
                marker: {
                    radius: 2
                },
                lineWidth: 1,
                states: {
                    hover: {
                        lineWidth: 1
                    }
                },
                threshold: null
            }
        },

        series: [{
            name: data.squid[0].endpoint,
            data: data.squid[0].Values
        }]

 });
