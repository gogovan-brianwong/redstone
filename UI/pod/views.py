import os
from django.shortcuts import render, redirect, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from Infrastructure.Authentication import APIAuth

# Create your views here.
from Infrastructure.public import *
from pods.handlers import PodHandler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class PodStatusPorter(View):

    @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super(PodStatusPorter, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        instance = PodHandler(APIAuth())
        ret = instance.fetch_all_by()
        return render(request, 'pods_status.html', { 'content': ret[0], 'current_epoch': ret[1] })

    def post(self, request, *args, **kwargs):

        select_uid = request.POST.get('data')
        instance = PodHandler(APIAuth())
        ret = instance.fetch_one_by_uid(select_uid)

        return HttpResponse(json.dumps(ret))








