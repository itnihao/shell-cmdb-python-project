堡垒机权限设计
====================
###需求
* 解决用户登录线上指定机器的权限问题

###要求
* 用户申请,多级审批(审批人资格说明:p7或者M4以上(包括本身))
* 权限分类: root ,evans, readonly(root只有ops可以申请)
* 权限有限期分 1天,7天,30天,1年(只有ops可以申请30天以上的)
* 邮件通知相关人审批
    * 给审批人发邮件
    * 开通成功发邮件
    * 删除过期发送邮件
* CMDB中可以看到我的审批
* 主机历史记录是否要做一个详细页面了,详情页展示5条,更多展示所有的
* CMDB中需要看到我的主机(即我拥有那些机器的权限)

###表设计
host_bastion_apply   权限申请表
```
    id              int(11)
    uid             int(11)         用户uid
	host_id		    int(11)	用户申请机器的id,审批多个就插入多条
	role            tinyint(1)      用户申请的权限,root:1,evans:2,readonly:3
	approve_uid     int(11)         当前审批人uid
	status          tinyint(1)      申请状态 1:审批中,2:驳回,3:正在开通中,4:开通成功,5:开通失败
	days            smallint        申请有效期期限(单位:天)
    content         varchar(255)    申请描述
    created         timestamp       创建时间
    updated         timestamp       更新时间
    索引
    id              auto_increment primary_key
	idx_uid_status  INDEX(`uid`,`status`)
	idx_approve_uid INDEX(`approve_uid`)
```

host_bastion_tasks  权限开通或者删除任务表
```
    id              int(11)
    apply_id        int(11)         申请id
    uid             int(11)         用户uid
    host_id         int(11)         主机id
    role            tinyint(1)      用户申请的权限,root:1,evans:2,readonly:3
    type            tinyint(1)      类型:默认值1,1:新增  2:删除
    status          tinyint(1)      状态默认值0,0:未运行,1:执行成功 2:执行失败
    exec_time       timestamp       执行时间
    created         timestamp       创建时间
    updated         timestamp       更新时间
    索引
    id              auto_increment primary_key
    idx_status      INDEX(`status`)
```

user_host  用户主机关系表(此表的数据源来至host_bastion_tasks表,当运行Job执行成功会对此表操作)
```
    id              int(11)
    uid             int(11)
    host_id         int(11)
    role            tinyint(1)      用户权限,root:1,evans:2,readonly:3
    status          tinyint(1)      status 默认1 1:有效,2表示过期
    created         timestamp       创建时间
    updated         timestamp       更新时间
    索引
    id              auto_increment primary_key
    idx_uid_host_id INDEX(`uid`,`host_id`)
```

mail_queue  邮件队列表专门用户发送邮件(后续的申请主机也可以用这个)
```
    id              int(11)
    email           varchar(255)    收件人邮箱地址
    subject         varchar(255)    邮件标题
    content         text            邮件内容
    status          tinyint(1)      状态,0:未运行,1:执行成功 2:执行失败
    created         timestamp       创建时间
    updated         timestamp       更新时间
    索引
    id              auto_increment primary_key
    idx_status      INDEX(`status`)
```


###数据量
* host_bastion_apply 按照每天20个申请,一年7300条数据量,先不考虑删除归档操作
* host_bastion_tasks 按照每天20个申请,每次申请5台,一年36500(365*100)条数据库,先不考虑删除归档操作
* mail_queue         按照每天20个申请,40封邮件,一年14600数据量,先不考虑删除归档操作
* user_host          安居客如果有1000台主机,安居客200名工程师,最多200000数据量,按照估计量600*20

###脚本需求
* 处理host_bastion_tasks任务,开通或者删除权限,每分钟运行一次,判断exec_time不大于当前时间并且status in (0,2)(PS:root>evans>readonly,也就是有root权限的用户同时拥有evans和readonly),对于同一个申请需要一次性跑完
* 处理mail_queue 发送邮件,每分钟运行一次
* 验证主机是否可以都有ansible_key 脚本(PS:需要知道主机是否active),每天运行一次
* 处理用户上级关系,通过OA接口可以获取上级信息,并获取级别(p_level,m_level),并获取部门department_id
* 迁移数据脚本(一次性)
    * 迁移用户公钥
    * 迁移用户申请
    * 迁移用户和机器开通关系


###页面需求
* 权限申请页面：申请机器,申请权限,申请原因
* 我的申请页面：序号,申请机器,申请权限,申请原因,申请时间,状态
* 我的审核页面: 序号,申请机器,申请权限,申请原因,申请时间,操作(通过或者驳回)
* 权限申请管理页面: 序号,申请机器,申请权限,申请原因,申请时间,状态,操作(通过或者驳回)
* 我的主机页面: 序号,主机名,权限,开通时间
* 权限统计页面: 序号,主机名,root(展示拥有此权限的用户,类似权限管理),evans(展示拥有此权限的用户,类似权限管理),readonly(展示拥有此权限的用户,类似权限管理)