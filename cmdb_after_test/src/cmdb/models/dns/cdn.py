# coding=utf-8
__author__ = 'qiqi'
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String
from application import db

class Cdn(db.Model):
    __tablename__ = 'cdn'

    id              = Column(Integer, primary_key=True)
    cdn             = Column(String(50), nullable=False)
    cdn_name        = Column(String(50), nullable=False)


    def __init__(self,cdn,cdn_name):
        self.cdn = cdn
        self.cdn_name  = cdn_name

    @property
    def cdn_descri_name(self):
        if self.cdn_name=='tencent':
            return '腾讯'
        elif self.cdn_name=='dnion':
            return '帝联'
        else:
            return '未知'