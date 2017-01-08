# -*- coding: UTF-8 -*-
from sqlalchemy import and_, or_
from flask import Blueprint, render_template, url_for, redirect, request, flash, make_response,jsonify
from flask_login import login_required, current_user
from application import app, db,celery
import time, datetime, re, json
from views.bastion import add_authority
from views.log import addlog
from views.functions import _set_used_ip, zabbix_rmhost, addmail, visible, responsejson
from config import DOMAIN
from pypages import Paginator
from tasks import host_device_changed
import xlwt, StringIO
from werkzeug.utils import secure_filename
from application import fujs
import xlrd
import os,random
from flask_socketio import SocketIO, emit, join_room, disconnect
from threading import Thread
from celery import Celery
from ansible_work.ansible_playwork import get_pb

ansible = Blueprint('ansible', __name__)

# thread = None
# def background_stuff():
#     """ Let's do it a bit cleaner """
#     while True:
#         time.sleep(1)
#         t = str(time.clock())
#         socketio.emit('message', {'data': 'This is data', 'time': t}, namespace='/test')
#
#
#
# @ansible.route('/')
# def index():
#     global thread
#     if thread is None:
#         thread = Thread(target=background_stuff)
#         thread.start()
#     return render_template('ansible/ansible.html')
#
# @socketio.on('my event', namespace='/test')
# def my_event(msg):
#     print msg['data']
#
# @socketio.on('connect', namespace='/test')
# def test_connect():
#     emit('my response', {'data': 'Connected', 'count': 0})
#
#
# @socketio.on('disconnect', namespace='/test')
# def test_disconnect():
#     print('Client disconnected')

# celery = Celery('cmdb', broker=app.config['BROKER_URL'])
# celery.conf.update(app.config)

# celery = Celery('cmdb')
# celery.config_from_object(app.config)
# celery.worker_main(argv=[''])

@ansible.route('/')
@login_required
def index():
    return render_template('ansible/ansible.html')

@celery.task(bind=True)
def long_task(self):
    """ Let's do it a bit cleaner """


    # verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    # adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    # noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    # message = ''
    # total = random.randint(10, 50)
    # for i in range(total):
    #     if not message or random.random() < 0.25:
    #         message = '{0} {1} {2}...'.format(random.choice(verb),
    #                                           random.choice(adjective),
    #                                           random.choice(noun))
    #     self.update_state(state='PROGRESS',
    #                       meta={'current': i, 'total': total,
    #                             'status': message})
    #     time.sleep(1)
    # return {'current': 100, 'total': 100, 'status': 'Task completed!',
    #         'result': 42}
    self.logs = []
    r = get_pb(self).run()
    self.logs.append("finish playbook")
    self.logs.append(str(r))
    return self.logs

    # message='running'
    # for i in range(0,10):
    #     time.sleep(5)
    #     t = str(time.clock())
    #     print i
    #     self.update_state(state='PROGRESS',
    #                       meta={'current': i,
    #                             'status': message})
    #     time.sleep(1)
    # return {'current': 100, 'status': 'SUCCESS'}

@ansible.route('/test',methods=['GET', 'POST'])
@login_required
def test():
    # r = get_pb('xx').run()
    task = long_task.apply_async()
    # task.wait()
    return jsonify({}), 202, {'Location': url_for('ansible.taskstatus',task_id=task.id)}

@ansible.route('/taskstatus/<task_id>',methods=['GET', 'POST'])
@login_required
def taskstatus(task_id):
    # task = long_task.AsyncResult(task_id)
    # print task.state
    # if task.state == 'PENDING':
    #     response = {
    #         'state': task.state,
    #         # 'current': 0,
    #         # 'total': 1,
    #         'status': 'Pending...'
    #     }
    # elif task.state != 'FAILURE':
    #     response = {
    #         'state': task.state,
    #         # 'current': task.info.get('current', 0),
    #         # 'total': task.info.get('total', 1),
    #         # 'status': task.info.get('status', '')
    #     }
    #     # if 'result' in task.info:
    #     #     response['result'] = task.info['result']
    # else:
    #     # something went wrong in the background job
    #     response = {
    #         'state': task.state,
    #         # 'current': task.info['current'],
    #         # 'total': 1,
    #         # 'status': str(task.info),
    #     }
    # return jsonify(response)

    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'status': task.info
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'status': task.info,  # this is the exception raised
        }
    return jsonify(response)