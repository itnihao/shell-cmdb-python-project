from django.shortcuts import render
from django.http import HttpResponse,Http404
from models import *
from apps.idc import models as idc_models
from apps.dpt import models as dpt_models
from apps.accessory import models as accessory_models
from django.views.generic import View
from public.Syskeywords import db_code_mapping
from apps.auth.views import is_login, have_permission

# Create your views here.

class ServerBaseView(View):
    def __init__(self):
        self.context = {}
        self.context['base'] = "admin_bases.html"

class Index(ServerBaseView):

    #@have_permission
    @is_login
    def get(self, request, *args, **kwargs):
        server_obj = TServer.objects.all().exclude(delete_status=db_code_mapping['delete'])
        self.context['server_count']=server_obj.count()
        server_obj = server_obj.filter(server_operation_status=1).exclude(delete_status=db_code_mapping['delete'])
        self.context['server_free_count']=server_obj.count()
        position_obj = idc_models.TPosition.objects.all().exclude(delete_status=db_code_mapping['delete'])
        self.context['position_count']=position_obj.count()
        position_obj = idc_models.TPosition.objects.filter(position_status=1).exclude(delete_status=db_code_mapping['delete'])
        self.context['position_free']=position_obj.count()
        cluster_obj = dpt_models.TCluster.objects.all()
        self.context['cluster_count']=cluster_obj.count()
        self.context['username'] = request.session['username']
        return render(request, 'index.html', self.context)

class Server(ServerBaseView):

    #@have_permission
    @is_login
    def get(self, request, *args, **kwargs):
        self.context['incservertype'] = TIncServerType.objects.values('inc_server_type_name').distinct()
        self.context['servertype'] = TServer.SERVER_TYPE_MAPPING#TServer.objects.values('server_type').distinct()
        self.context['servermodel'] = TDeviceProducerType.objects.values('producer_name').distinct()
        self.context['username'] = request.session['username']
        return render(request, 'server_index.html', self.context)

#class AssignServer(ServerBaseView):
#    def get(self, request, *args, **kwargs):
#        self.context['cpu_capacity'] = accessory_models.TRealaccessory.objects.values('cpu_capacity').distinct()
#        self.context['disk_capacity'] = accessory_models.TRealaccessory.objects.values('disk_capacity').distinct()
#        self.context['memory_capacity'] = accessory_models.TRealaccessory.objects.values('memory_capacity').distinct()
#        return render(request, 'assign_server_index.html', self.context)
#
#    def post(self, request, *args, **kwargs):
#        self.context['cpu_info'] = request.POST.get('cpu_type')
#        self.context['disk_info'] = request.POST.get('hard_type')
#        self.context['mem_info'] = request.POST.get('mem_type')
#        self.context['cpu_capacity'] = accessory_models.TRealaccessory.objects.values('cpu_capacity').distinct()
#        self.context['disk_capacity'] = accessory_models.TRealaccessory.objects.values('disk_capacity').distinct()
#        self.context['memory_capacity'] = accessory_models.TRealaccessory.objects.values('memory_capacity').distinct()
#        return render(request, 'assign_server_index.html', self.context)

class Repairs(ServerBaseView):
    @is_login
    def get(self, request, *args, **kwargs):
        self.context['username'] = request.session['username']
        return render(request, 'repairs_index.html', self.context)


class RepairOrderForm(ServerBaseView):
    @is_login
    def get(self, request, *args, **kwargs):
        try:
            snCode = request.GET.get("sn")
            obj = TServer.objects.filter(asset_id__asset_sn=snCode)[0]
            self.context['sn'] = snCode
            self.context['deviceType'] = obj.asset_id.get_device_type_display()
            self.context['position'] = '-'.join([str(obj.asset_id.position_id.rack_id.rack_name),str(obj.asset_id.position_id.rack_id.rack_code),str(obj.asset_id.position_id.position_num)])
            self.context['repairState'] = obj.server_health_status
            self.context['dueTime'] = obj.asset_id.asset_warranty_due_time
            self.context['username'] = request.session['username']

            try:
                obj1 = TServerRepair.objects.filter(asset_id__asset_sn=snCode).order_by('repair_start_time')
                self.context['repairlog'] = obj1
                #self.context['repairReason'] = obj1.repair_context
                #self.context['stepcount'] = obj1.repair_status
            except Exception as e:
                pass
                #self.context['repairReason'] = ""
                #self.context['stepcount'] = 1

        except Exception as e:
            raise Http404

        return render(request, 'repairs_order_form.html', self.context)


class RresourcePool(ServerBaseView):
    @is_login
    def get(self, request, *args, **kwargs):
        resourcepool=dpt_models.TResourcePool.objects.all()
        self.context['resourcepool']=resourcepool
        self.context['username'] = request.session['username']
        return render(request, 'resource_index.html', self.context)

class PoolManagment(ServerBaseView):
    @is_login
    def get(self, request, *args, **kwargs):
        self.context['username'] = request.session['username']
        return render(request, 'reource_pool.html', self.context)

class BaseResource(ServerBaseView):
#    @is_login
    def get(self, request, *args, **kwargs):
        resourceID = request.GET.get('id')
        if not resourceID:
            resourceID = 0
        if int(resourceID)>3:
            raise Http404
        self.context['resourceID'] = resourceID
        self.context['username'] = request.session['username']
        return render(request, 'base_resource_index.html', self.context)
