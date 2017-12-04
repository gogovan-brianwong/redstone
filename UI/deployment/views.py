import json
from django.shortcuts import render, redirect, HttpResponse
from django.views import View

from Infrastructure.public import *


class DeploymentIndex(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'deployment_index.html')

    def post(self, request, *args, **kwargs):
        pass



class DeploymentDetails(View):

    def get(self, request, *args, **kwargs):

        pass

    def post(selfs, request, *args, **kwargs):

        pass


def index(request):

    return render(request, 'deployment_index.html',{'data': all_deploy_info()})



def adddeploy(request):
    pass


# def find_one(request):
#
#     if request.method == 'POST':
#
#         deploy_name = request.POST.get('name')
#         return HttpResponse(json.dumps({ 'data': findOne(deploy_name) }))
#
#     else:
#         return HttpResponse(json.dumps({'status': 500 }))