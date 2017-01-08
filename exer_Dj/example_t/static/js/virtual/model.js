/**
 * Created by xuepingning on 2016/9/9.
 */


Vue.config.delimiters = ["[[", "]]"];
Vue.config.unsafeDelimiters = ['[[[', ']]]'];

var vue = new Vue({

    el: "#model_info",

    data: {
        select_department: [],  //选中的部门
        departments: ['新房','二手房'],          //部门列表
        models: [
            {
                business: '用户端技术部',
                name: 'user-web',
                monitor: {
                    cpu_user: 5,
                    network: 900,
                    QPS: 5
                },
                pool:['pool_A','pool_B']
            }, {
                business: '用户端技术部',
                name: 'user-job',
                monitor: {
                    cpu_user: 10,
                    network: 900,
                    QPS: 12
                },
                 pool:['pool_C','pool_D']
            }

        ],

        methods: {}

    }

});