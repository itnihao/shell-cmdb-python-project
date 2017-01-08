# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.assets import Environment
from flask_sqlalchemy import SQLAlchemy
import sys, os
from flask_util_js import FlaskUtilJs
from celery import Celery


reload(sys)
sys.setdefaultencoding('utf8')

class Application(Flask):
    def __init__(self, import_name):
        super(Application, self).__init__(import_name)
        self.config.from_pyfile('config.py')
        product_config = self.config.get("PRODUCT_CONFIG")
        if product_config and  os.path.isfile(product_config):
            self.config.from_pyfile(product_config)
        db.init_app(self)

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        if endpoint is None:
            endpoint = rule

        super(Application, self).add_url_rule(
            rule,
            endpoint=endpoint,
            view_func=view_func,
            **options
        )


def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

db = SQLAlchemy()
app = Application(__name__)
assets_env = Environment(app)
fujs=FlaskUtilJs(app)

app.config.update(
    CELERY_BROKER_URL=app.config['BROKER_URL'],
    CELERY_RESULT_BACKEND=app.config['BROKER_URL']
)
celery = make_celery(app)

# celery = Celery('cmdb', broker=app.config['BROKER_URL'],backend=app.config['BROKER_URL'])
# celery.conf.update(app.config)
# tmp = os.popen("export C_FORCE_ROOT='true'").readlines()
#
# os.popen("celery worker -A application.celery --loglevel=info &")

# ps -ef|grep celery |awk '{print $2}'| xargs kill -9
#export C_FORCE_ROOT="true"
#celery worker -A application.celery --loglevel=info &

@app.context_processor
def inject_fujs():
    return dict(fujs=fujs)


