cmdb gitlab 仓库


开发环境
========================
* 数据库信息
  * 192.168.1.103 用户名:caixh 密码:caixh123  数据库名称:cmdb

* 代码环境
  * 放在各自机器开发
  * 在src/cmdb 目录新建config.py
  
本地机器内容如下

    # -*- coding: utf-8 -*-
    import os
    SQLALCHEMY_DATABASE_URI = 'mysql://caixh:caixh123@192.168.1.103:3306/cmdb'
    SQLALCHEMY_ENCODING = "utf-8"
    SQLALCHEMY_ECHO = True
    DEBUG = True

    #migrate
    MIGRATE_DATABSE_URI ='mysql://caixh:caixh123@192.168.1.103:3306/zeus?charset=utf8'
    VM_DATABASE_URI =  'mysql://caixh:caixh123@192.168.1.103:3306/zeus?charset=utf8'
    #elasticsearc
    ES_HOST="192.168.193.39"
    ES_PORT=9200

    # celery
    BROKER_URL = 'redis://192.168.193.40:6379/0'

    #ANSIBLE
    ANSIBLE_BIZPATH = '/home/www/biz_ansible'
    ANSIBLE_BIZTEMP = '/home/www/biz_ansibletemp'
    ANSIBLE_BIZCONFIG = '/home/www/biz_config'
    ANSIBLE_BIZTEMP = '/home/www/biz_ansibletemp'
    PYTHON_VPATH = '/home/www/virpython/bin/python'
    ANSIBLE_PLAYBOOK = '/home/www/virpython/bin/ansible-playbook'


    #SQLALCHEMY_DATABASE_URI = 'mysql+oursql://root:123456@127.0.0.1/cmdb'
    #SQLALCHEMY_POOL_RECYCLE = 7200

    # oauth
    AUTH_URL = 'https://auth.corp.anjuke.com/oauth/2.0'
    AUTH_ID = 'nzl7lysmdgh3muzzrp9v'
    AUTH_SECRET = 'upe56ihqknuoiev5feeem283zw7wxjra7edpkgjv'
    SECRET_KEY = os.urandom(24)
    
    #ZABBIX API AUTH_URL
    ZABBIX_API_URL_10 = 'http://zabbix10.corp.anjuke.com/api/fastApi.php'
    ZABBIX_API_URL_20 = 'http://zabbix20.corp.anjuke.com/api/fastApi.php'

    #SERVER PORT
    SERVER_PORT = 5000

* dev展示环境
  * 192.168.193.40:5000
  * 主机用户名:vincent  密码 123456
  * git 仓库位置:/home/www/cmdb
  * virtualenv环境:/home/www/virpython