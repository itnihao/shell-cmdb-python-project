# -*- coding: utf-8 -*-

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Text, TIMESTAMP, DECIMAL
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT, FLOAT
from application import db
from datetime import datetime
from models.device_ip import DeviceIp
from models.ip_address import IpAddress
import json


class Device(db.Model):
    __tablename__ = "device"

    id            = Column(Integer, primary_key=True)
    device_cat_id = Column(Integer, nullable=False, index=True)
    supplier_id   = Column(Integer, nullable=False, index=True)
    model         = Column(String(20), nullable=False)
    frame_id      = Column(Integer,nullable=False,server_default='0')
    cpu           = Column(TINYINT(3), nullable=False, index=True)
    cpu_extra     = Column(Text, nullable=False)
    memory        = Column(FLOAT, nullable=False, index=True)
    memory_extra  = Column(Text, nullable=False)
    storage       = Column(Integer, nullable=False, index=True)
    storage_extra = Column(Text, nullable=False)
    rack_unit     = Column(TINYINT(1), nullable=False)
    sn            = Column(String(20), nullable=False)
    device_label  = Column(String(20), nullable=False)
    primary_mac   = Column(String(17), nullable=False)
    rack_id       = Column(Integer, nullable=False)
    rack_offset   = Column(TINYINT(2), nullable=False)
    primary_ip_id = Column(Integer, nullable=False, index=True)
    buy_time      = Column(TIMESTAMP, nullable=False, server_default='0000-00-00 00:00:00')
    elapsed_time  = Column(TIMESTAMP, nullable=False, server_default='0000-00-00 00:00:00')
    price         = Column(Integer, nullable=False)
    status        = Column(TINYINT(1), nullable=False, index=True)
    content       = Column(String(50), nullable=False)
    deleted       = Column(TINYINT(1), nullable=False, index=True, server_default='0')
    search        = Column(Text, nullable=False)
    created       = Column(TIMESTAMP, nullable=False, server_default='0000-00-00 00:00:00')
    updated       = Column(TIMESTAMP, nullable=False, server_default='0000-00-00 00:00:00')

    DELETED_NO = 0
    DELETED_YES = 1

    STATUS_BUY=1     #采购
    STATUS_START=2   #待装机 （上架，配置好远控卡ip）
    STATUS_READY=3   #待上线  (安装好操作系统）
    STATUS_ONLINE=4  #已上线 （设置好hostname,ip）
    STATUS_OFF=5     #下架


    def __init__(self):
        self.device_cat_id = ''
        self.supplier_id = ''
        self.model = ''
        self.cpu = 0
        self.cpu_extra = ''
        self.memory = 0
        self.memory_extra = ''
        self.storage = 0
        self.storage_extra = ''
        self.primary_ip_id = 0
        self.primary_mac = ''
        self.rack_unit = ''
        self.rack_id = ''
        self.rack_offset = ''
        self.sn = ''
        self.device_label = ''
        self.buy_time = datetime.now()
        self.elapsed_time = datetime.now()
        self.price = ''
        self.status = 0
        self.content = ''
        self.deleted = 0
        self.search = ''

    @staticmethod
    def net_names():
        return ['远控卡', '其他']

    def cpu_list(self):
        if self.cpu_extra:
            return json.loads(self.cpu_extra)

        return []

    def storage_list(self):
        if self.storage_extra:
            return json.loads(self.storage_extra)

        return []

    def service_term(self):
        year = 3
        if self.buy_time and self.elapsed_time:
            year = int(self.elapsed_time.strftime('%Y')) - int(self.buy_time.strftime('%Y'))
            if year == 0:
                year = 3

        return year

    def price_rmb(self):
        if self.price:
            return round(float(self.price) / 100, 2)

        return "未知"

    def rack_offsets(self):
        if self.rack_offset != 0:
            return self.rack_offset
        else:
            return "未知"

    def cpu_info(self):
        if self.cpu !=0:
            return "%d" %self.cpu
        else:
            return "未知"

    def memory_info(self):
        if self.memory !=0:
            if self.device_cat_id == 1:#服务器
                return "%dG" %self.memory
            else:
                return "%sG" %self.memory
        else:
            return "未知"

    def storage_info(self):
        if self.storage !=0:
            if self.storage >= 1000:
                return '%sT'%int(self.storage/1000)
            return "%dG" %self.storage
        else:
            return "未知"



    def update_nets(self, nets):
        from views.functions import _set_used_ip
        old_ips = DeviceIp.query.filter(DeviceIp.device_id == self.id).all()
        changed = False

        for ip in old_ips:
            if ip.ip_address_id in nets:
                info = nets[ip.ip_address_id]
                ip.net_name_id = info['net_name_id']
                ip.mac = info['mac']
                del nets[ip.ip_address_id]
            else:
                changed = True
                _set_used_ip(ip.ip_address_id)
                db.session.delete(ip)

        for ip_id in nets:
            changed = True
            info = nets[ip_id]

            _set_used_ip(ip_id, IpAddress.FLAG_USED, IpAddress.TYPE_DEVICE, self.id)

            dev_ip = DeviceIp()
            dev_ip.device_id = self.id
            dev_ip.ip_address_id = ip_id
            dev_ip.net_name_id = info['net_name_id']
            dev_ip.mac = info['mac']
            dev_ip.content = ''
            dev_ip.created = datetime.now()
            dev_ip.updated = datetime.now()
            db.session.add(dev_ip)

            if dev_ip.net_name_id == 0:
                self.primary_ip_id = ip_id
                self.primary_mac = dev_ip.mac

        return changed

    @property
    def model_descri(self):
        return self.model if len(self.model)>0 else '未知'

    @property
    def status_descri(self):
        if self.status == self.STATUS_BUY:
            return '采购流程'
        elif self.status == self.STATUS_START:
            return '待装机'
        elif self.status == self.STATUS_READY:
            return '待上线'
        elif self.status == self.STATUS_ONLINE:
            return '已上线'
        elif self.status == self.STATUS_OFF:
            return '下架'
        else:
            return  '未知'