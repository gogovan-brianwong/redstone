import os, time, json
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from markupsafe import Markup
from nodes.views import HostDetailsHandler, HostManageHandler
from Infrastructure.Authentication import APIAuth

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class HostDetailsPorter(View):

    def get(self, request, *args, **kwargs):

        instance = HostDetailsHandler(APIAuth())
        result = instance.fetch_all_by()

        return render(self.request, 'node_status.html', {'content': result['data'] })

    def post(self, request, *args, **kwargs):

        selectedUid = self.args[0]
        selectedHostName = request.POST.get('data')
        instance = HostDetailsHandler(APIAuth)
        result = instance.fetch_one_by(uid=selectedUid, hostname=selectedHostName)

        return HttpResponse(json.dumps(result))

class HostManagePorter(View):

    def get(self, request, *args, **kwargs):
        return render(self.request, 'node_status.html')

    def post(self, request, *args, **kwargs):
        selectedUid = self.args[0]
        selectedHostname = self.request.POST.get('nodename')
        nodeAnnotate_ = json.loads(self.request.POST.get('node_annotations'))
        nodeLabel_ = json.loads(self.request.POST.get('node_labels'))
        nodeSchedulableOption = self.request.POST.get('node_schedulableOption')
        instance = HostManageHandler(APIAuth())
        result = instance.node_update( selectedUid, selectedHostname, nodeAnnotate_, nodeLabel_, nodeSchedulableOption)

        return HttpResponse(json.dumps(result))

def deletehost(request):

    if request.method == 'POST':
        hostname = request.POST.get('hostname')
        hostip = request.POST.get('ipaddr')
        instance = HostManageHandler(APIAuth())
        result = instance.node_remove(hostname, hostip)
        return HttpResponse(json.dumps(result))
    else:
        redirect('/nodes/index/')
