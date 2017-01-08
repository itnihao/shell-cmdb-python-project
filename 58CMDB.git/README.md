# CMDB——DB字段设计使用规范

 1. 英文字段名和中文描述严格对应，出现某英文词的地方，对应的中文要用对应的词描述，不能使用易混词。
 2. 数据库字段一律小写，用下划线连接。主键和外链键值不需大写。
 3. id类字段一律用全名加下划线加 `_id` ，关系表用联合主键的形式。
 4. 表名加上 `t_` 前缀。
 5. id、name、type、model、num、count等非常常用的单词不要单用，加上前缀。
 6. 已确定使用缩写的名词，建议所有地方都只使用缩写，不允许使用全名：
> | 全写   | 缩写 | 描述 | 
> | :----- | :----- | :----- |
> | department | dpt |  | 
> | number | num |  | 
> | telephone  | tel | 电话 | 
> | organization  | org | 组织 |  
 
 7. 常见词统一译名：
> | 常见词   | 译名 | 描述 | 
> | :----- | :----- | :----- |
> | IP地址 | ip_address |  | 
> | 固资 | asset |  | 
> | 配件  | accessory |  | 
> | 供应商  | producer |  | 
> | 插槽  | slot |  | 
> | 设备  | device |  | 
> | 机位  | rack |  | 
> | 服务器  | server |  | 
> | 备注  | comment |  | 
> | 编号（有序）  | num |  | 
> | 代码  | code |  | 
> | 数量  | count |  | 
> | 业务线  | business_line |  | 
 > | 产品线  | business |  | 
 > | 模块  | product |  |  
  > | 集群  | cluster |  | 
 
 8. MYSQL建表数据类型:
> | 字段   | 类型 | 描述 | 
> | :----- | :----- | :----- |
> | 时间 | datetime |  | 
> | 长度 | int | 毫米 | 
> | id  | bigint | 主键，不用自增 | 
> | `str`  | varchar | 常规字段 | 
> | `str`  | text | 特殊字段 | 
> | `str`  | tinyint | 状态/枚举  | 
> | `str`  | bit | 逻辑  | 
 
 

 
