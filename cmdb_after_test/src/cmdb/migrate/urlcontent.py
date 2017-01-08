# -*- coding: utf-8 -*-
from sqlalchemy import *
from models.action import Action
from application import db
import  re

class Urlcontent:
    def run(self):
        self.tag()
        #self.repair()

    def tag(self):
        actions = Action.query.all()
        for action in actions:
            action.tag = action.tag + "管理"
            db.session.commit()

    def repair(self):
        actions = Action.query.all()
        for action in actions:
            if re.match(r'.*add$',action.url):
                action.content = "添加" + action.tag.split("管理")[0]
            if re.match(r'.*modify$',action.url):
                action.content = "修改" + action.tag.split("管理")[0]
            if re.match(r'.*delete$',action.url):
                action.content = "删除" + action.tag.split("管理")[0]
            db.session.commit();