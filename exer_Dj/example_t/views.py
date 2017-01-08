from django.views.generic import View
from django.shortcuts import render

class Pool(View):
    def get(self,request):
        # return render(request,'layout.html')
        return render(request,'pool_info.html')

        # return render(request, 'chart.html')

class Index(View):
    def get(self,request):
        return render(request, 'chart.html')
        # return render(request,'model.html')