# -*- coding: utf-8 -*-


from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Text, TIMESTAMP,DateTime
from sqlalchemy.dialects.mysql import TINYINT
from application import db
import datetime

class PUV(db.Model):
    __tablename__ = "puv"

    id= Column(Integer, primary_key=True)
    pv= Column(Integer,nullable=True)
    pv_nospider= Column(Integer,nullable=True)
    pv_nospider_m= Column(Integer,nullable=True)
    pv_nospider_p= Column(Integer,nullable=True)
    uv= Column(Integer,nullable=True)
    uv_m=Column(Integer,nullable=True)
    uv_p=Column(Integer,nullable=True)
    pv_uv= Column(Integer,nullable=True)

    pv_u= Column(Integer,nullable=True)
    pv_u_m= Column(Integer,nullable=True)
    pv_u_p= Column(Integer,nullable=True)

    uv_u= Column(Integer,nullable=True)
    uv_u_m= Column(Integer,nullable=True)
    uv_u_p= Column(Integer,nullable=True)

    pv_office=Column(Integer,nullable=True)
    pv_office_m=Column(Integer,nullable=True)
    pv_office_p=Column(Integer,nullable=True)

    pv_whitelist=Column(Integer,nullable=True)
    pv_whitelist_m=Column(Integer,nullable=True)
    pv_whitelist_p=Column(Integer,nullable=True)

    response_time=Column(Integer,nullable=True)
    request_time=Column(Integer,nullable=True)

    dataday= Column(String(40),nullable=True)
    hour=Column(String(40),nullable=True)
    time_f= Column(DateTime, nullable=False)

    def __init__(self, pv, pv_nospider, pv_nospider_m, pv_nospider_p, uv, uv_m, uv_p, pv_uv, dataday, hour,time_f,pv_u
                 ,pv_u_m ,pv_u_p ,uv_u ,uv_u_m ,uv_u_p ,pv_office ,pv_office_m ,pv_office_p ,pv_whitelist
                 ,pv_whitelist_m , pv_whitelist_p,response_time,request_time):
        self.pv      = pv
        self.pv_nospider = pv_nospider
        self.pv_nospider_m          = pv_nospider_m
        self.pv_nospider_p    = pv_nospider_p
        self.uv     = uv
        self.uv_m     = uv_m
        self.uv_p        = uv_p
        self.pv_uv           = pv_uv
        self.dataday        = dataday
        self.hour= hour
        self.time_f=time_f
        self.pv_u= pv_u
        self.pv_u_m= pv_u_m
        self.pv_u_p= pv_u_p
        self.uv_u= uv_u
        self.uv_u_m= uv_u_m
        self.uv_u_p= uv_u_p
        self.pv_office= pv_office
        self.pv_office_m= pv_office_m
        self.pv_office_p= pv_office_p
        self.pv_whitelist= pv_whitelist
        self.pv_whitelist_m= pv_whitelist_m
        self.pv_whitelist_p= pv_whitelist_p
        self.request_time=request_time
        self.response_time=response_time

    @property
    def date_descri(self):
        if(self.dataday) and self.hour:
            return self.dataday[0:4]+'/'+self.dataday[4:6]+'/'+self.dataday[6:8]+','+self.hour+':00:00'
        return ''