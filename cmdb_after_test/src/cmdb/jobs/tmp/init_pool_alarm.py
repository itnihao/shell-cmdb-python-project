# -*- coding: utf-8 -*-
from models.pool import Pool
from models.alarm import Alarm
from application import db
from sqlalchemy import and_

class Init_pool_alarm:
    def run(self):
        print '-------start--------'
        type = 1
        pool_info = Pool.query.all()
        for item in pool_info:
            target_id = item.id
            uid_list = []
            ops_owner = item.ops_owner
            uid_list.append(ops_owner)
            team_owner = item.team_owner
            uid_list.append(team_owner)
            biz_owner = item.biz_owner
            uid_list.append(biz_owner)
            for uid in uid_list:
                Alarm_info = Alarm.query.filter(and_(Alarm.uid == uid, Alarm.target_id == target_id, Alarm.type == 1)).all()
                if Alarm_info:
                    continue
                else:
                    target = Alarm(type,target_id,uid)
                    db.session.add(target)
                    db.session.commit()
        print 'end'



