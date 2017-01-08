var vue = new Vue({
    mixins: [OcaMixin],

    el: "#vue_host_apply",
    data: {
        vm_num: 1,  // 新添加的服务器数量
        shops: [],
        vms: [],
        step: 'step1',
        total_vm_num: 0,
        order_id: null,
    },
    methods: {
        add_watch: function () {
            let _vue = window._vue;
            _vue.$watch('current_zone', function (val, oldVal) {
                console.log(`change zone to: ${_vue.zones[val].template.endpoint}`);
                Promise.resolve().then(_vue.cluster_list)
                    .then(_vue.template_list)
                    .then(_vue.osFamilies_list)
                    .then(_vue.image_list);
            });
            _vue.$watch('current_cluster', function (val, oldVal) {
                console.log(`change cluster to: ${val}`);
                Promise.resolve().then(_vue.template_list)
                    .then(_vue.osFamilies_list)
                    .then(_vue.image_list);
            });
            _vue.$watch(
                'current_osFamily', function (val, oldVal) {
                    console.log(`change osFamily to: ${val}`);
                    Promise.resolve().then(_vue.template_list);
                });
        },


        vmtype_change: function () {
            this.current_vmtype_name = $('#vmtype').find("option:selected").text();
            console.log(`change vmtype to ${this.current_vmtype_name}`);
        },


        // 切换镜像
        template_change: function () {
            this.current_template_name = $('#template').find("option:selected").text();
            console.log(`change template/image to ${this.current_template_name}`);
        },


        // 加入购物车
        add_shop: function () {
            if (isNaN(this.vm_num)|| parseInt(this.vm_num) > 50 || parseInt(this.total_vm_num) + parseInt(this.vm_num) > 50 || parseInt(this.vm_num) <= 0) {
                bootbox.confirm(`一次创建的服务器总量不能超过50台,不能小于0台！\n请重新输入……`, function (result) {
                    if (result) {
                        return;
                    }
                });
            }
            else if (this.current_vmtype < 0) {
                bootbox.confirm(`请选择机型！`, function (result) {
                    if (result) {
                        return;
                    }
                });
            }
            else if (this.current_template < 0) {
                bootbox.confirm(`请选择系统版本！`, function (result) {
                    if (result) {
                        return;
                    }
                });
            }
            else {
                this.shops.push({
                    'zone': this.zones[this.current_zone],
                    'cluster': this.current_cluster,
                    'vmtype': this.current_vmtype,
                    'vmtype_name': this.current_vmtype_name,
                    'template_id': this.current_template,
                    'template_name': this.current_template_name,
                    'vm_num': this.vm_num,
                });
                this.total_vm_num = parseInt(this.total_vm_num) + parseInt(this.vm_num);
            }
        },


        // 从购物车删除
        del_shop: function (index) {
            this.total_vm_num =this.total_vm_num-parseInt(this.shops[index].vm_num);
            this.shops.splice(index, 1);
        },


        //修改表格中的虚机数量
        change_num: function (index) {
            let element = document.getElementById("check_info").rows[index + 1].cells[4];
            let num = parseInt(element.innerText);
            element.innerHTML = `<input id="chg_num" type="text" value="${num}" />`;
            $("#change_" + index).hide();
            $("#save_" + index).show();
            $("#cancel_" + index).show();
        },


        //修改后保存数据
        save_num: function (index) {
            let _vue = window._vue;
            let num = $('#chg_num').val();
            if (isNaN(num) || parseInt(num) > 50 || parseInt(this.total_vm_num) - parseInt(this.shops[index].vm_num) + parseInt(num) > 50 || parseInt(num) <= 0) {
                bootbox.confirm(`一次创建的服务器总量不能超过50台,不能小于0台！\n请重新输入……`, function (result) {
                    if (result) {
                        return;
                    }
                });
            }
            else {
                let element = document.getElementById("check_info").rows[index + 1].cells[4];
                element.innerHTML = num;
                this.total_vm_num = parseInt(this.total_vm_num) - parseInt(this.shops[index].vm_num);
                this.shops[index].vm_num = num;
                this.total_vm_num = parseInt(this.total_vm_num) + parseInt(num);
                $("#change_" + index).show();
                $("#save_" + index).hide();
                $("#cancel_" + index).hide();
            }

        },


        //取消保存
        cancel_num: function (index) {
            let _vue = window._vue;
            let element = document.getElementById("check_info").rows[index + 1].cells[4];
            let num = this.shops[index].vm_num;
            element.innerHTML = num;
            $("#change_" + index).show();
            $("#save_" + index).hide();
            $("#cancel_" + index).hide();
        },


        // 创建虚拟机
        create_vms: function () {
            let _vue = window._vue;

            if (!_vue.shops.length) {
                console.log("没有要创建的虚拟机");
                return null;
            }

            let promise_list = [];
            this.shops.forEach(function (shop) {
                for (let i = 0; i < parseInt(shop.vm_num); i++) {
                    data = {
                        'cluster_name': shop.cluster,
                        'template_id': shop.template_id,
                        'vmtype_id': shop.vmtype,
                        'order_id': _vue.order_id,
                    };
                    promise_list.push(_vue.api_template_instantiate(shop.zone, data).then(
                        (data) => {
                            if (data.success) {
                                _vue.vms.push({
                                    id: data.detail.vm_id,
                                    zone: shop.zone,
                                });
                            }
                            else {
                                let state = "alert-warning";
                                _vue.push_notice(state, data.detail, 10000);
                                _vue.vms.push({
                                    status: data.detail,
                                });
                            }

                        }
                    ));
                }
            });

            Promise.all(promise_list).then(() => {
                    console.log('all vm created');
                    _vue.step = 'step2';
                    _vue.refresh_vm_status();
                }
            );

            // 清空购物车
            this.shops = [];
        },

    },


    ready() {
        window._vue = this;
        // 订单号,用于日志里面标识一起创建的vm
        this.order_id = this.gen_uuid();

        this.zone_list()
            .then(this.cluster_list)
            .then(this.vmtype_list)
            .then(this.osFamilies_list)
            .then(this.template_list)
            .then(this.add_watch);
    }


});
