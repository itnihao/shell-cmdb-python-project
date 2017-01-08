# -*- coding: utf-8 -*-

from sqlalchemy.schema import Column
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.types import Integer, String, TIMESTAMP
from application import db
import datetime

class DnsZone(db.Model):

    __tablename__ = "dns_zone"

    id              = Column(Integer, primary_key=True)
    uid             = Column(Integer, nullable=False)
    zone            = Column(String(50), nullable=False) #域名后缀
    type            = Column(TINYINT, nullable=False) #0：个人域名OFFICE，1：公网域名IDC外部 2：IDC内部
    display         = Column(TINYINT, nullable=False) #0：不显示，1：显示 下拉框里是否显示
    content         = Column(String(255), nullable=False)
    created         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')

    TYPE_OFFICE = 0
    TYPE_IDC_OUT = 1
    TYPE_IDC_IN = 2
    TYPE_CDN = 3

    DISPLAY_YES = 1
    DISPLAY_NO = 0


    def __init__(self,uid,zone,type,display,content):
        self.uid     = uid
        self.zone    = zone
        self.type    = type
        self.display = display
        self.content = content
        self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated = self.created

    @property
    def type_descri(self):
        if self.type==0:
            return 'OFFICE'
        elif self.type==1:
            return 'IDC外部'
        elif self.type==2:
            return 'IDC内部'
        elif self.type==3:
            return 'CDN'
        else:
            return '未知'

    @property
    def display_descri(self):
        if self.display == 1:
            return '对外可见'
        else:
            return '对外不可见'