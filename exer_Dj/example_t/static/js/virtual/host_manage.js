var vue = new Vue({
    mixins: [OcaMixin],

    el: "#vue_hostpool_manage",
    data: {
        hosts: [],
        selected_hosts: [],
        vm_num: null,
        enable_zone_all: true,
        enable_cluster_all: true,
        fetching_hosts: false,
        search: null,
        HOST_STYLE: {
            null: 'label-success',
            undefined: 'label-success',
            '': 'label-success',
            'online': 'label-success',
            'offline': 'label-default ',
            'block': 'label-warning ',
            'maintain': 'label-warning ',
        }

    },


    methods: {


        add_watch: function () {
            let _vue = window._vue;
            _vue.$watch('current_zone', function (val, oldVal) {
                console.log(`change zone to: ${_vue.zones[val].template.endpoint}`);
                _vue.stop_refreshing_vm_status = true;
                Promise.resolve().then(_vue.cluster_list)
                    .then(_vue.host_list)
                    .then(() => {
                        _vue.stop_refreshing_vm_status = false;
                    });
            });
        },


        cluster_change: function () {
            let _vue = window._vue;
            let cluster = $('#cluster').val();
            if (_vue.current_cluster == cluster) {
                return;
            }
            _vue.current_cluster = cluster;
            console.log(`change cluster to: ${_vue.current_cluster}`);
            _vue.host_list();
        },


        host_list: function () {
            let _vue = window._vue;
            _vue.fetching_hosts = true;
            _vue.search = null;
            _vue.hosts = [];
            let zones;
            let zone = _vue.zones[_vue.current_zone];
            if (zone.template.endpoint == '-1') {
                zones = _vue.zones.filter(x => {
                    return (x.template.endpoint != '-1');
                });
            }
            else {
                zones = [zone];
            }

            let cluster;
            if (zone.template.endpoint == '-1' || _vue.current_cluster == '-1') {
                cluster = null
            }
            else {
                cluster = _vue.current_cluster;
            }

            let promise_hosts = zones.map(x => {
                return _vue.hostpool_info(x, cluster);
            });
            return Promise.all(promise_hosts).then((hosts_list) => {
                _vue.hosts = hosts_list[0].concat(...hosts_list.splice(1));
                _vue.fetching_hosts = false;
            });
        },


        //计算保百分比,保留2位小数
        math_round: function (num) {
            return (100 * (Math.round(num * 100) / 100)).toFixed(2);
        },


        //点击操作按钮时弹框提醒
        host_custom_state: function (state) {
            let host_str = '';
            let _vue = window._vue;
            if (_vue.selected_hosts.length == 0) {
                bootbox.confirm(`请先选择需要操作的机器！`, function (ok) {
                    if (ok) {
                        return;
                    }
                });
            }
            else {
                for (let index in _vue.selected_hosts) {
                    let [zone_id, host_id] = _vue.selected_hosts[index].split('_');
                    for (let i = 0; i < _vue.hosts.length; i++) {
                        if (_vue.hosts[i].id == host_id) {
                            host_str = host_str + _vue.hosts[i].template.hostname + '<br/>';
                            break;
                        }
                    }
                }
                bootbox.confirm(`确定要对以下宿主机：<br/>${host_str}执行${state}操作?`, function (ok) {
                    if (ok) {
                        let order_id = _vue.gen_uuid();
                        let promise_actions = [];
                        _vue.selected_hosts.forEach(zone_vm => {
                            let [zone_id, host_id] = zone_vm.split('_');
                            let zone = _vue.zones.filter(x => {
                                return x.id == zone_id;
                            })[0];
                            let template = `CUSTOM_STATE=${state}`;
                            let p = _vue.api_host_update(zone, host_id, template, true, order_id).then(
                                response => {
                                    _vue.push_notice('alert-success', `id:${host_id} => ${state}成功`, 10000)
                                },
                                response => {
                                    _vue.push_notice('alert-warning', `id:${host_id} => ${state}失败。${response.text()}`, 10000)
                                }
                            );
                            promise_actions.push(p);
                        });
                        Promise.all(promise_actions).then(()=> {
                            _vue.host_list();
                        });
                    }
                });
            }

        },


        //弹出框获取设置的VM数量
        set_vm_num: function () {
            let _vue = window._vue;
            if (_vue.selected_hosts.length == 0) {
                bootbox.confirm(`请先选择需要操作的机器！`, function (result) {
                    if (result) {
                        return;
                    }
                });
            }
            let order_id = _vue.gen_uuid();
            let promise_maxVms = [];
            for (let index in _vue.selected_hosts) {
                let zone_vm = _vue.selected_hosts[index];
                let [zone_id, host_id] = zone_vm.split('_');
                let zone = _vue.zones.filter(x => {
                    return x.id == zone_id;
                })[0];
                promise_maxVms.push(_vue.host_max_vms(zone, host_id, _vue.vm_num, order_id));
            }
            Promise.all(promise_maxVms).then(() => {
                _vue.host_list()
            });
        },


        // 设置host可以创建的vm数量
        host_max_vms: function (zone, id, num, order_id) {
            let _vue = window._vue;
            let template = `MAX_VMS=${num}`;
            return _vue.api_host_update(zone, id, template, true, order_id).then(
                response => {
                    _vue.push_notice('alert-success', `id:${id} => 成功`, 10000)
                },
                response => {
                    _vue.push_notice('alert-warning', `id:${id} => ${response.text()}`, 10000)
                }
            );
        },


        //表格全选
        check_all: function () {
            let _vue = window._vue;
            let checkbox = $('input:checkbox');
            let flag = checkbox[0].checked;
            if (flag) {
                for (let ind = 1; ind < checkbox.length; ind++) {
                    _vue.selected_hosts.push(checkbox[ind].value);
                }
            }
            else {
                _vue.selected_hosts = [];
            }

        },


        host_sort: function (key, convert = null) {
            _vue.hosts = _vue.sort_by(_vue.hosts, key, convert);
        },


    },


    ready()
    {
        window._vue = this;
        this.zone_list()
            .then(this.cluster_list)
            .then(this.host_list)
            .then(this.add_watch);
    }


});

