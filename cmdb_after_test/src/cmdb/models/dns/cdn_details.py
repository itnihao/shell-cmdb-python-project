# coding=utf-8
__author__ = 'qiqi'

from sqlalchemy.schema import Column
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.types import Integer, String, TIMESTAMP
from application import db
import datetime

class CdnDetails(db.Model):
    __tablename__ = 'cdn_details'

    id              = Column(Integer, primary_key=True)
    prefix          = Column(String(50), nullable=False)
    zone_id         = Column(Integer, nullable=False) #域名后缀 对应域名表中id
    area            = Column(TINYINT,nullable=False)
    cdn_id          = Column(Integer,nullable=False)
    visits           = Column(Integer)  #访问量
    created         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')

    AREA_DEFAULT = 0
    AREA_HUADONG = 1
    AREA_HUANAN = 2
    AREA_HUABEI = 3
    AREA_XIBU = 4

    def __init__(self,prefix,zone_id,area,cdn_id,visits):
        self.prefix  = prefix
        self.zone_id = zone_id
        self.area    = area
        self.cdn_id   = cdn_id
        self.visits     = visits
        self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated = self.created

    @property
    def area_descri(self):
        if self.area==0:
            return '默认'
        elif self.area==1:
            return '华东'
        elif self.area==2:
            return '华南'
        elif self.area==3:
            return '华北'
        elif self.area==4:
            return '西部'
        else:
            return '未知'

    @property
    def area_descri_pinyin(self):
        if self.area==0:
            return 'default'
        elif self.area==1:
            return 'hudong'
        elif self.area==2:
            return 'huanan'
        elif self.area==3:
            return 'huabei'
        elif self.area==4:
            return 'xibu'
        else:
            return 'unknow'