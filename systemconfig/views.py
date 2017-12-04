from django.shortcuts import render
from django.views import View
# Create your views here.

class SystemInfo(View):

    def get(self, request):
        return render(request,'setting.html')

    def post(self, request, *args, **kwargs):
        pass



class SystemAPIServer(View):

    def get(self, request):

        return render(request, 'setting.html')

    def post(self, request, *args, **kwargs):

        pass