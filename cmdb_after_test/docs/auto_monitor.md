自动化设计
========================

* tasks

        id              int
        type            smallint        类型 1：自动化 2：自定义命令
        target_id       int             关联ID,例如如果是自动化,此ID就会使pool表的自增id
        command         text            命令json格式，三个key   tasks(需要执行的任务),success(执行成功需要回调的命令),fail(执行失败需要回调的命令)
        status          smallint        0 未执行 1 执行成功 2 执行失败
        note            text            备注:会填充执行命令日志
        created         timestamps      创建时间
        updated         timestamps      更新时间


监控设计
=========================

* follow

        id              int             自增id
        uid             int             关注用户的id
        type            smallint        类型 1：pool 2: host
        target_id       int             关联ID,如果类型是1,此ID就会使pool表的自增id
        created         timestamps      创建时间
        updated         timestamps      更新时间


* 关注功能
  * 在pool列表页和详细页 都加入关注功能
  * 在主机列表页和主机详细页都加入关注功能


* 展示
  * 在我们CMDB的导航条上加入监控，页面显示关注的pool和关注的主机 两个tab
    * 关注的pool，先显示pool列表，点击pool，进入详细列表，展示pool下主机的监控信息
    * 关注的主机,直接展示所有主机的监控信息
  * 监控的指标
    * load,cpu,mem,disk,io,swap
    * 所有的数据都从zabbix数据库获取,目前监控由肖云龙和谢鹏负责


