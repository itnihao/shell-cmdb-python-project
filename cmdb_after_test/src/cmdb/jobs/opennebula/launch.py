# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../..")#加入默认的扫描路径
from application import app
import getopt

'''
  Job运行统一入口 python launch.py -m EsRebuild
'''
if __name__ == "__main__":
    with app.app_context():
        opts, args = getopt.getopt(sys.argv[1:], "hm:p:")
        for op, mod in opts:
            if op == "-m":
                filename = mod.lower()
                import_string = "from %s import %s as  jobtarget"%(filename,mod)
                exec import_string
                target = jobtarget()
                target.run()
            elif op == "-h":
                print '''Job运行统一入口 用法如下:
    python launch.py -m xxx (xxx 表示模块名称,模块名称和文件必须一样,并且文件名称必须是小写)
    '''
                sys.exit()
