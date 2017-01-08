Api设计文档(cmdb小组共同讨论)
==================
* 使用Rest 规范
* 返回参数 errcode 错误码, errmsg, statuscode状态码, 如果errcode>0，会有相应的错误信息提示，返回数据全部用UTF-8编码
* 返回数据都是json格式
* 统一api域名:ops.corp.anjuke.com/api/cmdb
* 签名计算
    * 统一生成私钥
    * 详细签名后面再写个文档 按照本根以前做的一个签名做[签名算法](http://git.corp.anjuke.com/corp/api-docs/browse/master/api/rule.markdown)

### 返回状态说明

| 状态码      |     含义                 |        说明                       |
| ---------- | ------------------------ | -------------------------------- |
|    200     |      OK                  | 请求成功                          |
|    400     |   BAD REQUEST            | 请求的地址不存在或者包含不支持的参数 |
|    401     |   UNAUTHORIZED           | 未授权                            |
|    403     |   FORBIDDEN              | 被禁止访问                        |
|    404     |   NOT FOUND              | 所请求资源不存在                   |
|    405     |   METHOD NOT ALLOWED     | 使用不允许的方法                   |
|    410     |   GONE                   | 资源不可用                        |
|    500     |   INTERNAL SERVER ERROR  | 内部服务器错误                     |

### 返回错误码说明

| 错误码      |   错误信息                    |       含义                      |    statuscode     |
| ---------- | ---------------------------- | ------------------------------- | ------------------ |
|   999      |   unknow_error               |    未知错误                      | 400                |
|   1000     |   need_permission            |    需要权限                      | 403                |
|   1001     |   uri_not_found              |    资源不存在                    | 404                |
|   1002     |   missing_args               |    参数不全                      | 403                |
|   1003     |   input_too_short            |    输入为空或者字数不够            | 400                |
|   1004     |   error_input                |    输入格式不正确                 | 400                |
|   1005     |   target_not_found           |    查询对象不存在                 | 400                |
|   1006     |   target_existed             |    添加对象已存在                 | 400                |

主机api
=============
* 添加主机
    * URL:ops.corp.anjuke.com/api/cmdb/host
    * Method: POST
    * Params
        * hostname
        * ip
        * is_virtual   是否是虚拟机 1表示是，0表示不是
        * parent_host_name
        * parent_ip   如果is_virtual==1 那么 parent_host_name和parent_ip 至少一个
    * 返回参数
        * statuscode  状态码
        * errcode  返回码
        * errmsg  如果errcode>0，会有相应的错误信息提示
    * 返回参数示例

            {
                "errcode":0,
                "statuscode":200,
                "errmsg":"",
            }

* 删除主机
    * URL:ops.corp.anjuke.com/api/cmdb/host/<ip:xx|host_name:xx|id:xxx>
    * Method: DELETE
    * 返回参数
        * statuscode  状态码
        * errcode  返回码
        * errmsg  如果errcode>0，会有相应的错误信息提示
    * 返回参数示例

            {
                "errcode":0,
                "statuscode":200,
                "errmsg":"",
            }

* 修改主机状态
    * URL:ops.corp.anjuke.com/api/cmdb/host/<ip:xx|host_name:xx|id:xxx>
    * Method: POST 或者 PUT
    * Params
        * status
    * 返回参数
        * statuscode  状态码
        * errcode  返回码
        * errmsg  如果errcode>0，会有相应的错误信息提示

    * 返回参数示例

            {
                "errcode":0,
                "statuscode":200,
                "errmsg":"",
            }

* 获取所有的主机信息
    * URL:ops.corp.anjuke.com/api/cmdb/hosts
    * Method: GET
    * 返回参数
        * statuscode  状态码
        * errcode  返回码
        * errmsg  如果errcode>0，会有相应的错误信息提示
        * total 主机数量
        * hosts
            * host_name  主机名
            * ip  业务ip
            * is_virtual 是否是虚拟机  0:不是 1:是
            * parent_id 如果不是虚拟主机，值为0 ，如果是虚拟主机 值是所在宿主机的id
            * device_id 设备id
            * memory 内存 单位G
            * cpu cpu核
            * storage 硬盘 单位G
            * created 主机创建时间
            * updated 主机更新时间
    * 返回参数示例

            {
                "errcode":0,
                "statuscode":200,
                "errmsg":"",
                "total":5,
                "hosts":[
                    {
                        "ip":"10.10.3.32",
                        "host_name":"app10-034",
                        "is_virtual":0,
                        "parent_id":0,
                        "device_id":15,
                        "memory":64,
                        "cpu":8,
                        "storage":300,
                        "created":"2014-08-17 23:56:03",
                        "updated":"2014-08-17 23:56:03"
                    },
                    .........
                ]
            }


* 获取主机信息
    * URL:ops.corp.anjuke.com/api/cmdb/host/<ip:xx|host_name:xx|id:xxx>
    * Method: GET
    * 返回参数
        * errcode  返回码
        * statuscode  状态码
        * errmsg  如果errcode>0，会有相应的错误信息提示
        * host_name  主机名
        * ip  业务ip
        * is_virtual 是否是虚拟机  0:不是 1:是
        * parent_id 如果不是虚拟主机，值为0 ，如果是虚拟主机 值是所在宿主机的id
        * device_id 设备id
        * memory 内存 单位G
        * cpu cpu核
        * storage 硬盘 单位G
        * created 主机创建时间
        * updated 主机更新时间
    * 返回参数示例

            {
                "errcode":0,
                "statuscode":200,
                "errmsg":"",
                "ip":"10.10.3.32",
                "host_name":"app10-034",
                "is_virtual":0,
                "parent_id":0,
                "device_id":15,
                "memory":64,
                "cpu":8,
                "storage":300,
                "created":"2014-08-17 23:56:03",
                "updated":"2014-08-17 23:56:03"
            }