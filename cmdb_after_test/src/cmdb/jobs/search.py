# -*- coding: utf-8 -*-

from application import db
from models.host import Host
from models.device import Device
from models.supplier import Supplier
from models.device_category import DeviceCategory
from models.rack import Rack
from models.datacenter import Datacenter

class Search:
    def run(self):#type=>1:host type=>2:device , status=>1:insert status=>2:update status=>3:delete
        print("====start====")
        host_info = Host.query.filter(Host.deleted == 0).order_by(Host.id).all()
        if host_info:
            print("====host====")
            for host in host_info:
                parentname = ""
                ip = ""
                sql = "select b.ipv4 from host_ip as a,ip_address as b where a.ip_address_id = b.id and a.host_id=%d"%host.id
                ipinfo = db.engine.execute(sql)
                if ipinfo:
                    for item in ipinfo:
                        ip = ip+" %s"%item.ipv4
                device_id = host.device_id
                hostname = host.hostname
                note = host.note
                type = host.type_descri
                if host.is_virtual == 1:
                    parentname = _get_host_name(host.parent_id)
                cpu = host.cpu_descri
                memory = host.memory_descri
                storage = host.storage_descri
                sql = "select b.ipv4 from device_ip as a,ip_address as b where a.ip_address_id = b.id and a.device_id=%d"%device_id
                ipsinfo=db.engine.execute(sql).fetchall()
                if ipsinfo:
                    for item in ipsinfo:
                        ip = ip+" %s"%item.ipv4
                host.search = "%s#@#%s#@#%s#@#%s#@#%s#@#%s#@#%s#@#%s"%(hostname, type, parentname, ip, cpu, memory, storage, note)
                db.session.commit()
        device_info = Device.query.filter(Device.deleted == 0).order_by(Device.id).all()
        if device_info:
            print("=====device=====")
            for device in device_info:
                supplier_name = ""
                supplier_short = ""
                category_name = ""
                category_short = ""
                ip = ""
                rack_name = ""
                datacenter_name = ""
                sn = device.sn
                label = device.device_label
                model = device.model
                cpu = device.cpu_info()
                memory = device.memory_info()
                storage = device.storage_info()

                supplier = Supplier.query.filter(Supplier.id == device.supplier_id).first()
                if supplier:
                    supplier_name = supplier.name
                    supplier_short = supplier.short_name

                device_category = DeviceCategory.query.filter(DeviceCategory.id == device.device_cat_id).first()
                if device_category:
                    category_name = device_category.name
                    category_short = device_category.short_name

                rack = Rack.query.filter(Rack.id == device.rack_id).first()
                if rack:
                    rack_name = rack.name
                    datacenter = Datacenter.query.filter(Datacenter.id == rack.datacenter_id).first()
                    datacenter_name = datacenter.name

                sql="select b.ipv4 from device_ip as a,ip_address as b where a.ip_address_id = b.id and a.device_id=%d"%device.id
                ipsinfo=db.engine.execute(sql).fetchall()
                if ipsinfo:
                    for item in ipsinfo:
                        ip=ip+" %s"%item.ipv4
                host_info = Host.query.filter(Host.device_id == device.id).first()
                if host_info:
                    host_id=host_info.id
                    sql="select b.ipv4 from host_ip as a,ip_address as b where a.ip_address_id = b.id and a.host_id=%d"%host_id
                    ipsinfo=db.engine.execute(sql).fetchall()
                    if ipsinfo:
                        for item in ipsinfo:
                            ip=ip+" %s"%item.ipv4
                device.search = "%s#@#%s#@#%s#@#%s#@#%s#@#%s#@#%s#@#%s#@#%s#@#%s#@#%s#@#%s#@#%s"%(label, sn, supplier_name, supplier_short, category_name, category_short, rack_name, datacenter_name, model, ip, cpu, memory, storage)
                db.session.commit()
        print("====end=====")

def _get_host_name(id):
    host_info = Host.query.filter(Host.id == id).first()
    if host_info:
        return str(host_info.hostname)

