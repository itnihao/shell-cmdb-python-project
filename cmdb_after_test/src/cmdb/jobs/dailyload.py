# -*- coding: utf-8 -*-

from sqlalchemy import *
from flask.ext.script import Manager
from application import app, db
from models.host import Host
from models.pool import Pool
from models.pool_load_daily import PoolLoadDaily
from models.pool_load_ratio import PoolLoadRatio
from models.host_load_ratio import HostLoadRatio
from models.host_load_daily import HostLoadDaily
import datetime


class DailyLoad:
    def run(self):
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        end = str(yesterday)+' 23:59:59'
        start = str(yesterday)+' 00:00:00'
        print(yesterday)
        self.daily_pool_load(end, start)
        self.daily_host_load(end, start)

    def daily_pool_load(self, today, yesterday):
        print "daily_pool_load"
        poolinfo = Pool.query.all()
        for pool in poolinfo:
            count = PoolLoadRatio.query.filter(and_(PoolLoadRatio.created.between(yesterday,today),PoolLoadRatio.pool_id == pool.id)).count()
            if count > 20:
                num = int(count*0.05)-1
            else:
                num = 0
            loadratio = PoolLoadRatio.query.filter(and_(PoolLoadRatio.created.between(yesterday,today),PoolLoadRatio.pool_id == pool.id)).order_by(PoolLoadRatio.ratio.desc()).offset(num).limit(1).first()
            if loadratio:
                daily_ratio = loadratio.ratio
                daily_poolid = pool.id
                daily_created = yesterday
                target = PoolLoadDaily(pool_id=daily_poolid, ratio=daily_ratio, created=daily_created)
                db.session.add(target)
                db.session.commit()

    def daily_host_load(self, today, yesterday):
        print "daily_host_load"
        hostinfo = Host.query.filter(Host.deleted == 0).all()
        for host in hostinfo:
            count = HostLoadRatio.query.filter(and_(HostLoadRatio.created.between(yesterday,today),HostLoadRatio.host_id == host.id)).count()
            if count > 20:
                num = int(count*0.05)-1
            else:
                num = 0
            loadratio = HostLoadRatio.query.filter(and_(HostLoadRatio.created.between(yesterday,today),HostLoadRatio.host_id == host.id)).order_by(HostLoadRatio.ratio.desc()).offset(num).limit(1).first()
            if loadratio:
                daily_ratio = loadratio.ratio
                daily_hostid = host.id
                daily_created = yesterday
                target = HostLoadDaily(host_id=daily_hostid, ratio=daily_ratio, created=daily_created)
                db.session.add(target)
                db.session.commit()
