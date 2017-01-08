from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import View
from models import *
from public.APIViews import JSONResponse
from public.Syskeywords import db_code_mapping
from public.Exceptions import APIError
from apps.dpt import models as dpt_models
import hashlib
from datetime import datetime, timedelta
import time
import urllib,urllib2
import json

# Create your views here.

class Auth(JSONResponse, View):

    def get(self, request, *args, **kwargs):

        self.args = args
        self.kwargs = kwargs
        self.request = request
        self.expires_in = 7200
        self.token = ''

        if self.request.GET.has_key('apikey') and self.request.GET.has_key('script'):
            apikey = self.request.GET.get('apikey')
            script = self.request.GET.get('script')
            script = self.md5(script)
            try:
                flag, self.token = self.create_or_update_token(apikey, script)
                if flag:
                    context = {'token': self.token, 'expires_in': self.expires_in}
                    return JSONResponse.success(self, context)
                else:
                    return JSONResponse.invalid(self)
            except:
                return JSONResponse.invalid(self)

        else:
            return JSONResponse.invalid(self)


    def create_or_update_token(self, key, script):
        obj = TAuth.objects.filter(apiid = key)[0]
        if obj and obj.apiid == key and obj.script == script:
            now = datetime.now()
            t = now + timedelta(seconds = self.expires_in)
            obj.exp_time = t
            raw = key + script + str(time.time()*1000)
            obj.token = self.md5(raw)

            obj.save()
            return True, obj.token
        else:
            return False, '0'


    def md5(self, raw):
        m = hashlib.md5()
        m.update(raw)
        return m.hexdigest()


def is_login(func):
    def warpper(self, *args, **kwargs):
        request = self.request
        go = request.META['PATH_INFO']
        # print request.COOKIES
        if not sso(request):
            url = "https://sso.58corp.com/login/go?url=http://cmdb.58corp.com%s" % (go)
            return HttpResponseRedirect(url)
        else:
            return func(self, *args, **kwargs)
    return warpper


def have_permission(func):
    def warpper(self, *args, **kwargs):
        self.context = {}
        request = self.request
        uri = request.path
        self.context['username'] = request.session['username']
        if uri in request.session['operation'] and request.method == request.session['operation'][uri]:
            return func(self, *args, **kwargs)
        else:
            # return HttpResponse(status=403)
            return render(request, '403.html', self.context)

    return warpper

def sso(request):
    # cookies = request.COOKIES
    # url = "http://sso.web.58dns.org/login/get_user_data"
    # userid = cookies['Sso_UserID']
    # ssid = cookies['Sso_ssid']
    # data = {'UserID':userid, 'SSID':ssid}
    # print data
    # data = urllib.urlencode(data)
    # req = urllib2.Request(url, data)
    # response = urllib2.urlopen(req)
    # page = response.read()
    # page = json.loads(page)
    # info = page['result']
    # bsp_user_id = info['id']
    # account = info['userName']
    #
    # user = dpt_models.TBspUser.objects.filter(bsp_user_id=bsp_user_id)
    # if user:
    #     request.session['username'] = account
    #     request.session['bsp_user_id'] = bsp_user_id
    #     request.session['operation'] = GetPermissions(user)
    #     print request.session['operation']
    #     return 1
    # else:
    #     return 0
    #
    try:
        cookies = request.COOKIES
        url = "http://sso.web.58dns.org/login/get_user_data"
        userid = cookies['Sso_UserID']
        ssid = cookies['Sso_ssid']
        data = {'UserID':userid, 'SSID':ssid}
        data = urllib.urlencode(data)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        page = response.read()
        page = json.loads(page)
        info = page['result']
        bsp_user_id = info['id']
        account = info['userName']

        user = dpt_models.TBspUser.objects.filter(bsp_user_id=bsp_user_id)
        if user:
            request.session['username'] = account
            request.session['bsp_user_id'] = bsp_user_id
            request.session['operation'] = GetPermissions(user)
            GetRole(account)
            # print request.session['operation']
            return 1
        else:
            return 0
    except:
        return 0

def GetPermissions(userobj):
    d = {}
    user_group = TUserGroup.objects.filter(user=userobj)
    group_obj = [i.group for i in user_group]

    role = TGroupRole.objects.filter(group__in = group_obj)
    role = [ i.role for i in role]

    m_r_p = TRoleModularPermissionsType.objects.filter(role__in = role)

    for i in m_r_p:
        # print i.modular.modularname, i.permission.permission
        o = TModularOperation.objects.filter(modular = i.modular)
        for j in o:
            if j.operation.permission.permission == i.permission.permission and j.operation.permission_status:
                # print j.operation.uri, j.operation.http_method, j.operation.permission_status
                d[j.operation.uri] = j.operation.http_method
    print d


    # permission = [ i.permission for i in m_r_p ]
    #
    # modular = [ i.modular for i in m_r_p ]
    # m_o = TModularOperation.objects.filter(modular__in = modular)
    #
    # operation =  [ i.operation for i in m_o if i.operation.permission in permission ]
    #
    # for i in operation:
    #     # print i.uri, i.permission.permission, i.permission_status
    #     d[i.uri] = i.http_method
    return d

def GetRole(user):
    try:
        userobj = dpt_models.TBspUser.objects.filter(account=user)
        user_group = TUserGroup.objects.filter(user=userobj)
        group_obj = [i.group for i in user_group]

        role = TGroupRole.objects.filter(group__in = group_obj)
        role = [ i.role for i in role]
        return role[0].rolename
    except:
        return None



class AuthBaseView(View):
    def __init__(self):
        self.context = {}


class UserManager(AuthBaseView):
    @have_permission
    @is_login
    def get(self, request, *args, **kwargs):
        self.context['username'] = request.session['username']
        return render(request, 'user_manager_index.html', self.context)

class UserGroupManager(AuthBaseView):
    @have_permission
    @is_login
    def get(self, request, *args, **kwargs):
        self.context['username'] = request.session['username']
        return render(request, 'usergroup_manager_index.html', self.context)

class RoleManager(AuthBaseView):
    @have_permission
    @is_login
    def get(self, request, *args, **kwargs):
        self.context['username'] = request.session['username']
        return render(request, 'role_manager_index.html', self.context)

class LogOut(AuthBaseView):
    @is_login
    def get(self, request, *args, **kwargs):
        url = "https://sso.58corp.com/login/go?url=http://cmdb.58corp.com"
        try:
            del request.session['username']
            del request.session['bsp_user_id']
            del request.session['operation']
            return HttpResponseRedirect(url)
        except:
            return HttpResponseRedirect(url)
