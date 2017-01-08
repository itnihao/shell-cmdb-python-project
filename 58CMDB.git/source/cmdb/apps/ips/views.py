from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.views.generic import View
from models import *

# Create your views here.

class IpsBaseView(View):
    def __init__(self):
        self.context = {}
        self.context['base'] = "admin_bases.html"

class Ips(IpsBaseView):

    def get(self, request, *args, **kwargs):
        ip_types = TRealIp.objects.values('ip_type').distinct()
        self.context['ip_types'] = ip_types
        self.context['username'] = request.session['username']
        return render(request, 'ips_index.html', self.context)
