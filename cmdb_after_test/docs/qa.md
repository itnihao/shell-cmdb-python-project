cmdb讨论记录
====================
* 小陆说,内部资产编号需要一个特有字段? 在资产表加一个字段 asset_label  表示内部资产编号。
  * 服务器编号 SH－IDC－FWQ－xxx
  * 交换机编号 SH－IDC－JHJ－xxx
  * 路由器编号 SH－IDC－LUQ－xxx
  * 防火墙编号 SH－IDC－FHQ－xxx

* 目前的设计 各种责任人和pool关联起来。但是以安居客的目前现状来看,不是所有的主机都会有pool的，这样责任人问题就来了?
  * 是需要的，但是第一期不做这个功能

* 虚拟机的cpu，内存，硬盘是否需要在页面上添加？
  * 不需要，本根会做一个job 到对应机器取

* Python中使用json.loads解码字符串时出错：ValueError: Expecting property name: line 1 column 1 (char 1)
  * addedSingleQuoteJsonStr = re.sub(r"(,?)(\w+?)\s*?:", r"\1'\2':", orginalJsonStr);
  * doubleQuotedJsonStr = addedSingleQuoteJsonStr.replace("'", "\"");
  * 给属性添加单引号；
  * 把所有的单引号替换成双引号；