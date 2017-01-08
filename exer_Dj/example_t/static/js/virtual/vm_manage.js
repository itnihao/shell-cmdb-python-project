var vue = new Vue({
        mixins: [OcaMixin],

        el: "#vue_host_manage",
        data: {
            selected_vms: [],   // 选中的vm
            // notice: [],     // 通知
            notice: '',
            vm_state: '',
            VM_STATUS_COLOR: {
                3: 'label-success',
            },
            fetching_vms: false,
            search: null,
        },


        methods: {
            add_watch: function () {
                let _vue = window._vue;
                _vue.$watch('current_zone', function (val, oldVal) {
                    console.log(`change zone to: ${_vue.zones[val].template.endpoint}`);
                    _vue.stop_refreshing_vm_status = true;
                    Promise.resolve().then(_vue.cluster_list)
                        .then(_vue.vm_list)
                        .then(() => {
                            _vue.stop_refreshing_vm_status = false;
                        });
                });
            },

            // 使用click而不是watch来变更current_cluster,原因更新zone的时候可能会触发cluster的watcher,导致重复请求。
            cluster_change: function () {
                let _vue = window._vue;
                let cluster = $('#cluster').val();
                if (_vue.current_cluster == cluster) {
                    return;
                }
                _vue.current_cluster = cluster;
                console.log(`change cluster to: ${_vue.current_cluster}`);
                _vue.stop_refreshing_vm_status = true;
                _vue.vm_list()
                    .then(() => {
                        _vue.stop_refreshing_vm_status = false;
                    });
            },


            vm_action: function (action) {

                let _vue = window._vue;
                if (_vue.selected_vms.length == 0) {
                    bootbox.confirm(`请先选择需要操作的云主机！`, function (result) {
                        if (result) {
                            return;
                        }
                    });
                }
                else {
                    let vmId__index = {};
                    let vms = [];
                    let name_str = '';
                    let action_dic = {
                        reboot: '重启',
                        delete: '删除',
                        resume: '开机',
                        poweroff: '关机',
                        delete_recreate: '重装系统',
                        reset_key: '重置密码',
                        open_net: '开通外网'
                    };


                    // for (let zid_vid of _vue.selected_vms) {  // index在promise里面是lazy的,即只能获取最后一个index值
                    for (let index in _vue.selected_vms) {
                        // 根据zone_id和vm_id查找vm
                        // [zone_id, vm_id] = zid_vid.split('_');
                        [zone_id, vm_id] = _vue.selected_vms[index].split('_');
                        zone_id = parseInt(zone_id);
                        vm_id = parseInt(vm_id);//vm;
                        for (let x = 0; x < _vue.vms.length; x++) {
                            if (_vue.vms[x].id == vm_id && _vue.vms[x].zone.id == zone_id) {
                                vms[index] = _vue.vms[x];
                                vmId__index[_vue.vms[x].id] = x;
                                name_str = name_str + vms[index].name + "<br/>";
                                break;
                            }
                        }
                    }
                    bootbox.confirm(`确定要对以下虚拟机：<br/> ${name_str} 执行${action_dic[action]}操作?`, function (result) {
                            if (result) {
                                let order_id = _vue.gen_uuid();
                                for (let ind in vms) {
                                    // 执行action
                                    _vue.api_vm_action(vms[ind].zone, vms[ind], action, order_id).then(
                                        (result) => {
                                            let vm_id = result.vm_id;
                                            let vm_state;
                                            if (result.success) {
                                                // _vue.push_notice(`${_vue.vms[vmId__index[vm_id]].name} => ${action}成功`);
                                                _vue.notice = `${_vue.vms[vmId__index[vm_id]].name} => ${action}成功`;
                                                console.log("vue.notice" + _vue.notice);
                                                vm_state = (`alert-success`);
                                            }
                                            else {
                                                _vue.notice = `${_vue.vms[vmId__index[vm_id]].name} => ${action}失败:${result.detail}`;
                                                console.log("vue.notice" + _vue.notice);
                                                vm_state = (`alert-warning`);
                                                // _vue.push_notice(`${_vue.vms[vmId__index[vm_id]].name} => ${action}失败:${result.detail}`);
                                            }
                                            _vue.push_notice(vm_state, _vue.notice, 10000);
                                        }
                                    );
                                }
                            }
                        }
                    );
                }

            },


            vm_list: function () {
                let _vue = this;
                _vue.fetching_vms = true;
                let dc_list;
                _vue.search = null;
                let cluster;
                let dc = _vue.zones[_vue.current_zone];
                if (dc.template.endpoint == '-1') {
                    dc_list = _vue.zones.filter(x => {
                        return x.template.endpoint != '-1'
                    });
                }
                else {
                    dc_list = [dc];
                }

                if (dc.template.endpoint == '-1' || _vue.current_cluster == '-1') {
                    cluster = null
                }
                else {
                    cluster = _vue.current_cluster;
                }

                let promises = dc_list.map(x => {
                    return _vue.api_vmpool_info(x, cluster);
                });
                return Promise.all(promises).then((vms_list) => {
                    _vue.vms = vms_list[0].concat(...vms_list.splice(1));
                    _vue.fetching_vms = false;
                });
            },


            //表格全选
            check_all: function () {
                let _vue = window._vue;
                let checkbox = $('input:checkbox');
                let flag = checkbox[0].checked;
                if (flag) {
                    for (let ind = 1; ind < checkbox.length; ind++) {
                        _vue.selected_vms.push(checkbox[ind].value);
                    }
                }
                else {
                    _vue.selected_vms = [];
                }

            }
            ,


            vnc_click: function (rpc_endpoint, vm_id) {
                let _vue = window._vue;
                Vue.http.post(`/vnc?rpc_endpoint=${rpc_endpoint}&vm_id=${vm_id}`).then(response => {
                    vnc_info = response.json();
                    window.open(`/vnc?host=${vnc_info.host}&port=${vnc_info.port}&token=${vnc_info.token}&title=${vnc_info.vm_name}`);
                });
            }
            ,

        },


        ready()
        {
            window._vue = this;
            _vue.enable_zone_all = true;
            _vue.enable_cluster_all = true;
            this.zone_list()
                .then(this.cluster_list)
                .then(this.vm_list)
                .then(this.refresh_vm_status)
                .then(this.add_watch);
        }


    })
    ;

