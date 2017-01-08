Vue.config.delimiters = ["[[", "]]"];
Vue.config.unsafeDelimiters = ['[[[', ']]]'];

var OcaMixin = {
    data: {
        vms: [],
        current_zone: null,   // zones列表索引
        zones: [],
        enable_zone_all: false,  // 多一个显示所有数据中心的选项
        clusters: [],
        current_cluster: null,
        enable_cluster_all: false,     // 多一个显示所有集群的选项
        images: [],
        current_image: -1,
        current_image_name: null,
        templates: [],
        current_template: null,
        current_template_name: null,
        osFamilies: [],
        current_osFamily: null,
        vmtypes: [],
        current_vmtype: null,
        current_vmtype_name: null,

        // 刷新虚拟机状态相关参数
        refreshing_vm_status: false,        // 用于在前端显示状态提示条
        stop_refreshing_vm_status: false,   // false则中断刷新虚拟机状态
        refresh_interval: 5000,                 // 刷新间隔(ms)

        order_reverse: '',    // 反转排序

        VM_STATUS: {
            0: 'INIT',
            1: 'PENDING',
            2: 'HOLD',
            3: 'ACTIVE',
            4: 'STOPPED',
            5: 'SUSPENDED',
            6: 'DONE',
            7: 'FAILED',
            8: 'POWEROFF',
        },

        HOST_STATUS: {
            0: '运行',
            1: '运行',
            2: '运行 ',
            3: '维修 ',
            4: '下线 ',
            5: '运行',
            6: '运行',
            7: '运行'
            // '锁住'
        },

        LCM_VM_STATUS: {
            0: 'LCM_INIT',
            1: 'PROLOG',
            2: 'BOOT',
            3: 'RUNNING',
            4: 'MIGRATE',
            5: 'SAVE_STOP',
            6: 'SAVE_SUSPEND',
            7: 'SAVE_MIGRATE',
            8: 'PROLOG_MIGRATE',
            9: 'PROLOG_RESUME',
            10: 'EPILOG_STOP',
            11: 'EPILOG',
            12: 'SHUTDOWN',
            13: 'CANCEL',
            14: 'FAILURE',
            15: 'DELETE',
            16: 'UNKNOWN',
            17: 'HOTPLUG',
            18: 'SHUTDOWN_POWEROFF',
            19: 'BOOT_UNKNOWN',
            20: 'BOOT_POWEROFF',
            21: 'BOOT_SUSPENDED',
            22: 'BOOT_STOPPED',
            23: 'CLEANUP_DELETE',
            24: 'HOTPLUG_SNAPSHOT',
            25: 'HOTPLUG_NIC',
            26: 'HOTPLUG_SAVEAS',
            27: 'HOTPLUG_SAVEAS_POWEROFF',
            28: 'HOTPLUG_SAVEAS_SUSPENDED',
            29: 'SHUTDOWN_UNDEPLOY',
            30: 'EPILOG_UNDEPLOY',
            31: 'PROLOG_UNDEPLOY',
            32: 'BOOT_UNDEPLOY',
            33: 'HOTPLUG_PROLOG_POWEROFF',
            34: 'HOTPLUG_EPILOG_POWEROFF',
            35: 'BOOT_MIGRATE',
            36: 'BOOT_FAILURE',
            37: 'BOOT_MIGRATE_FAILURE',
            38: 'PROLOG_MIGRATE_FAILURE',
            39: 'PROLOG_FAILURE',
            40: 'EPILOG_FAILURE',
            41: 'EPILOG_STOP_FAILURE',
            42: 'EPILOG_UNDEPLOY_FAILURE',
            43: 'PROLOG_MIGRATE_POWEROFF',
            44: 'PROLOG_MIGRATE_POWEROFF_FAILURE',
            45: 'PROLOG_MIGRATE_SUSPEND',
            46: 'PROLOG_MIGRATE_SUSPEND_FAILURE',
            47: 'BOOT_UNDEPLOY_FAILURE',
            48: 'BOOT_STOPPED_FAILURE',
            49: 'PROLOG_RESUME_FAILURE',
            50: 'PROLOG_UNDEPLOY_FAILURE',
            51: 'DISK_SNAPSHOT_POWEROFF',
            52: 'DISK_SNAPSHOT_REVERT_POWEROFF',
            53: 'DISK_SNAPSHOT_DELETE_POWEROFF',
            54: 'DISK_SNAPSHOT_SUSPENDED',
            55: 'DISK_SNAPSHOT_REVERT_SUSPENDED',
            56: 'DISK_SNAPSHOT_DELETE_SUSPENDED',
            57: 'DISK_SNAPSHOT',
            59: 'DISK_SNAPSHOT_DELETE',
            60: 'PROLOG_MIGRATE_UNKNOWN',
            61: 'PROLOG_MIGRATE_UNKNOWN_FAILURE',
        },

    },

    methods: {
        api_vm_info: function (vm_id, zone, hosts = null) {
            let _vue = this;
            return _vue.$http.get(`/api/vm_info/${vm_id}/?rpc_endpoint=${zone.template.endpoint}`)
                .then((response) => {
                    let vm = response.json();
                    return vm
                })
                .then((vm) => {
                    // 判断虚拟机在哪台宿主机上
                    let target_host;
                    if (hosts) {
                        for (let host_ix = 0; host_ix < hosts.length; host_ix++) {
                            if ($.inArray(vm_id, hosts[host_ix].vm_ids) >= 0) {
                                target_host = hosts[host_ix];
                                break;
                            }
                        }
                    }
                    vm.host = target_host;
                    vm.zone = zone;
                    return vm;
                });
        },


        // 列出虚拟机
        api_vmpool_info: function (dc, cluster = null) {
            let _vue = window._vue;
            let url = `/api/vmpool_info/?rpc_endpoint=${dc.template.endpoint}`;
            // if (cluster){
            //     url += `&filter_user_template.cluster=${cluster}`;
            // }
            return Vue.http.get(url).then((response) => {
                let vms = response.json();
                for (let i = 0; i < vms.length; i++) {
                    vms[i].zone = dc;
                }

                // 关联host信息到vm上
                return _vue.attach_host_to_vm(vms).then(vms => {
                    // 按照cluster过滤vms
                    if (cluster) {
                        // vms = [for (vm of vms) if  (vm.hasOwnProperty('host') && vm.host.cluster == cluster) vm];
                        vms = vms.filter(vm => {
                            return (vm.hasOwnProperty('host') && vm.host.cluster == cluster)
                        });
                    }
                    return vms;
                });
            });
        },


        // 关联host到vm上
        attach_host_to_vm: function (vms) {
            return vue.zone_hosts(vms).then((zone_hosts) => {
                for (let i = 0; i < vms.length; i++) {
                    let hosts = zone_hosts[vms[i].zone.id];
                    for (let j = 0; j < hosts.length; j++) {
                        if ($.inArray(vms[i].id, hosts[j].vm_ids) >= 0) {
                            vms[i].host = hosts[j];
                            break;
                        }
                    }
                }
                return vms;
            });
        },


        // 基于模板创建虚拟机
        api_template_instantiate: function (zone, data) {
            return Vue.http.post(`/api/template_instantiate/?rpc_endpoint=${zone.template.endpoint}`, data).then(
                (response) => {
                    return {
                        success: true,
                        detail: response.json().detail,
                    };
                },
                (response) => {
                    return {
                        success: false,
                        detail: response.text(),
                    };
                }
            );
        },


        hostpool_info: function (zone, cluster = null) {
            return Vue.http.get(`/api/hostpool_info/?rpc_endpoint=${zone.template.endpoint}`).then((response) => {
                let result = [];
                let hosts = response.json();
                hosts.forEach(host => {
                    if (!cluster || host.cluster == cluster) {
                        host.zone = zone;
                        result.push(host);
                    }
                });
                return result;
            });
        },


        api_host_update: function (zone, id, template, merge = true, order_id = null) {
            let data = {
                template: template,
                merge: merge,
            };
            if (order_id){
                data.order_id = order_id;
            }
            return Vue.http.post(`/api/host_update/${id}/?rpc_endpoint=${zone.template.endpoint}`, data);
        },


        // 只获取vms用到的区域的hosts信息
        zone_hosts: function (vms) {
            let zone__hosts = {};
            let zones = [];
            for (let i = 0; i < vms.length; i++) {
                let vm = vms[i];

                if (!vm.id) {
                    continue;
                }
                // else if (($.inArray(vm.status, ['ACTIVE', 'FAILED']) != -1) && vm.host) {
                //     continue;
                // }

                zone_ids = zones.map(x => {
                    return x.id
                });
                if ($.inArray(vm.zone.id, zone_ids) == -1) {
                    zones.push(vm.zone);
                }
            }
            let promise_hostpoolInfo_list = [];
            zones.forEach((zone) => {
                promise_hostpoolInfo_list.push(Promise.resolve(zone)
                    .then(_vue.hostpool_info)
                    .then((data) => {
                        zone__hosts[zone.id] = data
                    })
                );
            });

            return Promise.all(promise_hostpoolInfo_list).then(() => {
                return zone__hosts
            });
        },


        // 刷新虚拟机状态
        refresh_vm_status: function () {
            let _vue = window._vue;

            if (_vue.stop_refreshing_vm_status) {
                console.log('skip refresh vm status.');
                setTimeout(_vue.refresh_vm_status, _vue.refresh_interval);
                return;
            }

            console.log('begin refresh vm status...');
            _vue.refreshing_vm_status = true;

            // 获取host信息后,在去获取vm信息
            return _vue.zone_hosts(_vue.vms).then((zone__hosts) => {
                let promise_list = [];
                for (let i = 0; i < _vue.vms.length; i++) {
                    let vm = _vue.vms[i];

                    // 没有id,说明创建虚拟机失败了,不用刷新状态。
                    if (!vm.id) {
                        continue
                    }
                    let hosts = zone__hosts[vm.zone.id];
                    promise_list.push(_vue._refresh_vm_status(i, hosts));
                }

                Promise.all(promise_list).then(() => {
                    console.log('end refresh vm status.');
                    _vue.refreshing_vm_status = false;
                    setTimeout(_vue.refresh_vm_status, _vue.refresh_interval);
                });
            });
        },


        _refresh_vm_status: function (index, hosts) {
            let _vue = window._vue;
            return _vue.api_vm_info(_vue.vms[index].id, _vue.vms[index].zone, hosts).then((data) => {
                if (_vue.stop_refreshing_vm_status) {
                    return
                }
                _vue.vms.$set(index, data);
            });
        },


        zone_list: function () {
            let _vue = this;
            return _vue.$http.get('/api/zonepool_info/').then((response) => {
                let zones = response.json();
                if (_vue.enable_zone_all) {
                    zones.splice(0, 0, {name: '所有数据中心', template: {endpoint: '-1'}});
                }
                _vue.zones = zones;
                _vue.current_zone = 0;
            });
        },


        cluster_list: function () {
            let _vue = this;
            let dc = _vue.zones[_vue.current_zone];
            if (dc.template.endpoint == '-1') {
                _vue.clusters = [{name: '-1'}];
                _vue.current_cluster = '-1';
                return;
            }

            return _vue.$http.get('/api/clusterpool_info/?rpc_endpoint=' + dc.template.endpoint).then((response) => {
                let clusters = response.json();
                if (_vue.enable_cluster_all) {
                    clusters.splice(0, 0, {name: '-1'});
                }
                _vue.clusters = clusters;
                _vue.current_cluster = _vue.clusters[0].name;
            });
        },


        // 一个镜像一个模板,提取模板中的镜像,然后展示到系统版本栏。
        template_list: function () {
            let _vue = this;
            let dc = _vue.zones[_vue.current_zone];
            return _vue.$http.get(`/api/templatepool_info/?rpc_endpoint=${dc.template.endpoint}&filter_template.cluster=${_vue.current_cluster}&filter_template.osfamily=${_vue.current_osFamily}`)
                .then((resonse) => {
                    _vue.templates = resonse.json();
                    _vue.current_template = -1;
                    _vue.current_template_name = null;
                });
        },


        osFamilies_list: function () {
            let _vue = this;
            let osFamilies = ['centos', 'ubuntu', 'windows'];
            _vue.osFamilies = osFamilies;
            _vue.current_osFamily = osFamilies[0];
        },


        // image_list: function () {
        //     let _vue = this;
        //     let dc = _vue.zones[_vue.current_zone];
        //     return _vue.$http.get(`/api/imagepool_info/?rpc_endpoint=${dc.template.endpoint}&filter_template.cluster=${_vue.current_cluster}&filter_template.os=${_vue.current_osFamily}`)
        //         .then((response) => {
        //             _vue.images = response.json();
        //             _vue.current_image = -1;
        //             _vue.current_image_name = null;
        //         });
        // },


        api_vm_action: function (zone, vm, action, order_id = null) {
            let _vue = this;
            let data = {
                action: action,
                cluster_name: vm.host ? vm.host.cluster : "无"
            };
            if (order_id) {
                data.order_id = order_id;
            }
            return Vue.http.post(`/api/vm_action/${vm.id}/?rpc_endpoint=${zone.template.endpoint}`, data).then(
                (response) => {
                    return {
                        success: true,
                        vm_id: vm.id,
                        detail: response.json().detail,
                    }
                },
                (response) => {
                    return {
                        success: false,
                        vm_id: vm.id,
                        detail: response.json().detail,
                    }
                }
            );
        },


        // 获取机型列表
        vmtype_list: function () {
            let _vue = window._vue;
            return Vue.http.get('/api/vmtypes/').then(response => {
                _vue.vmtypes = response.json();
                _vue.current_vmtype = -1;
            });
        },


        //推出执行结果弹框
        push_notice: function (state, msg, time) {
            let id = (new Date()).valueOf();
            let append_msg = `<div id="${id}" class="alert ${state}" style="font-size: 14px;width: 300px"><button type="button" class="close" data-dismiss="alert"><i class="icon-remove"></i></button>${msg}</div>`;
            $("#ace-settings-container").append(append_msg);
            setTimeout(() => {
                $("#" + id).remove();
            }, time);
        },


        // 自定义排序,支持多层级属性,如key = att1.att11
        // convert: 比较大小前转换类型,如字符串转换为数字
        sort_by: function (objs, key, convert = null) {
            let _vue = window._vue;
            let [last_key, reverse] = _vue.order_reverse.split(':');
            if (last_key == key) {
                reverse = reverse * -1;
            }
            else {
                reverse = 1;
            }
            _vue.order_reverse = `${key}:${reverse}`;
            objs.sort((a, b) => {
                let value1 = eval(`a.${key}`);
                let value2 = eval(`b.${key}`);
                if (convert) {
                    value1 = convert(value1);
                    value2 = convert(value2);
                }
                if (value1 > value2) {
                    return 1 * reverse;
                }
                else if (value1 < value2) {
                    return -1 * reverse;
                }
                else {
                    return 0;
                }
            });
            return objs;
        },


        gen_uuid: function (len = 16, radix = 16) {
            var chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'.split('');
            var uuid = [], i;
            radix = radix || chars.length;

            if (len) {
                // Compact form
                for (i = 0; i < len; i++) uuid[i] = chars[0 | Math.random() * radix];
            } else {
                // rfc4122, version 4 form
                var r;

                // rfc4122 requires these characters
                uuid[8] = uuid[13] = uuid[18] = uuid[23] = '-';
                uuid[14] = '4';

                // Fill in random data.  At i==19 set the high bits of clock sequence as
                // per rfc4122, sec. 4.1.5
                for (i = 0; i < 36; i++) {
                    if (!uuid[i]) {
                        r = 0 | Math.random() * 16;
                        uuid[i] = chars[(i == 19) ? (r & 0x3) | 0x8 : r];
                    }
                }
            }

            return uuid.join('');
        },


    }
};