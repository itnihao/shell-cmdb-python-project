__author__ = 'xiaoyucai'
import pyhs2
import datetime

class HiveClient:
    def __init__(self,db_host,user,database,password='',port=10000,authMechanism="PLAIN"):
        self.conn=pyhs2.connect(host=db_host,
                                port=port,
                                authMechanism=authMechanism,
                                user=user,
                                password=password,
                                database=database,
                                )

    def query(self,sql):
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetch()

    def close(self):
        self.conn.close()

class MysqlClient:
    def __init__(self):
        pass


def request_count_recently():
    hive_client=HiveClient(db_host='10.10.8.164',user='hdfs',database='alog')
    now=datetime.datetime.now()
    time=now.strftime("%Y-%m-%d %H:%M:%S")
    year=now.strftime("%Y")
    month=now.strftime("%m")
    day=now.strftime("%d")
    hour=now.strftime("%H")
    sql='select min, count(*)  from d_%s%s%s where hour=%s group by min' % (year,month,day,hour)
    print sql
    result=hive_client.query(sql)
    for i in result:
        print i
    hive_client.close()

def request_ip_recently():
    hive_client=HiveClient(db_host='10.10.8.164',user='hdfs',database='alog')
    now=datetime.datetime.now()
    time=now.strftime("%Y-%m-%d %H:%M:%S")
    year=now.strftime("%Y")
    month=now.strftime("%m")
    day=now.strftime("%d")
    hour=now.strftime("%H")
    sql='select remote_addr,count(*) as count from d_20150721 where hour = 17 and min > 3 and min < 5 group by remote_addr'
    sql='select min, count(*)  from d_%s%s%s where hour=%s group by min' % (year,month,day,hour)
    hive_client.close()

def main():
    with pyhs2.connect(host='10.10.8.164',
                       port=10000,
                       authMechanism="PLAIN",
                       user='hdfs',
                       password='',
                       database='alog'
                       ) as conn:
        with conn.cursor() as cur:
            print cur.execute("select remote_addr,count(*) as count from d_20150722 where hour=15 and min=30 group by remote_addr sort by count desc limit 20")
            print cur.getSchema()
            for i in cur.fetch():
                print i
if __name__ == '__main__':
    main()