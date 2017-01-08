from django.shortcuts import render
from django.http import HttpResponse,Http404
from models import *
from django.views.generic import View


class NetDeviceBaseView(View):
    def __init__(self):
        self.context = {}
        self.context['base'] = "admin_bases.html"

class NetDevice(NetDeviceBaseView):

    def get(self, request, *args, **kwargs):
      return render(request, 'netdevice.html', self.context)
