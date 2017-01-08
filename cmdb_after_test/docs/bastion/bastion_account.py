# -*- coding: utf-8 -*-
import MySQLdb
import subprocess
import datetime
import os
#按需要修改下面的配置
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PWD = 'root'
MYSQL_DATABASE = 'cmdb'

LOCAL_SHELL = '/usr/local/bin/eash'

class Bastion_Account:

    def run(self):
        start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print '-----------start:%s-------------'%start_time
        conn = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PWD, MYSQL_DATABASE)
        conn.autocommit(True)
        c = conn.cursor()
        sql = 'SELECT uid FROM `host_bastion_apply` WHERE `status`=3 group by uid'
        c.execute(sql)
        rows = c.fetchall()
        for row in rows:
            id = row[0]
            username = self.getDomainName(id)
            if username:
                self.do_bastion(id,username)
        ##用户key有变动
        sql = 'SELECT id,uid FROM `pubkey_changed_queue` WHERE `bastion_host_flag`=0  order by id asc limit 5'
        c.execute(sql)
        rows = c.fetchall()
        for row in rows:
            uid = row[1]
            id = row[0]
            username = self.getDomainName(uid)
            if username:
                self.do_bastion(uid,username)
                sql = "update pubkey_changed_queue set bastion_host_flag = 1 where id =%s" %id
                c.execute(sql)
        c.close()
        conn.close()
        end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print '-----------end:%s-------------'%end_time

    def do_bastion(self,id,username):
        home_dir = '/home/%s' %username
        key_file = '%s/.ssh/authorized_keys' % home_dir
        print key_file
        if not os.path.exists(home_dir):
            print 'Adding user %s' % username
            subprocess.check_call(['useradd', '-s', LOCAL_SHELL, '-m', username])
            ssh_dir = '/home/%s/.ssh' % username
            subprocess.check_call(['mkdir', ssh_dir])
            subprocess.check_call(['chown', '%s.%s' % (username, username), ssh_dir])
            subprocess.check_call(['chmod', '700', ssh_dir])

            key_file = '%s/authorized_keys' % ssh_dir
            subprocess.check_call(['touch', key_file])
            subprocess.check_call(['chown', '%s.%s' % (username, username), key_file])
            subprocess.check_call(['chmod', '600', key_file])


        keys = self.getkeys(id)
        if keys:
            keys = '%s\n'%keys
            with open(key_file, 'w') as f:
                f.write(keys)


    def getkeys(self,uid):
        conn = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PWD, MYSQL_DATABASE)
        conn.autocommit(True)
        c = conn.cursor()
        sql = 'SELECT `key` FROM `sshkey` WHERE `uid`=%s'%uid
        c.execute(sql)
        rows = c.fetchall()
        keys = []
        for row in rows:
            keys.append(row[0])
        return '\n'.join(keys)

    def getDomainName(self,uid):
        conn = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PWD, MYSQL_DATABASE)
        conn.autocommit(True)
        c = conn.cursor()
        sql = "select name from user where id =  %s" %uid
        c.execute(sql)
        row = c.fetchone()
        if row:
            return row[0]
        else:
            return ''


if __name__ == '__main__':
    target = Bastion_Account()
    target.run()




