from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.generic import View
from apps.auth.views import is_login
from models import *

# Create your views here.

class DptBaseView(View):
    def __init__(self):
        self.context = {}
        self.context['base'] = "admin_bases.html"


class Cluster(DptBaseView):
    def get(self, request, *args, **kwargs):
        self.context['username'] = request.session['username']
        return render(request, 'cluster_index.html', self.context)


class ClusterUser(DptBaseView):
    @is_login
    def get(self, request, *args, **kwargs):
        cluster_id = request.GET.get('id')
        # cluster = TCluster.objects.get(cluster_id=cluster_id)
        # objs = TClusterUser.objects.filter(cluster_id=cluster_id)[:10]
        # users = []
        # for obj in objs:
        #     user = TBspUser.objects.get(bsp_user_id=obj.bsp_user_id)
        #     users.append({'user_name':user.account, 'is_admin':'obj.is_admin', 'op':'obj.op_type', 'cluster_id':'cluster_id','user_id':'user.id'})
        # self.context['cluster'] = cluster
        # self.context['users'] = users
        self.context['cluster_id'] = cluster_id
        self.context['username'] = request.session['username']
        return render(request, 'cluster_user.html', self.context)



class BusLine(DptBaseView):
     @is_login
     def get(self, request, *args, **kwargs):
        # buslines = TBusline.objects.all().order_by('-busline_id')[0:5]
        # return render(request, 'busline_index.html', {'buslines':buslines})
        self.context['username'] = request.session['username']
        return render(request, 'busline_index.html', self.context)


class DptLine(DptBaseView):
    @is_login
    def get(self, request, *args, **kwargs):
        dpts = TDpt.objects.all()[:5]
        # dpts={'name':12}
        # return render(request, 'dpt_index.html', {'dpts':dpts})
        self.context['username'] = request.session['username']
        return render(request, '01.html', self.context)


class OrgTree(DptBaseView):
    @is_login
    def get(self, request, *args, **kwargs):
        id = request.GET.get('id')
        if id is not None:
            self.context['dpt_id'] = id
        else:
            self.context['dpt_id'] = 0
        org_obj = TOrg.objects.filter(org_level='0').all()
        self.context['top_org'] = org_obj
        self.context['username'] = request.session['username']
        return render(request, 'orgtree_index.html', self.context)


class DptTree(DptBaseView):
    def get(self, request, *args, **kwargs):
        pass


class Dpt(DptBaseView):
    @is_login
    def get(self, request, *args, **kwargs):
        dpt_id = request.GET.get('pid')
        breads = []

        if dpt_id is None:
            dpts = TDpt.objects.filter(dpt_level=1)
        else:
            dpt_id = int(dpt_id)
            dpts = TDpt.objects.get(dpt_p_id=dpt_id)

        self.context['dpts'] = dpts
        self.context['username'] = request.session['username']
        return render(request, 'dpt_index.html', self.context)


class DptDetail(DptBaseView):
    # def display_views(self):
    #     view_classes = ['item-red', 'item-default', 'item-blue', 'item-grey', 'item-pink', 'item-green', 'item-orange']
    #     return view_classes
    @is_login
    def get(self, request, *args, **kwargs):
        dpt_id = request.GET.get('id')
        dpt = TDpt.objects.get(dpt_id=dpt_id)
        dpt_ops = dpt.dptuser.filter(op_type='0')[0:7]
        dpt_owns = dpt.dptuser.filter(op_type='1')[0:7]
        dpt_admins = dpt.dptuser.filter(is_admin='1')[0:7]



        self.context['dpt_owns'] = dpt_owns
        self.context['dpt_ops'] = dpt_ops
        self.context['dpt_admins'] = dpt_admins
        self.context['dpt'] = dpt

        # assoc department
        orgs  = dpt.orgdpt.all()
        self.context['orgs'] = orgs
        # self.context['org'] = orgs
        self.context['username'] = request.session['username']
        return render(request, 'dpt_detail.html', self.context)


# class BuslineDetail(DptBaseView):
#
#     def get(self, request, *args, **kwargs):
#         busline_id = request.GET.get('id')
#         busline = TBusline.objects.get(busline_id=busline_id)
#         self.context['busline'] = busline
#         return render(request, 'dpt_detail.html', self.context)


# class DptUser(DptBaseView):
#     def get(self, request, *args, **kwargs):
#         id = request.GET.get('id')
#         # self.context['is_none'] = 0
#         dpt_info = TDpt.objects.get(dpt_id=id)
#         self.context['dpt'] = dpt_info
#         dpt_users = TDptUser.objects.filter(dpt_id=id)
#         objs = []
#         for dpt_user in dpt_users:
#             user = TUserBsp.objects.get(id=dpt_user.bsp_user_id)
#             objs.append({'user_name':user.account, 'is_admin':dpt_user.is_admin, 'op':dpt_user.op_type, 'dpt_user_id':dpt_user.dpt_user_id})
#         self.context['users'] = objs
#         return render(request, 'dpt_user_index.html', self.context)



class DptUser(DptBaseView):
    @is_login
    def get(self, request, *args, **kwargs):
        id = request.GET.get('id')
        dpt = TDpt.objects.get(dpt_id=id)
        dpt_users = dpt.dptuser.all()
        self.context['dpt'] = dpt
        self.context['users'] = dpt_users
        self.context['username'] = request.session['username']
        return render(request, 'dpt_user_index.html', self.context)


class DptLevel(DptBaseView):

    def list_bread(self, *args):
        pass

    @is_login
    def get(self, request, *args, **kwargs):
        dpt_id = request.GET.get('id')
        dpts = TDpt.objects.filter(dpt_p_id = dpt_id)
        self.context['dpts'] = dpts
        breads  = []
        if not int(dpt_id) == 0:
            if not dpts:
                p_dpt = TDpt.objects.get(dpt_id = dpt_id)
            else:
                p_dpt = dpts[0].dpt_p
            self.context['p_dpt'] = p_dpt
            for i in range(int(p_dpt.dpt_level)-1):
                bread = {'name':p_dpt.dpt_name, 'id':p_dpt.dpt_id}
                breads.append(bread)
                p_dpt = TDpt.objects.get(dpt_id =p_dpt.dpt_p_id)
            breads.append({'name':p_dpt.dpt_name, 'id':p_dpt.dpt_id})
            breads.append({'name':'top','id':0})
            breads.reverse()
        else:
            self.context['p_dpt'] = {'p_dpt':0, 'dpt_level':1}

        self.context['breads'] = breads
        self.context['username'] = request.session['username']
        return render(request, 'dpt_index.html', self.context)


class BusLineUser(DptBaseView):
    @is_login
    def get(self, request, *args, **kwargs):
        id = request.GET.get('id')
        busline = TBusline.objects.get(busline_id=id)
        objs = TBuslineUser.objects.filter(busline_id=id)[0:5]
        users = []
        for obj in objs:
            user = TUserBsp.objects.get(id=obj.bsp_user_id)
            users.append({'id':obj.busline_user_id, 'user_name':user.account, 'op':obj.op_type, 'is_admin':obj.is_admin})


        self.context['users'] =  users
        self.context['busline'] = busline
        self.context['username'] = request.session['username']
        return render(request, 'busline_user_index.html', self.context)

# class DptOrg(DptBaseView):
#     def get(self, request, *args, **kwargs):



class BusLineDpt(DptBaseView):
    @is_login
    def get(self, request, *args, **kwargs):
        id = request.GET.get('id')
        busline_obj = TBusline.objects.get(busline_id=id)
        self.context['busline'] = busline_obj
        dpt_objs = TDpt.objects.filter(dpt_level='1').all()
        self.context['top_dpt'] = dpt_objs
        self.context['username'] = request.session['username']
        return render(request, 'dpttree_index.html', self.context)


class ClusterBusline(DptBaseView):
    @is_login
    def get(self, request, *args, **kwargs):
        id = request.GET.get('id')
        busline_obj = TCluster.objects.get(cluster_id=id)
        self.context['cluster'] = busline_obj
        objs =  TClusterBusline.objects.filter(cluster_id=id)
        buslines = []
        for obj in objs:
            busline = TBusline.objects.get(busline_id=obj.busline_id)
            buslines.append({'code':busline.busline_code, 'name':busline.busline_name, 'id':obj.cluster_busline_id})
        self.context['buslines'] = buslines
        self.context['username'] = request.session['username']

        return render(request, 'cluster_busline.html', self.context)



class BusLineDetail(DptBaseView):
    @is_login
    def get(self, request, *args, **kwargs):
        busline_id = request.GET.get('id')
        busline = TBusline.objects.get(busline_id=busline_id)
        self.context['busline'] = busline
        self.context['busline_id'] = busline.busline_id
        self.context['busline_code'] = busline.busline_code
        self.context['busline_name'] = busline.busline_name
        self.context['owner_op'] = busline.owner_op.nickname
        self.context['owner_biz'] = busline.owner_biz.nickname
        self.context['owner_op_id'] = busline.owner_op.bsp_user_id
        self.context['owner_biz_id'] = busline.owner_biz.bsp_user_id
        self.context['busline_level'] = busline.busline_level
        self.context['is_leaf'] = busline.is_leaf
        self.context['fullpath'] = busline.fullpath
        self.context['description'] = busline.description
        self.context['state'] = busline.state
        self.context['parent'] = busline.parent_id
        self.context['username'] = request.session['username']
        if len(busline.bsp_org_id)>0:
            self.context['bsporg'] = busline.bsp_org_id
        else:
            self.context['bsporg'] = '-1'
        self.context['parent_name'] = busline.parent.busline_name
        try:
            self.context['bsporg_name'] = busline.bsp_org.org_name
        except Exception as e:
            self.context['bsporg_name'] = ""
        return render(request, 'busline_detail.html', self.context)
