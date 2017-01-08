# -*- coding: utf-8 -*-

from flask.ext.assets import Bundle

from application import assets_env
from views.public import public
from views.user import user
from views.server import server
from views.datacenter import datacenter
from views.ip import ip
from views.rack import rack
from views.pool import pool
from views.supplier import supplier
from views.host import host
from views.device import device
from views.log import log
from views.logger.index import logger
from views.monitor.index import monitor
from views.error import error
from views.tools import tools
from views.bastion import bastion
from views.pmz_search import pmz_search
from views.parts import parts
from views.sa.tickets import tickets
from views.sa.tickets_category import tickets_category
from views.sa.dns_category import dns_category

from views.sa.dns import dns
from views.orders.index import orders
from views.ldapgroup import *
from views.puv import *
from views.publics.excel import ExportExcel
# from views.ansible import *
# from views.ansible_work.ansible_playwork import *
from views.work import *
from views.woekpermission import *

css = Bundle('css/foundation.css','css/svgs/foundation-icons.css','css/cmdb.css',filters='cssmin', output='asset/layout.css')
js = Bundle('js/vendor/modernizr.js', 'js/vendor/jquery.js','js/jquery.cookie.js',"plugins/footable/js/footable.js","plugins/footable/js/footable.sort.js",'js/foundation.min.js','js/public.js',filters='jsmin', output='asset/layout.js')
assets_env.register("layout_css",css)
assets_env.register("layout_js",js)