环境部署
=================
*  sudo apt-get install python-virtualenv
* 激活虚拟环境
    *  pip install flask
    *  pip install Flask-Script
    *  pip install Flask-Assets
    *  pip install sqlalchemy
    *  pip install Flask-SQLAlchemy
    *  pip install flask-login
    *  pip install mysql-python
       *  sudo apt-get install libmysqlclient-dev
       *  sudo apt-get install python-dev
    *  pip install IPy
    *  pip install PyPages
    *  pip install celery-with-redis
    *  pip install elasticsearch
    *  pip install ply #语法分析
    *  pip install cssmin
    *  pip install jsmin
    *  pip install xlwt
* 或者 pip install -r requirements.txt

* 线上环境部署(nginx+uwsgi+redis+celery)
* nginx部署
  * 安装nginx  apt-get install nginx
  * nginx配置
    * vim /etc/nginx/conf.d/cmdb.conf,内容如下

        server{
              listen 80;
              server_name  ops.corp.anjuke.com;
              location / {
                 try_files $uri @yourapplication;
              }
              location @yourapplication{
                include uwsgi_params;
                uwsgi_pass unix:/tmp/uwsgi.sock;
                uwsgi_param UWSGI_PYHOME /home/www/virpython;
                uwsgi_param UWSGI_CHDIR /home/www/cmdb/src/cmdb;
              }
        }
* uwsgi
  * 安装uwsgi pip install uwsgi
  * 运行项目
    * cd /home/www/cmdb/src/cmdb/
    * nohup /home/www/virpython/bin/uwsgi -s /tmp/uwsgi.sock -w manage:app --chmod-socket=662  > /var/log/cmdb.log 2>&1 &

* redis
  * 安装redis
    * wget http://download.redis.io/releases/redis-2.8.13.tar.gz
    * tar -xvf redis-2.8.13.tar.gz
    * mv redis-2.8.13 redis
    * cd redis
    * make
    * make install
  * 启动redis
    * cp redis/redis.conf /etc/
    * redis-server   可以放到supervisor中管理

* celery
  * 安装celery  pip install celery-with-redis
  * 运行worker
      * cd /home/www/cmdb/src/cmdb/
      * python celery_tasks.py  可以放到supervisor中管理

* elasticsearch
  * elasticsearch 服务端
    * 安装服务端
      * apt-get install openjdk-7-jdk
      * wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.3.1.zip
      * unzip elasticsearch-1.3.1.zip
      * mv elasticsearch-1.3.1 elasticsearch
      * sh elasticsearch/bin/elasticsearch
  * python 客户端
    * pip install elasticsearch

* supervisor
  * 安装 apt-get install supervisor