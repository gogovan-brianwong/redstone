from __future__ import print_function
from django.shortcuts import redirect, render, HttpResponse
# Create your views here.
import os

from django.views import View
from markupsafe import Markup
from kubernetes import client
from kubernetes.client.rest import ApiException
from corelogic.common.views import getHost
from Infrastructure.public import *
from nodes.archive import addhost_config
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class HostDetailsHandler(ResourceBaseHandler):

    # _instance = None
    response = {'status': True, 'data': '', 'message': ''}

    def __init__(self, APIHelper):
        super(HostDetailsHandler, self).__init__()
        self.auth_instance = APIHelper
        self.api_instance = client.CoreV1Api()

    def fetch_all_by(self):
        status_list = []
        try:
            ret = self.get_instance.list_node(watch=False)
            content = ret.items
            for i in content:
                status_dict = {}
                status_dict['uid'] = i.metadata.uid
                status_dict['hostname'] = i.metadata.name
                status_dict['ipaddr'] = i.status.addresses[0].address
                status_dict['schedulable'] = i.spec.unschedulable
                status_dict['osimage'] = i.status.node_info.os_image
                status_dict['kernel_ver'] = i.status.node_info.kernel_version
                status_dict['conditions'] = i.status.conditions[3].status
                status_list.append(status_dict)
            HostDetailsHandler.response['data'] = status_list

            return HostDetailsHandler.response

        except Exception as e:
            HostDetailsHandler.response['status'] = False
            HostDetailsHandler.response['message'] = e
            return HostDetailsHandler.response


    def fetch_one_by(self, uid, hostname):
        pretty = 'true'
        export = 'false'
        try:
            api_response = self.get_instance.read_node(hostname, pretty=pretty, export=export)
            node_detail = {}
            node_detail['name'] = api_response.metadata.name
            node_detail['cluster_name'] = api_response.metadata.cluster_name
            node_detail['unique_id'] = api_response.metadata.uid
            node_detail['ip_addr'] = api_response.to_dict()['status']['addresses']  # return List
            node_detail['create_time'] = Markup.unescape(api_response.metadata.creation_timestamp)
            node_detail['unschedulable'] = api_response.spec.unschedulable
            node_detail['taint'] = api_response.spec.taints
            node_detail['pod_cidr'] = api_response.spec.pod_cidr
            node_detail['annotations'] = [k + '=' + v for k, v in
                                          api_response.metadata.annotations.items()]  # return List
            node_detail['labels'] = [k + '=' + v for k, v in api_response.metadata.labels.items()]  # return List
            node_detail['machine_info'] = [{k: v} for k, v in api_response.to_dict()['status']['node_info'].items()]

            HostDetailsHandler.response['data'] = node_detail
            return HostDetailsHandler.response

        except ApiException as e:

            HostDetailsHandler.response['status'] = False
            HostDetailsHandler.response['message'] = e
            return HostDetailsHandler.response


class HostManageHandler(ResourceBaseHandler):

    response = {'status': True, 'message': '', 'data': ''}
    auth_user = 'root'
    auth_passwd = 'winner'

    def __init__(self, APIHelper):
        super(HostManageHandler, self).__init__()
        self.auth_instance = APIHelper
        self.api_instance = client.CoreV1Api()
        self.addhost_config = addhost_config



    def node_update(self, *args, **kwargs):

        uid, hostname, nodeAnnotate, nodeLabel, nodeSchedulableOption = args
        pretty = 'true'  # str | If 'true', then the output is pretty printed. (optional)
        clear_body = { "metadata": { "labels": None, "annotations": None } }
        api_response = self.get_instance.patch_node(name=hostname, body=clear_body, pretty=pretty)
        #
        body = {
            "spec":
                {
                    "unschedulable": bool(BooleanHandler(nodeSchedulableOption))
                },
            "metadata":
                {
                    "labels": ArrayHandler(nodeLabel).toDict,
                    "annotations": ArrayHandler(nodeAnnotate).toDict,
                }
            }
        try:
            api_response = self.get_instance.patch_node(hostname, body=body, pretty=pretty)
            HostManageHandler.response['status'] = True
            return  HostManageHandler.response

        except ApiException as e:
            HostManageHandler.response['status'] = False
            HostManageHandler.response['message'] = e
            return HostManageHandler.response


    def node_remove(self, *args):

        hostname, hostip = args
        # kubernetes.client.configuration.api_key['authorization'] = 'c2Il5dOKae12hz5mT6Gxk7LXYHrW2xwe'
        # kubernetes.client.configuration.api_key_prefix['authorization'] = 'Bearer'

        kubelet_response = self.stopKubelet(hostip, user=HostManageHandler.auth_user, passwd=HostManageHandler.auth_passwd)

        if kubelet_response:
            response = self.del_remote_dir(hostip,self.getAllRemotePath(addhost_config.deploy_list),user=HostManageHandler.auth_user,
                                           passwd=HostManageHandler.auth_passwd, hostname=hostname)
            if response:

                grace_period_sec = 56
                try:
                    api_response = self.get_instance.delete_node(name=hostname, body=client.V1DeleteOptions(), grace_period_seconds=grace_period_sec)
                    HostManageHandler.response['status'] = True
                    return HostManageHandler.response
                except ApiException as e:
                    HostManageHandler.response['status'] = False
                    HostManageHandler.response['message'] = e
                    return HostManageHandler.response



def check_hostname(request):
    if request.method == 'POST':
        host_name = request.POST.get('input_host').strip()
        print(host_name)
        status = 200
        if host_name in [ item['hostname'] for item in getHost()]:
            status = 404
            err_msg = 'The name is duplicated.'
            return HttpResponse(json.dumps({'status': status, 'err_msg': err_msg}))
        else:
            return HttpResponse(json.dumps({'status': status}))


def check_ipaddr(request):
    import subprocess

    if request.method == 'POST':
        ip = request.POST.get('host_ip').strip()
        subnet = request.POST.get('host_subnet').strip()
        cmd = 'ping -c 1 ' + ip
        error = ''
        response_code = subprocess.getstatusoutput(cmd)[0]
        print(response_code)
        if response_code == 0:
            return HttpResponse(json.dumps({'status': 200, 'err_msg': error}))
        else:
            error = 'Unreachable IP Address'
            return HttpResponse(json.dumps({'status': 500, 'err_msg': error}))
