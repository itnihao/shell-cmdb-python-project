版本控制
===============
* 版本命名 YYYY_WW_DD
    * YYYY 年份 例如 2015,2016
    * WW 第几周 例如05,12
    * DD 星期中的第几天 例如01,02,03,...,06,07
* 版本控制文件
    * GA    /home/www/config/RELEASE_VERSION_GA
    * BETA  /home/www/config/RELEASE_VERSION_BETA
* 外围配置 /home/www
    * 新增配置 PRODUCT_CONFIG,例如PRODUCT_CONFIG = "/home/www/config.py"

* 版本位置
    * 版本路径 /home/www/release

任务
===================
* 启动脚本,目前在/home/www/cmdb_shells/cmdb.sh(通过supervisor管理)
* 上线工具修改
* 需要注意的地方
    * 发布每个版本需要发布一个config.py的文件到srcc/cmdb目录
    * 需要给static下面的asset和.webassets-cache可写权限