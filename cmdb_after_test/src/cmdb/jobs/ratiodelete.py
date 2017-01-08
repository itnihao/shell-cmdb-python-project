# -*- coding: utf-8 -*-
# 清理满载率数据,保留半年数据
# cron 每天3点15分

from application import app, db
from models.host_load_ratio import HostLoadRatio
from models.host_load_daily import HostLoadDaily

from models.pool_load_daily import PoolLoadDaily
from models.pool_load_ratio import PoolLoadRatio
import datetime

class RatioDelete:
    def run(self):
        print '-----------start------------'
        today = datetime.date.today()
        limit_day = today - datetime.timedelta(days=61)
        limit_dt = str(limit_day)+' 23:59:59'
        daily_limit_day = today - datetime.timedelta(days=734)
        daily_limit_dt = str(daily_limit_day)+' 23:59:59'
        print limit_dt
        print daily_limit_dt
        self.host_daily(daily_limit_dt)
        self.host_ratio(limit_dt)
        self.pool_daily(daily_limit_dt)
        self.pool_ratio(limit_dt)
        print '----------end---------------'

    #删除host 实时数据
    def host_ratio(self,limit_dt):
        HostLoadRatio.query.filter(HostLoadRatio.created <= limit_dt).delete()
        db.session.commit()
    #删除host 天数据
    def host_daily(self,limit_dt):
        HostLoadDaily.query.filter(HostLoadDaily.created <= limit_dt).delete()
        db.session.commit()

    #删除pool 实时数据
    def pool_ratio(self,limit_dt):
        PoolLoadRatio.query.filter(PoolLoadRatio.created <= limit_dt).delete()
        db.session.commit()
    #删除pool 天数据
    def pool_daily(self,limit_dt):
        PoolLoadDaily.query.filter(PoolLoadDaily.created <= limit_dt).delete()
        db.session.commit()


