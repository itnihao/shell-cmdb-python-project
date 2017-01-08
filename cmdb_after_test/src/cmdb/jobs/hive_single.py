import pyhs2
import time
import xlwt
import subprocess
from models.puv import *
from application import db

class Hive_single:
    def run(self):
        print "===========start==========="
        self.test()
        print "===========end============="

    conn=''
    data_pv=[]
    data_nospider_pv=[]
    data_nospider_pv_m=[]
    data_ip=[]
    data_ip_m=[]

    data_pv_office=[]
    data_pv_office_m=[]

    data_uv_office=[]
    data_uv_office_m=[]

    data_pv_whitlist=[]
    data_pv_whitlist_m=[]

    data_pv_u=[]

    data_response_time=[]
    data_request_time=[]
    fday=''
    limit=50

    def test(self):
        now_time =datetime.datetime.now()
        yes_time = now_time + datetime.timedelta(days=-1)
        self.fday = yes_time.strftime('%Y%m%d')

        # r=subprocess.call("ssh work@10.48.190.6 'hive -e \" select hour,AVG(request_time) from alog.d_20160107  group by hour\"'", shell=True)
        # print r
        # return
        # self.conn= pyhs2.connect(host='10.10.8.164',port=10000,authMechanism='PLAIN',user='chaojin',password='HON123well',database='alog')
        self.conn= pyhs2.connect(host='10.126.102.227',port=10000,authMechanism='PLAIN',user='hadoop',password='',database='alog')

        self.request_time()
        self.response_time()

        self.pv()
        self.pv_nospider()
        self.ip()
        self.pv_m()
        self.ip_m()
        self.pv_office()
        self.pv_office_m()
        self.pv_whitlist()
        self.pv_whitlist_m()


        # self.data_pv=[['04', 7429338], ['05', 7135196], ['06', 9165761], ['07', 11582127], ['08', 15971410], ['09', 26336106], ['10', 30922580], ['11', 28202055], ['12', 24290956], ['13', 26206880], ['14', 27861418], ['15', 30052877], ['16', 30080196], ['17', 27408290], ['18', 24321258], ['19', 25579743], ['20', 28503237], ['21', 28902383], ['22', 26055757], ['23', 19178970], ['00', 14320642], ['01', 10126671], ['02', 8027274], ['03', 6669678]]
        # self.data_nospider_pv=[['04', 6654448], ['05', 6393474], ['06', 8464367], ['07', 10904520], ['08', 15317043], ['09', 25586971], ['10', 30232837], ['11', 27538964], ['12', 23691771], ['13', 25562785], ['14', 27161059], ['15', 29417339], ['16', 29359182], ['17', 26647971], ['18', 23601106], ['19', 24845989], ['20', 27742180], ['21', 28132096], ['22', 25344841], ['23', 18461802], ['00', 13484789], ['01', 9347004], ['02', 7294637], ['03', 5935829]]
        # self.data_ip=[['04', 65438], ['05', 69563], ['06', 95408], ['07', 142422], ['08', 195829], ['09', 241486], ['10', 263719], ['11', 269966], ['12', 260768], ['13', 263171], ['14', 267337], ['15', 301762], ['16', 281912], ['17', 268644], ['18', 248607], ['19', 255186], ['20', 267635], ['21', 274120], ['22', 251771], ['23', 195634], ['00', 138591], ['01', 97017], ['02', 77487], ['03', 68857]]
        # self.data_nospider_pv_m=[['04', 1810894], ['05', 1964468], ['06', 2742942], ['07', 4163853], ['08', 5134219], ['09', 6340405], ['10', 8346049], ['11', 7442074], ['12', 7727823], ['13', 7916154], ['14', 7810090], ['15', 8444525], ['16', 8188713], ['17', 7653373], ['18', 7628473], ['19', 8938438], ['20', 10687680], ['21', 11820606], ['22', 11933092], ['23', 8758959], ['00', 5764498], ['01', 3341145], ['02', 2359787], ['03', 1928322]]
        # self.data_ip_m=[['04', 34373], ['05', 39259], ['06', 62978], ['07', 100906], ['08', 118690], ['09', 128796], ['10', 139035], ['11', 143385], ['12', 151488], ['13', 145205], ['14', 140398], ['15', 142480], ['16', 147895], ['17', 149885], ['18', 146932], ['19', 154350], ['20', 165902], ['21', 176167], ['22', 166378], ['23', 127521], ['00', 89736], ['01', 57392], ['02', 42795], ['03', 36606]]
        # self.data_pv_office=[['04', 747665], ['05', 686508], ['06', 889631], ['07', 1264693], ['08', 1711765], ['09', 2200275], ['10', 2637276], ['11', 2665304], ['12', 2817015], ['13', 2756672], ['14', 2724363], ['15', 2802302], ['16', 2853944], ['17', 2656316], ['18', 2374841], ['19', 2651915], ['20', 2980643], ['21', 3288003], ['22', 3376949], ['23', 2585100], ['00', 1827453], ['01', 1128992], ['02', 916097], ['03', 670585]]
        # self.data_pv_office_m=[['04', 29915], ['05', 36223], ['06', 63703], ['07', 97407], ['08', 123751], ['09', 152513], ['10', 173828], ['11', 162801], ['12', 174445], ['13', 172890], ['14', 163985], ['15', 164383], ['16', 163174], ['17', 156775], ['18', 159173], ['19', 184354], ['20', 212034], ['21', 243465], ['22', 242164], ['23', 180805], ['00', 122686], ['01', 68041], ['02', 41640], ['03', 32385]]
        # self.data_pv_whitlist=[['04', 142943], ['05', 149335], ['06', 158431], ['07', 217435], ['08', 548062], ['09', 746801], ['10', 945563], ['11', 909166], ['12', 826706], ['13', 826676], ['14', 824556], ['15', 865491], ['16', 830550], ['17', 758367], ['18', 719195], ['19', 773789], ['20', 874584], ['21', 910717], ['22', 923611], ['23', 440789], ['00', 295206], ['01', 200364], ['02', 188319], ['03', 150186]]
        # self.data_pv_whitlist_m=[['04', 610], ['05', 560], ['06', 1094], ['07', 3100], ['08', 10217], ['09', 28325], ['10', 52780], ['11', 37318], ['12', 25506], ['13', 25573], ['14', 29301], ['15', 37643], ['16', 30914], ['17', 30351], ['18', 26592], ['19', 27912], ['20', 35452], ['21', 22109], ['22', 18807], ['23', 11437], ['00', 4748], ['01', 1722], ['02', 871], ['03', 603]]
        # self.data_request_time=[['09', 191.5906512764462], ['10', 322.19374560476615], ['11', 196.45401349477729], ['12', 207.65164496848644], ['13', 245.32073096944595], ['14', 288.7520045038035], ['15', 235.4443292728712], ['16', 204.7204036457833], ['17', 209.185289216171], ['18', 229.6106372640924], ['19', 237.68049043487906], ['20', 259.9131858643712], ['21', 234.13261371884502], ['22', 236.53665563973962], ['23', 235.32348793605718], ['00', 260.4184725194794], ['01', 259.8724814925054], ['02', 276.52958333469985], ['03', 285.7949460148579], ['04', 264.09224524379937], ['05', 253.2665199672797], ['06', 231.56939744728274], ['07', 231.89636306896324], ['08', 206.03761432678093]]
        # self.data_response_time=[['09', 73.89710014301826], ['10', 197.86394609945023], ['11', 69.21909233933495], ['12', 61.8976461195546], ['13', 63.64431980020032], ['14', 63.88699122999483], ['15', 98.25964302079143], ['16', 66.4388131324401], ['17', 65.22119734002118], ['18', 64.83730607847434], ['19', 63.25918498390687], ['20', 88.86976154120376], ['21', 65.48364302777459], ['22', 62.70225857079036], ['23', 65.85484680890742], ['00', 65.82676124698467], ['01', 73.69012585997567], ['02', 79.10024415781524], ['03', 83.80836192399636], ['04', 82.07645309194966], ['05', 77.1825216194526], ['06', 72.93492336129793], ['07', 66.9451916758476], ['08', 62.75312942155944]]
        # self.data_pv=[['11', 31926030], ['12', 26570245], ['13', 27706460], ['14', 29983283], ['15', 31684052], ['16', 30369676],
        #          ['17', 27695302], ['18', 25567671], ['19', 27713306], ['20', 30738546], ['21', 30113929], ['22', 26183854],
        #          ['23', 19330249], ['00', 13327030], ['01', 8980689], ['02', 7504230], ['03', 6898389], ['04', 6129399],
        #          ['05', 6191977], ['06', 7760364], ['07', 9931335], ['08', 15370260], ['09', 26953476], ['10', 35548014]]
        #
        # self.data_nospider_pv=[['11', 31130632], ['12', 25817588], ['13', 26955555], ['14', 29075782], ['15', 31027000], ['16', 29955781],
        #          ['17', 27308403], ['18', 24820593], ['19', 26979353], ['20', 30007849], ['21', 29401213], ['22', 25518828],
        #          ['23', 18675890], ['00', 12612186], ['01', 8293281], ['02', 6802218], ['03', 6043664], ['04', 5327604],
        #          ['05', 5443425], ['06', 7056699], ['07', 9215194], ['08', 14625880], ['09', 26022517], ['10', 34695090]]
        #
        # self.data_ip=[['11', 303043], ['12', 286843], ['13', 278498], ['14', 282295], ['15', 288256], ['16', 291645], ['17', 278034],
        #          ['18', 263214], ['19', 270122], ['20', 279261], ['21', 283891], ['22', 256927], ['23', 201155], ['00', 141247],
        #          ['01', 101722], ['02', 82599], ['03', 73707], ['04', 70386], ['05', 74925], ['06', 101106], ['07', 144279],
        #          ['08', 201277], ['09', 242906], ['10', 304001]]

        if(not self.data_pv) or (not self.data_ip) or(not self.data_nospider_pv) \
                or (not self.data_nospider_pv_m) or (not self.data_ip_m):
            print 'get data error '
            return

        all_data=[]
        if len(self.data_pv_whitlist_m)<24:
           for d in range(0,24):
               d_f=str(d)
               if d<10:
                   d_f='0'+str(d)
               isExist_d=False
               for f in self.data_pv_whitlist_m:
                   if f[0]==d_f:
                       isExist_d=True
                       break
               if not isExist_d:
                    self.data_pv_whitlist_m.append([d_f,0])
        if len(self.data_pv_whitlist)<24:
           for d in range(0,24):
               d_f=str(d)
               if d<10:
                   d_f='0'+str(d)
               isExist_d=False
               for f in self.data_pv_whitlist:
                   if f[0]==d_f:
                       isExist_d=True
                       break
               if not isExist_d:
                    self.data_pv_whitlist.append([d_f,0])

        for i in range(0,24):
            all_data.append([self.data_pv[i][0],self.data_pv[i][1],self.data_nospider_pv[i][1],self.data_ip[i][1],
                             self.data_nospider_pv[i][1]/self.data_ip[i][1],self.data_nospider_pv_m[i][1]
                                ,self.data_ip_m[i][1],self.data_pv_office[i][1],self.data_pv_office_m[i][1],self.data_pv_whitlist[i][1]
                             ,self.data_pv_whitlist_m[i][1],self.data_response_time[i][1],self.data_request_time[i][1]])

        for insert_d in  all_data:
            dctarget=PUV(hour=insert_d[0],pv=insert_d[1],pv_nospider=insert_d[2],uv=insert_d[3],
                         pv_uv=(insert_d[2]-insert_d[7]-insert_d[9])/(insert_d[3]),
                         dataday=self.fday,pv_nospider_m=insert_d[5],pv_nospider_p=insert_d[2]-insert_d[5],
                         uv_m=insert_d[6],uv_p=insert_d[3]-insert_d[6],
                         time_f=datetime.datetime.strptime(self.fday+' '+insert_d[0]+':00:00','%Y%m%d %H:%M:%S'),
                         pv_office=insert_d[7],pv_office_m=insert_d[8],pv_office_p=insert_d[7]-insert_d[8],
                         pv_whitelist=insert_d[9],pv_whitelist_m=insert_d[10],pv_whitelist_p=insert_d[9]-insert_d[10],
                         pv_u=insert_d[2]-insert_d[7]-insert_d[9],pv_u_m=insert_d[5]-insert_d[8]-insert_d[10],
                         pv_u_p=(insert_d[2]-insert_d[7]-insert_d[9]-insert_d[5]+insert_d[8]+insert_d[10]),uv_u=0,uv_u_m=0,uv_u_p=0,
                         response_time=int(insert_d[11]),request_time=int(insert_d[12]))
            db.session.add(dctarget)
            db.session.commit()

# print(cur.getDatabases())

    def pv(self):
         with self.conn.cursor() as cur:
            sql_ex="select hour,count(user_agent) from %s group by hour" %('alog.d_'+self.fday)

            yy=cur.execute(sql_ex)
            self.data_pv= cur.fetch()
            print 'data_pv'
            print self.data_pv
        # print cur._currentBlock

    def pv_nospider(self):
        with self.conn.cursor() as cur:
        # sql_ex="select hour,count(user_agent) from d_20151126  where user_agent not  REGEXP '^spider\\' group by hour"
            sql_ex="select hour,count(user_agent) from %s  where user_agent not rlike '\\spider+' group by hour"%('alog.d_'+self.fday)
            xx=cur.execute(sql_ex)
            self.data_nospider_pv=cur.fetch()
            print 'data_nospider_pv'
            print self.data_nospider_pv
        # print cur._currentBlock

    def ip(self):
        with self.conn.cursor() as cur:

            sql_ex="select hour,count(DISTINCT remote_addr) from %s where user_agent not rlike '\\spider+' group by hour "%('alog.d_'+self.fday)
            zz=cur.execute(sql_ex)
            self.data_ip=cur.fetch()
            print 'data_ip'
            print self.data_ip
            # print cur._currentBlock

    def pv_m(self):
        with self.conn.cursor() as cur:
        # sql_ex="select hour,count(user_agent) from d_20151126  where user_agent not  REGEXP '^spider\\' group by hour"
            sql_ex="select hour,count(user_agent) from %s  where user_agent not rlike '\\spider+' " \
                   "and (user_agent rlike '\\iPhone+' or user_agent rlike '\\Android+' or user_agent rlike '\\iPad+')  group by hour"%('alog.d_'+self.fday)
            xx=cur.execute(sql_ex)
            self.data_nospider_pv_m= cur.fetch()
            print 'data_nospider_pv_m'
            print self.data_nospider_pv_m

    def ip_m(self):
        with self.conn.cursor() as cur:

            sql_ex="select hour,count(DISTINCT remote_addr) from %s where user_agent not rlike '\\spider+' " \
                   "and (user_agent rlike '\\iPhone+' or user_agent rlike '\\Android+' or user_agent rlike '\\iPad+') group by hour "%('alog.d_'+self.fday)
            zz=cur.execute(sql_ex)
            self.data_ip_m=cur.fetch()
            print 'data_ip_m'
            print self.data_ip_m

    def pv_office(self):
        with self.conn.cursor() as cur:
        # sql_ex="select hour,count(user_agent) from d_20151126  where user_agent not  REGEXP '^spider\\' group by hour"
            sql_ex="select hour,count(user_agent) from %s where (remote_addr rlike '\\10.10.+' or remote_addr rlike '\\10.20.+' or remote_addr rlike '\\192.168.+' or remote_addr='127.0.0.1') " \
                   "group by hour"%('alog.d_'+self.fday)

            xx=cur.execute(sql_ex)
            self.data_pv_office=cur.fetch()
            print 'data_pv_office'
            print self.data_pv_office

    def pv_office_m(self):
        with self.conn.cursor() as cur:
        # sql_ex="select hour,count(user_agent) from d_20151126  where user_agent not  REGEXP '^spider\\' group by hour"
            sql_ex="select hour,count(user_agent) from %s where (remote_addr rlike '\\10.10.+' or remote_addr rlike '\\10.20.+' or remote_addr rlike '\\192.168.+' or remote_addr='127.0.0.1') " \
                   "and (user_agent rlike '\\iPhone+' or user_agent rlike '\\Android+' or user_agent rlike '\\iPad+') group by hour"%('alog.d_'+self.fday)

            xx=cur.execute(sql_ex)
            self.data_pv_office_m=cur.fetch()
            print 'data_pv_office_m'
            print self.data_pv_office_m

    def pv_whitlist(self):
        with self.conn.cursor() as cur:
            f = open("hive_write_list.txt", 'r')
            add_str = ""
            for line in f.readlines():
                add_str += "\'%s\',"% line.strip()
            add_str = add_str[:-1]
            sql_ex = "select hour,count(user_agent) from %s where " \
                     "remote_addr in ( %s ) group by hour" % ('alog.d_' + self.fday, add_str)
            zz = cur.execute(sql_ex)

            self.data_pv_whitlist = cur.fetch()
            print 'data_pv_whitlist'
            print self.data_pv_whitlist

    def pv_whitlist_m(self):
        with self.conn.cursor() as cur:
            f = open("hive_write_list.txt", 'r')
            add_str = ""
            for line in f.readlines():
                add_str += "\'%s\',"% line.strip()
            add_str = add_str[:-1]
            sql_ex = "select hour,count(user_agent) from %s where " \
                     "(user_agent rlike '\\iPhone+' or user_agent rlike '\\Android+' or user_agent rlike '\\iPad+') " \
                     "and remote_addr in ( %s ) group by hour" % ('alog.d_' + self.fday, add_str)
            zz = cur.execute(sql_ex)

            self.data_pv_whitlist_m = cur.fetch()
            print 'data_pv_whitlist_m'
            print self.data_pv_whitlist_m

    def request_time(self):
        try:
            with self.conn.cursor() as cur:
                # f = open("hive_write_list.txt", 'r')
                # add_str = ""
                # for line in f.readlines():
                #     add_str += "\'%s\',"% line.strip()
                # add_str = add_str[:-1]
                sql_ex = "select hour,AVG(request_time) from %s group by hour" % ('alog.d_' + self.fday)
                zz = cur.execute(sql_ex)

                self.data_request_time = cur.fetch()
                print 'data_request_time'
                print self.data_request_time
        except Exception,e:
            print e
            exit()

    def response_time(self):
        try:
            with self.conn.cursor() as cur:
                # f = open("hive_write_list.txt", 'r')
                # add_str = ""
                # for line in f.readlines():
                #     add_str += "\'%s\',"% line.strip()
                # add_str = add_str[:-1]
                sql_ex = "select hour,AVG(upstream_response_time) from %s  group by hour" % ('alog.d_' + self.fday)
                zz = cur.execute(sql_ex)

                self.data_response_time = cur.fetch()
                print 'data_response_time'
                print self.data_response_time
        except Exception,e:
            print e
            exit()


def exportexcel(sheetname,head,content):
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet(sheetname)
        row = 1
        for column,name in enumerate(head):
            ws.write(0, column, name)
        for count,name in enumerate(content):
            for column,item in enumerate(name):
                ws.write(row, column, item)
            row += 1
        wb.save('puv_export.xlsx')


# head = ('hour','spider_pv','pv','uv','pv/uv')
# exportexcel('sheet1',head,all_data)
