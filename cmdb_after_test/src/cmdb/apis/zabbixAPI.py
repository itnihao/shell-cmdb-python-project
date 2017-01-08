# coding=utf-8
__author__ = 'qiqi'

from application import app
import json
import urllib2

class ZABBIX_API():
    auth_id = ''

    def zabbix_request(self,data):
        url = app.config.get('ZABBIX_URL')
        header = {"Content-Type": "application/json"}
        request = urllib2.Request(url,json.dumps(data))
        for key in header:
            request.add_header(key,header[key])
        try:
            result = urllib2.urlopen(request)
        except urllib2.URLError as e:
            print "Auth Failed, Please Check Your Name And Password:",e.code
            return False
        else:
            response = json.loads(result.read())
            result.close()
            return response['result']

    def connect(self):
        data = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
            "user": app.config.get('ZABBIX_USER'),
            "password": app.config.get('ZABBIX_PASS')
            },
            "id": 0
        }
        self.auth_id = self.zabbix_request(data)
        if self.auth_id == '':
            return False
        else:
            return True

    def disconnect(self):
        data = {
            "jsonrpc": "2.0",
            "method": "user.logout",
            "params": [],
            "id": 1,
            "auth": self.auth_id,
        }
        return self.zabbix_request(data)

    def get_host(self):
        data = {
            "jsonrpc":"2.0",
            "method":"host.get",
            "params":{
                "output":["hostid","name"],
                "filter":{"host":""}
            },
            "auth":self.auth_id,
            "id":1,
        }
        return self.zabbix_request(data)

    def get_alerts(self):
        data = {
            "jsonrpc": "2.0",
            "method": "alert.get",
            "params": {
                "output": "extend",
                "sortorder": "alertid",
                "limit": "5"
            },
            "auth": self.auth_id,
            "id": 1
        }
        return self.zabbix_request(data)

    def get_triggers(self):
        data = {
            "jsonrpc": "2.0",
            "method": "trigger.get",
            "params": {
                "output": "extend",
                "expandData": "hostname",
                "monitored":"1",
                # "maintenance":True,
                # "only_true": "1",
                "filter":{"value": 1}
            },
            "auth": self.auth_id,
            "id": 1
        }
        return self.zabbix_request(data)


