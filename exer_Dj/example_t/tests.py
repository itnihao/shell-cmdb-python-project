# coding: utf-8
# from __future__ import unicode_literals
import requests
from flask import render_template,Flask
app = Flask(__name__)

session = requests.session()

@app.route('/')
def index():
    data = session.get('http://ops.corp.anjuke.com/api/cmdb/host/')# print data.json()
    host = []
    for x in data.json()['list']:
        host.append(x['hostname'])
    return render_template("/test.html",host=host)

if __name__ == '__main__':
    app.run()


