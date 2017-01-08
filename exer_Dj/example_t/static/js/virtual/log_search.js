var vue = new Vue({
    mixins: [OcaMixin],

    el: "#vue_log_search",
    data: {
        ops_logs: [],
        next_page: null,     // 上一页
        previous_page: null, // 下一页
        current_page: null,
        fetching_logs: false,
        page_count: null,
        PAGE_SIZE: 20,
    },

    watch: {
        'current_page': function (val, oldVal) {
            let _vue = window._vue;
            val = parseInt(val);
            let page_num = _vue.page_count;
            if (val > page_num) {
                _vue.current_page = page_num;
            }
            else if (!val) {
                _vue.current_page = 1;
            }
            else {
                if (val < 1) {
                    _vue.current_page = 1;
                }
            }
        },
    },

    methods: {

        add_watch: function () {
            let _vue = window._vue;
            _vue.$watch('current_zone', (val, oldVal) = > {
                let _vue = window._vue;
            console.log(`change zone to: ${_vue.zones[val].template.endpoint}`);
            Promise.resolve().then(_vue.cluster_list).then(() = > {
                _vue.list_logs()
        })
            ;
        })
        },


        cluster_change: function () {
            let _vue = window._vue;
            let cluster = $('#cluster').val();
            if (_vue.current_cluster == cluster) {
                return;
            }
            _vue.current_cluster = cluster;
            console.log(`change cluster to: ${_vue.current_cluster}`);
            _vue.list_logs();
        },


        // 生成日志过滤参数
        gen_log_filters: function () {
            let _vue = window._vue;
            let filters = {};
            // 按照zone过滤
            let zone = _vue.zones[_vue.current_zone];
            if (zone.template.endpoint != '-1') {
                filters.zone_name = zone.name
            }
            // 按照cluster过滤
            if (_vue.current_cluster != '-1') {
                filters.cluster_name = _vue.current_cluster;
            }
            return filters
        },


        // url: djangorest返回的带分页信息的url, 例如: http://127.0.0.1:8000/api/operation_logs/?page=2
        //      没有的话默认显示第一页
        api_operation_logs: function (filters = null, page_num = null) {
            let filter_url;
            if (page_num) {
                filter_url = `?page=${page_num}&`;
            }
            else {
                filter_url = '?';
            }

            if (filters) {
                for (let k in filters) {
                    filter_url += `${k}=${filters[k]}&`;
                }
            }
            console.log('log filter_url: ' + filter_url);
            return Vue.http.get(`/api/operation_logs/${filter_url}`)
        },


        list_logs: function (page_num = 1, extra_filters = null) {
            let _vue = window._vue;
            _vue.fetching_logs = true;
            _vue.ops_logs = [];
            let filters = _vue.gen_log_filters();
            if (extra_filters) {
                filters = $.extend(filters, extra_filters);
            }
            _vue.next_page = null;
            _vue.previous_page = null;

            return _vue.api_operation_logs(filters, page_num).then(response = > {
                    let ops_logs_info = response.json();
            let ops_logs = ops_logs_info['results'];
            _vue.page_count = Math.ceil(ops_logs_info['count'] / _vue.PAGE_SIZE);


            // 获取分页信息
            let next = new RegExp("page=[0-9]+").exec(ops_logs_info['next']);
            if (next) {
                _vue.next_page = next[0].split('=')[1]

            }
            let previous = new RegExp("page=[0-9]+").exec(ops_logs_info['previous']);
            if (previous) {
                _vue.previous_page = previous[0].split('=')[1]
            }

            let promises_vmInfo = [];
            let unique_vmIds = [];  // 【zoneId_vmId, ..】
            for (let x = 0; x < ops_logs.length; x++) {
                if (!ops_logs[x].vm_id) {
                    continue;
                }

                // 获取vm_id所属的zone
                let zone;
                for (z of _vue.zones) {
                    if (z.template.endpoint == ops_logs[x].rpc_endpoint) {
                        zone = z;
                        break;
                    }
                }
                if (!zone) {
                    console.error("could not get zone obj by rpc_endpoint: " + ops_logs[x].rpc_endpoint);
                    continue;
                }

                // 获取不重复的vm_ids,避免重复调用api_vm_info
                let zoneId_vmId = `${zone.id}_${ops_logs[x].vm_id}`;
                if ($.inArray(zoneId_vmId, unique_vmIds) == -1) {
                    unique_vmIds.push(zoneId_vmId);
                    promises_vmInfo.push(_vue.api_vm_info(ops_logs[x].vm_id, zone));
                }
            }

            // 给ops_log加上vm属性
            return Promise.all(promises_vmInfo).then(_vue.attach_host_to_vm).then(vms = > {
                for (let x = 0;
            x < ops_logs.length;
            x++
            )
            {
                for (vm of vms) {
                    if (vm.id == ops_logs[x].vm_id) {
                        ops_logs[x].vm = vm;
                        break;
                    }
                }
            }
            _vue.ops_logs = ops_logs;
            _vue.current_page = page_num;
            _vue.fetching_logs = false;
        })
            ;
        })


        },


        filter_by_orderId: function (order_id) {
            let _vue = window._vue;
            let filters = {'order_id': order_id};
            _vue.list_logs(1, filters)
        },


    },


    ready() {
        window._vue = this;
        let _vue = this;
        _vue.enable_zone_all = true;
        _vue.enable_cluster_all = true;
        _vue.zone_list()
            .then(this.cluster_list)
            .then(_vue.list_logs)
            .then(_vue.add_watch);
        // Vue.http.get('/api/operation_logs/').then((response) => {
        //     _vue.ops_logs = response.json();
        // });
        $('[data-rel=tooltip]').tooltip();
    }
});
