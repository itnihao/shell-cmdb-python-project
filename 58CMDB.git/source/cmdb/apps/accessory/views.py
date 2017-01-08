from django.shortcuts import render
from django.http import HttpResponse,Http404
from models import *
from django.views.generic import View

# Create your views here.

class AccessoryBaseView(View):
    def __init__(self):
        self.context = {}
        self.context['base'] = "admin_bases.html"

class Accessory(AccessoryBaseView):

    def get(self, request, *args, **kwargs):
      return render(request, 'accessory.html', self.context)
