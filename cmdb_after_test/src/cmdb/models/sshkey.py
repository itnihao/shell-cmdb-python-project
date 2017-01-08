# -*- coding: utf-8 -*-

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, TIMESTAMP, TEXT
from application import db
from flask_login import current_user
import datetime

class Sshkey(db.Model):
    __tablename__ = "sshkey"

    id         = Column(Integer, primary_key=True)
    uid        = Column(Integer, nullable=False)
    name       = Column(String(20), nullable=False)
    key        = Column(TEXT, nullable=False)
    created    = Column(TIMESTAMP, nullable=False, server_default='0000-00-00 00:00:00')
    updated    = Column(TIMESTAMP, nullable=False, server_default='0000-00-00 00:00:00')

    def __init__(self, uid, name, key,created=""):
        self.uid     = uid
        self.name    = name
        self.key     = key
        if created:
            self.created = created
        else:
            self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated = self.created


    @property
    def short_key(self):
        if self.key:
            return '%s...%s' % (self.key[:20], self.key[-20:])
        else:
            return ""

