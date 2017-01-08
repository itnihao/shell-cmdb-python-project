表字段设计
===================
* 目前有14张表
  * user 表 用户表
  * datacenter 表 机房表
  * rack表 机柜表
  * ip_address表  ip池分配表
  * supplier 表  供应商表
  * device_category 表  设备分类表
  * device 表  设备表
  * device_ip  设备多ip关系表
  * host 表 host表
  * host_ip 表  主机多ip关系表
  * host_operation_history 表  主机操作变更表
  * pool 表  pool详细表
  * pool_host 表 主机pool关联表
  * pool_config pool配置表
  * log 表 其他操作日志表
  * tasks 表  任务队列表
  * follow 表 关注关系表



表字段详细描述
=======================
user

    id              int
    oauth_id        int(10)         auth返回的id
    oauth_token     varchar(40)     用于和auth交互的凭证
    cn_name         varchar(50)     中文名
    name            varchar(50)     用户名
    employee_id     varchar(10)     工牌号
    email           varchar(255)    邮箱
    status          tiny(2)         标记是否离职
    superior_id     int(11)         直属上级领导人的user_id，0为没有上级
    p_level         tinyint(2)      p级别
    m_level         tinyint(2)      m级别
    department_id   int(10)         部门id
    department_name varchar(50)     部门名称
    function_id      int(10)         tech id
    function_name    varchar(50)     tech name
    mobile          varchar(11)     手机号码
    created         timestamps      创建时间
    updated         timestamps      更新时间

    索引
    id              auto_increment primary_key
    oauth_id        index  idx_oauth_id
    oauth_token     index  idx_oauth_token
    cn_name         index  idx_cn_nme
    name            index  idx_name
self, hostname, primary_ip_id, type, is_virtual, parent_id, device_id, status, cpu, memory, storage, deleted=0

datacenter

    id              int             机房 id
    name            varchar(20)     机房名称
    short_name      varchar(20)     机房简称
    address         varchar(80)     机房地址
    idc_label       varchar(20)     机房资产编号例如SH-IDC
    content         text            备注字段:紧急接口人信息: 例如电话,座机,姓名,邮 箱
    deleted         tinyint(1)      1表示被删除了
    created         timestamps      创建时间
    updated         timestamps      更新时间


    索引
    id              auto_increment primary_key


rack

    id              int             机柜 id
    datacenter_id   int(10)         所属机房 id
    name            varchar(10)     机柜名称
    height          tinyint(3)      机柜高度例如:48u
    deleted         tinyint(1)      1表示被删除了
    content         varchar(50)     机柜描述
    created         timestamps      创建时间
    updated         timestamps      更新时间

    索引
    id              auto_increment primary_key
    datacenter_id   index idx_datacenter_id
    name            index idx_name

ip_address

    id              int             ip池id
    ipv4            varchar(15)     index   真实ip
    flag            tinyint(10)     index   1表示占用,0表示未占用,2表示系统预留
    note            varchar(40)     备注字段
    created         timestamps      创建时间
    updated         timestamps      更新时间

    索引
    id              auto_increment primary_key
    ipv4            index idx_ipv4
    flag            index idx_flag

supplier

    id              int             供应商id
    name            varchar(30)     供应商名称
    content         text            备注字段:供应商联系人,电话等等
    created         timestamps      创建时间
    updated         timestamps      更新时间

    索引
    id              auto_increment primary_key

device_category

    id              int             设备分类id
    name            varchar(15)     设备名称
    short_name      varchar(30)     设备简称
    deleted         tinyint(1)      1表示被删除了
    note            varchar(40)     备注字段
    created         timestamps      创建时间
    updated         timestamps      更新时间

    索引
    id              auto_increment primary_key


device

    id              int             设备 id
    device_cat_id   int(10)    设备分类 id
    supplier_id     int(10)         供应商 id
    model           varchar(20)     机器型号
    cpu             tinyint(3)      cpu核数
    cpu_extra       text            存 json:分别三个 key cpu_core: Cpu 核数 cpu_model: Cpu 型号 cpu_num: Cpu 个数
    memory          smallint        内存大小 单位GB
    memory_extra    text            存 json(有几个内存就写几个 item):
    storage         smallint        硬盘总大小 单位GB
    storage_extra   text            存 json(有几块硬盘就有几个 item):每个 item 包括以下几 个属性 size:硬盘大小,单位 GB rate:转速 type:接口类型 SATA 等
    rack_unit       tinyint(1)      设备U型
    sn              varchar(20)     Sn号
    device_label    varchar(20)     内部设备编号由小陆统一生成
    primary_mac     varchar(17)     Mac 地址:格式 ff:ff:ff:ff:ff:ff
    rack_id         int(10)         index 机柜 id
    rack_offset     tinyint(2)      在机柜的位置:从上到下
    primary_ip_id   int(10)         ip池id
    buy_time        timestamps      采购时间
    elapsed_time    timestamps      过保时间
    price           int(10)         金额,单位分
    deleted         tinyint(1)      1表示被删除了
    content         varchar(50)     其他信息
    search          text            搜素关键词
    created         timestamps      创建时间
    updated         timestamps      更新时间

    索引
    id              auto_increment primary_key
    device_cat_id   index  idx_device_category_id
    supplier_id     index  idx_supplier_id
    primary_ip_id   index  idx_primary_ip_id
    cpu             index  idx_cpu
    memory          index  idx_memory
    storage         index  idx_storage
    search          index  idx_search


device_ip

    id              int             auto_increment, primary_key
    device_id       int(10)         设备id
    net_name_id     tinyint         网卡标示:0 远控卡,1=>其他
    ip_address_id   varchar(15)     其他ip
    mac             varchar(40)     mac地址
    content         varchar(50)     此ip的作用
    created         timestamps      创建时间
    updated         timestamps      更新时间

    索引
    id              auto_increment primary_key
    device_id       index idx_device_id
    ip_address_id   index idx_ip_address_id

device_operation_history

    id              int
    device_id       int(10)         设备id
    uid             int(10)         用户id
    content         text            操作说明
    created         timestamps      创建时间
    updated         timestamps      更新时间

    索引
    id              auto_increment primary_key
    device_id       index ix_device_operation_history_device_id

host

    id              int             主机 id
    hostname        varchar(12)     index   业务 appname
    primary_ip_id   int(10)         ip池id
    type            tinyint(2)      1:app池 2:apc池 3:db/dw等
    is_virtual      tinyint(1)      0:表示不是虚拟的机器  1:表示是虚拟的机器
    parent_id       int(10)         如果是虚拟主机 请填写宿主 机id
    device_id       int(10)         关联设备id
    status          tinyint(1)      index 主机状态
    cpu             tinyint(3)      cpu核数
    memory          smallint        内存大小 单位GB
    storage         smallint        硬盘总大小 单位GB
    deleted         tinyint(1)      1表示被删除了
    search          text            搜索关键词
    created         timestamps      创建时间
    updated         timestamps      更新时间


    索引
    id              auto_increment primary_key
    primary_ip_id   index  idx_primary_ip_id
    hostname        index  idx_hostname
    cpu             index  idx_cpu
    memory          index  idx_memory
    storage         index  idx_storage
    search          index  idx_search


host_ip

    id              int
    host_id         int(10)         主机id
    net_name_id     tinyint         网卡标示:0=>eth0,1=>eth1....7=>eth7
    primary_ip_id   int(10)         其他ip
    content         varchar(50)     此ip的作用
    created         timestamps      创建时间
    updated         timestamps      更新时间

    索引
    id              auto_increment primary_key
    host_id         index idx_host_id
    primary_ip_id   index idx_primary_ip_id


vm

    id              int
    vm_id           int             关联虚拟机id
    status          tinyint         0 未执行  1 执行成功  2 执行失败
    content         varchar(50)     备注（操作日志等）
    created         timestamps      创建时间
    updated         timestamps      更新时间


host_operation_history

    id              int
    host_id         int(10)         主机 id
    uid             int(10)         用户id
    content         text            操作说明
    created         timestamps      创建时间
    updated         timestamps      更新时间

    索引
    id              auto_increment primary_key
    host_id         index idx_primary_ip_id

pool

    id              int             pool编号
    name            varchar(20)     pool名称
    ops_owner       int(10)         ops接口人
    team_owner      int(10)         pool负责人 id
    biz_owner       int(10)         业务接口人 id
    note            varchar(40)     备注
    created         timestamps      创建时间
    updated         timestamps      更新时间

    索引
    id              auto_increment primary_key

pool_host

    id              int
    pool_id         int(10)         pool编号
    host_id         int(10)         主机编号
    note            varchar(40)     备注
    created         timestamps      创建时间
    updated         timestamps      更新时间

    索引
    id              auto_increment primary_key
    pool_id         index idx_pool_id
    host_id         index idx_host_id

pool_config

    id              int
    pool_id         int(10)         pool的id
    key             varchar(15)     操作名称 例如上线，下线
    value           varchar(80)     操作描述
    note            varchar(50)     备注
    created         timestamps      创建时间
    updated         timestamps      更新时间

    索引
    id              auto_increment primary_key
    pool_id         index idx_pool_id

log

    id              int             auto_increment, primary_key
    uid             int(10)         用户id
    flag            smallint        index 1:pool 详细表 2:pool 关联表
    content         text            操作描述
    created         timestamps      创建时间
    updated         timestamps      更新时间


tasks

    id              int
    type            smallint        类型 1：自动化 2：自定义命令
    target_id       int             关联ID,例如如果是自动化,此ID就会使pool表的自增id
    command         text            命令json数组
    success         text            命令执行成功会执行:json数组
    fail            text            命令执行失败会执行:json数组
    hosts           text            主机列表:json数组
    status          smallint        0 未执行 1 执行成功 2 执行失败
    note            text            备注:会填充执行命令日志
    created         timestamps      创建时间
    updated         timestamps      更新时间

follow

    id              int             自增id
    uid             int             关注用户的id
    type            smallint        类型 1：pool 2: host 3:rack
    target_id       int             关联ID,如果类型是1,此ID就会使pool表的自增id,3:=>rack_id
    created         timestamps      创建时间
    updated         timestamps      更新时间

alarm

    id              int
    uid             int(11)         用户id
    type            smallint(6)     type=1 pool  type=2 host
    target_id       int(11)         主机id或pool_id
    created         timestamp       创建时间
    updated         timestamp       更新时间

    索引
    id              auto_increment primary_key
    uid             index idx_alarm_uid
    type            index idx_alarm_type
    target_id       index idx_alarm_target_id

sshkey

    id              int
    uid             int(11)         用户id
    name            string(20)      公钥名称
    key             text            用户公钥
    created         timestamp       创建时间
    updated         timestamp       更新时间

    索引
    id              auto_increment primary_key

ip_blacklist

    id              int
    ip_address      string(15)      ip地址
    type            tinyint         type=1 pool  type=2 host
    content         string(255      主机id或pool_id
    user_id         int             用户id
    deleted         tinyint         1表示被删除
    created         timestamp       创建时间
    updated         timestamp       更新时间

    索引
    id              auto_increment primary_key




role 表：

```
id                   int    
name                 varchar(25)                    角色名字
created              timestamp
updated              timestamp
索引
id                   auto_increment primary_key
name        index    idx_name
```
user_role表：
```
id                   int
user_id              int                                    用户对应的user id
role_id              int                                    对应角色的id
created              timestamp
updated              timestamp
索引 
id                   auto_increment primary_key
user_id              idx_user_id
```
action表
```
id                   int
url                  varchar(60)                        权限管理的url
content              varchar()                           记录url的作用
methond              varchar(25)                       url对应的方法
tag                  varchar(25)                      url的归类(如：host,poll)
created              timestamp
updated              timestamp
索引
id                   auto_increment primary_key
url       index      idx_url
tag       index      idx_tag
```
role_action表：
```
id                   int
action_id            int                  角色对应的动作的id
role_id              int                  角色id
created              timestamp
updated              timestamp
索引
id                   auto_increment primary_key
unique      index    name(role_id,action_id)
````

host_load_ratio

    id              int
    host_id         int(11)         主机id
	ratio			int(11)			满载率
    content         string(255)     各项指标
    created         timestamp       创建时间
    updated         timestamp       更新时间

    索引
    id              auto_increment primary_key
	idx_host_id     INDEX(`host_id`)


host_load_daily
```
    id              int
    host_id         int(11)         主机id
	ratio			int(11)			满载率
    content         string(255)     各项指标
    created         timestamp       创建时间
    updated         timestamp       更新时间
    索引
    id              auto_increment primary_key
	idx_host_id     INDEX(`host_id`
```   
    
pool_load_ratio

    id              int
    pool_id         int(11)         pool_id
	ratio			int(11)			满载率
    content         string(255)     各项指标
    created         timestamp       创建时间
    updated         timestamp       更新时间

    索引
    id              auto_increment primary_key
	idx_pool_id     INDEX(`pool_id`)


pool_load_daily(每日计算一次)

    id              int
    pool_id         int(11)         pool_id
	ratio			int(11)			满载率
    content         string(255)     各项指标
    created         timestamp       创建时间
    updated         timestamp       更新时间

    索引
    id              auto_increment primary_key
	idx_pool_id     INDEX(`pool_id`)


stock_parts_model

    id              int
    type            tinyint         内存/硬盘
    content         varchar(255)    型号描述
    created         timestamp       创建时间
    updated         timestamp       更新时间

    索引
    id              auto_increment primary_key
    type            index idx_type


stock_parts

    id              int
    type            tinyint         内存/设备
    model_id        int(11)         内存/硬盘型号
    num             int(11)         总数
    status          tinyint         状态：0 可使用，1 报废
    created         timestamp       创建时间
    updated         timestamp       更新时间

    索引
    id              auto_increment primary_key
    type            index idx_type
    model_id        index model_id
    status          index status


stock_history

    id              int
    target_id       int(11)         对应型号表id
    device_id       int(11)         内存或硬盘对应的设备id,0:采购入库，其他值出库或报废关联的设备
    num             int             数量
    status          tinyint         状态：0 采购，1 报废
    type            tinyint         行为：0 入库，1 出库
    content         varchar(255)    备注 (从设备上取回来重新入库的标注在备注里）
    created         timestamp       创建时间
    updated         timestamp       更新时间

    索引
    id              auto_increment primary_key
    device_id       index idx_device_id
    status_type     index idx_status_type

dns_zone

    id              int
    uid             int(11)         审核人
    zone            varchar(50)     域名后缀
    type            tinyint         0：公网域名  1：个人域名
    display         tinyint         0：不显示 1：显示，管理员可见
    content         varchar(255)    备注用途
    created         timestamp       创建时间
    updated         timestamp       更新时间

    索引
    id              auto_increment primary_key

dns_apply

    id              int
    prefix          varchar(50)     域名前缀
    zone_id         int(11)         域名后缀 对应域名表中id
    type            tinyint         记录类型 1：A记录，2：CNAME 3：MX 4：TXT
    value           varchar(50)     ip或者域名
    uid             int(11)         申请人id
    approve_id     int(11)         审核人id
    content         varchar(255)    备注用途
    priority        tinyint         MX记录优先级 冗余字段
    created         timestamp       创建时间
    updated         timestamp       更新时间

    索引
    id              auto_increment primary_key

dns_history

    id              int
    dns_apply_id    int(11)         申请id
    status          tinyint         申请状态 0：驳回 1：通过
    created         timestamp       创建时间
    updated         timestamp       更新时间

    索引
    id              auto_increment primary_key

