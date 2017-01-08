from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.views.generic import View
from models import *
from public.Syskeywords import db_code_mapping
from apps.auth.views import is_login

# Create your views here.

class IdcBaseView(View):
    def __init__(self):
        self.context = {}
        self.context['base'] = "admin_bases.html"

class Idc(IdcBaseView):
    @is_login
    def get(self, request, *args, **kwargs):
        self.context['username'] = request.session['username']
        return render(request, 'idc_index.html', self.context)

class Rack(IdcBaseView):
    @is_login
    def get(self, request, *args, **kwargs):
        idc_id = request.GET.get('idc_id')
        if idc_id is None:
            raise Http404

        rack_obj = TRack.objects.filter(idc_id=idc_id).exclude(delete_status=db_code_mapping['delete'])
        self.context['rack_obj'] = rack_obj
        self.context['username'] = request.session['username']
        return render(request, 'rack_index.html', self.context)

class Position(IdcBaseView):
    @is_login
    def get(self, request, *args, **kwargs):
        rack_id = request.GET.get('rack_id')
        if rack_id is None:
            raise Http404

        position_obj = TPosition.objects.filter(rack_id=rack_id).exclude(delete_status=db_code_mapping['delete'])
        self.context['position_obj'] = position_obj
        self.context['username'] = request.session['username']
        return render(request, 'position_index.html', self.context)
