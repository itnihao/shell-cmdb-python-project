cmdb功能
===================
* 用户中心模块
  * 登录功能(强制登录)
  * 用户管理
  * 同步用户信息的job

* IDC管理模块
  * 机房管理 (一个页面就可以了，添加或者修改都可以div弹出层)
        * 机房列表展示
        * 机房详细展示
        * 添加机房
        * 修改机房(删除机房功能不需要)

  * 机柜管理 (一个页面就可以了，添加或者修改都可以div弹出层)
        * 机柜列表展示(关联机房)
        * 机柜详细展示
        * 添加机柜
        * 修改机柜
        * 删除机柜(删除之前 对应的所属此机柜的设备需要先修改)

  * 供应商管理  (一个页面就可以了，添加或者修改都可以div弹出层)
        * 供应商列表展示
        * 供应商详细介绍列表
        * 添加供应商
        * 修改供应商(不需要删除功能,可以在备注中注明)

  * ip池管理 (此功能应该只对特殊几个人有)
        * 添加ip和ip段
        * 删除 (修改功能好像可以不需要,如果错了直接删除。如果删除某个ip之前需要确认此ip是否被占用)

* 设备管理模块
  * 设备分类管理(一个页面就可以了,添加可以弹出div层)
        * 分类展示
        * 添加分类
        * 修改分类
        * 删除分类

  * 设备管理
        * 展示列表
        * 添加设备 (关于某些有多少item的,需要动态添加input。例如多个ip，多个磁盘，多个内存条)
        * 修改设备
        * 搜索功能：根据ip,设备类型,供应商等等


* 主机管理模块
  * 主机管理
        * 主机展示列表
        * 主机详细展示(也需要讲变更历史展示出来，例如展示5条，更多可以去详细列表看)
        * 搜素功能：根据ip，hostname,机器类型(实体机器或者虚拟机器)
        * 添加主机
        * 修改主机信息
        * 删除主机(删除之前 如果该主机在某个pool 需要先解除关系)
  * 主机变更操作历史
        * 展示列表 和主机详细展示结合

* pool服务模块(做一个tree结构)
  * pool展示列表
  * pool信息修改(例如负责人，pool名字)
  * pool添加主机
  * pool删除主机

* 日志功能
  * 只展示列表，分页就可以了，先只查看就好了
