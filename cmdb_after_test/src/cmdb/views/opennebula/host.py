# -*- coding: utf-8 -*-
from views.oca.host import Host

class Oca_Host:
    def __init__(self,client):
        self.client = client

    def info(self):
        xml = '''<?xml   version="1.0"   encoding="utf-8"?>
<TEMPLATE>
<ID>1001</ID>
</TEMPLATE>'''
        try:
            h =  Host(xml,self.client)
            h.info()
            print h.id
            tp = h.__getattr__("TEMPLATE")
            for item in tp:
                print item.tag,item.text
        except:
            import traceback
            traceback.print_exc()