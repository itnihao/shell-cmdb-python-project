# -*- coding: utf-8 -*-
# 采用mysqldump 备份cmdb 数据库
# cron 每天四点
from application import app, db
import os,time

class DBback:
    def run(self):
        print "==========start=========="
        PATH = app.config.get("BACKUP_PATH")
        self.preint(PATH)
        self.backup(PATH)
        print "==========end============="

    def preint(self,PATH):
        if not os.path.exists(PATH):
            os.makedirs(PATH)

    def backup(self,PATH):
        datatime = time.strftime('%Y%m%d')
        data = app.config.get("SQLALCHEMY_DATABASE_URI").split(":")
        user = data[1].split("/")[2]
        password = data[2].split("@")[0]
        host = data[2].split("@")[1]
        port = int(data[3].split("/")[0])
        db   = data[3].split("/")[1]
        cmd = "find %s -type f -ctime +30 -exec rm -f {} \; " %PATH
        os.system(cmd)
        conn = "mysqldump -h%s -u%s -p%s -P%d --opt --default-character-set=utf8 --add-drop-database --databases %s | gzip -c > %s/cmdb_%s.gz" %(host,user,password,port,db,PATH,datatime)
        os.system(conn)
