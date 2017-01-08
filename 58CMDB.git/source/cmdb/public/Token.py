from functools import wraps
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from public.Exceptions import APIError
from apps.auth.models import TAuth
from datetime import datetime

def token_required(view_func):

    def _wrapped_view(self, *args, **kwargs):
        request = self.request
        token = None
        if request.method == 'GET' and request.GET.has_key('token'):
            token = request.GET.get('token')

        elif request.method == 'POST' and request.POST.has_key('token'):
            token = request.POST.get('token')

        if token:
            obj = TAuth.objects.filter(token=token)[0]
            now = datetime.now()
            if obj and obj.exp_time >= now:
                return view_func(self, *args, **kwargs)
            else:
                raise APIError(-1003)
        else:
            raise APIError(-1003)

    return _wrapped_view
