from  __future__ import absolute_import, unicode_literals
# Create your views here.
import json
import os
from kubernetes import client, config
from kubernetes.client.rest import ApiException
# from a2.celery import app
import requests
from django.shortcuts import render, redirect, HttpResponse

from dao import models
# client.configuration.api_key['authorization'] = 'c2Il5dOKae12hz5mT6Gxk7LXYHrW2xwe'
# client.configuration.api_key_prefix['authorization'] = 'Bearer'




BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# MONGODB_HOST = '192.168.151.15'


# def login_auth(req):
#     user_name = req.POST.get('username')
#     pass_word = req.POST.get('passwd')
#
#     obj_list = models.UserDetails.objects.all()
#     for item in obj_list:
#         if item.username == user_name and item.password == pass_word:
#             req.session['username'] = user_name
#             req.session['is_logined'] = True
#             req.session['api_token'] = 'Authorization: Bearer c2Il5dOKae12hz5mT6Gxk7LXYHrW2xwe'
#
#         status_code = 200
#         return status_code
#     else:
#         status_code = 404
#         return status_code


# @app.task(bind=True)
# def get_top_restart_pod():
#     from operator import itemgetter
#
#     BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     master = 'https://k8s-master-elb.allbright.local:443'
#     ca_cert = os.path.join(BASE_DIR, '../certs', 'ca.pem')
#     client_cert = os.path.join(BASE_DIR, '../certs', 'node-registry.pem')
#     client_key = os.path.join(BASE_DIR, '../certs', 'node-registry-key.pem')
#     # headers = { "Authorization: Bearer c2Il5dOKae12hz5mT6Gxk7LXYHrW2xwe" }
#     namespace = 'kube-system'
#     endpoint = '/api/v1/namespaces/' + namespace + '/pods'
#     repl = requests.get(master + endpoint, verify=ca_cert,
#                         cert=(client_cert, client_key))
#     content = repl.json()
#     pod_restart_list = []
#
#     for eachitem in content['items']:
#         pod_restart_dict = {}
#         pod_restart_dict['podname'] = eachitem['metadata']['name'].strip()
#         pod_restart_dict['pod_restart_num'] = collect_restart_num(eachitem['status'][
#                                                                       'containerStatuses'])  # send list to collect_restart_num function to generate restart count for each pod
#         pod_restart_dict['pod_located'] = eachitem['spec']['nodeName'].strip()
#
#         if 'hostNetwork' in eachitem['spec'].keys():
#             pod_restart_dict['hostnetwork'] = 'Static'
#
#         else:
#             pod_restart_dict['hostnetwork'] = 'Dynamic'
#
#         pod_restart_list.append(pod_restart_dict)
#
#     pod_restart_list = sorted(pod_restart_list, key=itemgetter('pod_restart_num'), reverse=True)
#
#     return pod_restart_list[0:10]




# Decorator for user authentication





def collectCPU():
    pass


def cal_cpu_metrics(arg=None):
    from conf.metric_opts import cpu_param
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    master = 'https://k8s-master-elb.allbright.local:443'
    ca_cert = os.path.join(BASE_DIR, '../assets/certs', 'ca.pem')
    client_cert = os.path.join(BASE_DIR, '../assets/certs', 'node-registry.pem')
    client_key = os.path.join(BASE_DIR, '../assets/certs', 'node-registry-key.pem')
    # kubernetes.client.configuration.api_key['authorization'] = 'c2Il5dOKae12hz5mT6Gxk7LXYHrW2xwe'
    # kubernetes.client.configuration.api_key_prefix['authorization'] = 'Bearer'
    heapster_url = "/api/v1/proxy/namespaces/kube-system/services/heapster/api/v1/model"
    cpu_metrics_list = []

    headers = {'X-Frame-Options': None}
    # headers = { "Authorization": "Bearer c2Il5dOKae12hz5mT6Gxk7LXYHrW2xwe" }
    idx = 1
    metric_type = 'CPU Used'
    for row in getHost():
        hostname = row['hostname']
        hostip = row['hostip']
        # allocatable = row['allocatable']
        cpu_metric_dict = {}
        host_cpu_metric_dict = {

            "cpu_usage_rate": "/nodes/" + hostname + "/metrics/cpu/usage_rate",
            "cpu_allocatable": "/nodes/" + hostname + "/metrics/cpu/node_allocatable"

        }
        cpu_usage = requests.get(master + heapster_url + host_cpu_metric_dict['cpu_usage_rate'], headers=headers,
                                 verify=ca_cert,
                                 cert=(client_cert, client_key)).json()
        # cpu_usage = requests.get(master + heapster_url + host_cpu_metric_dict['cpu_usage_rate'], headers=headers).json()
        cpu_allocatable = requests.get(master + heapster_url + host_cpu_metric_dict['cpu_allocatable'],
                                       headers=headers, verify=ca_cert,
                                       cert=(client_cert, client_key)).json()
        # cpu_allocatable = requests.get(master + heapster_url + host_cpu_metric_dict['cpu_allocatable'],headers=headers).json()
        last_cpu_allocatable = int(cpu_allocatable['metrics'][-1]['value'])
        last_cpu_usage = int((cpu_usage['metrics'][-1]['value']))
        cpu_percentage = int(round(last_cpu_usage / last_cpu_allocatable, 2) * 100)
        cpu_metric_dict['cpu_percent'] = cpu_percentage
        cpu_metric_dict['maxvalue'] = cpu_param['maxValue']
        cpu_metric_dict['hostip'] = hostip
        cpu_metric_dict['cpu_usage'] = last_cpu_usage
        cpu_metric_dict['cpu_allocatable'] = last_cpu_allocatable
        cpu_metric_dict['hostname'] = hostname
        cpu_metric_dict['gauge_id'] = 'gauge_' + str(idx)
        cpu_metric_dict['canvas_id'] = 'canvas_' + str(idx)
        cpu_metric_dict['metric_type'] = metric_type
        cpu_metric_dict['host_metric_type'] = 'cpu_metric'
        idx += 1

        cpu_metrics_list.append(cpu_metric_dict)

    return cpu_metrics_list


def cal_memory_metrics(arg=None):
    from conf.metric_opts import cpu_param
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    master = 'https://k8s-master-elb.allbright.local:443'
    ca_cert = os.path.join(BASE_DIR, '../assets/certs', 'ca.pem')
    client_cert = os.path.join(BASE_DIR, '../assets/certs', 'node-registry.pem')
    client_key = os.path.join(BASE_DIR, '../assets/certs', 'node-registry-key.pem')
    heapster_url = "/api/v1/proxy/namespaces/kube-system/services/heapster/api/v1/model"
    mem_metrics_list = []
    idx = 1
    metric_type = 'Memory Used'
    headers = {'X-Frame-Options': None}
    for row in getHost():
        hostname = row['hostname']
        hostip = row['hostip']
        mem_metric_dict = {}
        host_mem_metric_dict = {

            "mem_usage": "/nodes/" + hostname + "/metrics/memory/usage",
            "mem_allocatable": "/nodes/" + hostname + "/metrics/memory/node_allocatable"

        }
        mem_usage_rate = requests.get(master + heapster_url + host_mem_metric_dict['mem_usage'], headers=headers,
                                      verify=ca_cert,
                                      cert=(client_cert, client_key)).json()
        mem_allocatable_rate = requests.get(master + heapster_url + host_mem_metric_dict['mem_allocatable'],
                                            headers=headers, verify=ca_cert,
                                            cert=(client_cert, client_key)).json()
        mur = mem_usage_rate['metrics'][-1]['value']
        mar = mem_allocatable_rate['metrics'][-1]['value']
        result = cal_memory(mur, mar)

        mem_metric_dict['mem_percent'] = result
        mem_metric_dict['mem_allocatable'] = round(mar / 1024 ** 3, 2)
        mem_metric_dict['mem_usage'] = round(mur / 1024 ** 3, 2)
        mem_metric_dict['maxvalue'] = cpu_param['maxValue']
        mem_metric_dict['gauge_id'] = 'mem_gauge_' + str(idx)
        mem_metric_dict['canvas_id'] = 'mem_canvas_' + str(idx)
        mem_metric_dict['hostname'] = hostname
        mem_metric_dict['hostip'] = hostip
        mem_metric_dict['metric_type'] = metric_type
        mem_metric_dict['host_metric_type'] = 'mem_metric'
        idx += 1
        mem_metrics_list.append(mem_metric_dict)  # returned type is List
    return mem_metrics_list


def cal_fs_metrics(arg=None):
    from pymongo import MongoClient
    client = MongoClient('192.168.151.17', 27017)
    db = client.metrics
    col = db.host_metrics
    metric_type = 'Filesystem Used'
    fs_metrics_list = []
    idx = 0
    for row in col.find():
        eachhost = {}
        eachhost['hostname'] = row['HostMetrics']['Hostname']
        eachhost['hostip'] = row['HostMetrics']['IPAddr']
        eachhost['disk_total'] = row['HostMetrics']['Disk']['total_space']
        eachhost['disk_used'] = row['HostMetrics']['Disk']['used_space']
        eachhost['disk_free'] = row['HostMetrics']['Disk']['free_space']
        eachhost['disk_percent'] = row['HostMetrics']['Disk']['used_percent']
        eachhost['gauge_id'] = 'fs_gauge_' + str(idx)
        eachhost['canvas_id'] = 'fs_canvas_' + str(idx)
        eachhost['metric_type'] = metric_type
        eachhost['host_metric_type'] = 'fs_metric'
        fs_metrics_list.append(eachhost)
        idx += 1
    return fs_metrics_list


def collect_restart_num(num_list):
    if len(num_list) > 1:
        total_num = 0
        for i in num_list:
            total_num += int(i['restartCount'])

        return total_num
    else:
        total_num = int(num_list[0]['restartCount'])
        return total_num


def cal_memory(usage, allocate):
    result_usage = usage / 1024 / 1024
    result_allocate = allocate / 1024 / 1024
    cal_result = round((result_usage / result_allocate), 2) * 100

    return cal_result


def getHost():
    master = 'https://k8s-master-elb.allbright.local:443'
    ca_cert = os.path.join(BASE_DIR, '../assets/certs', 'ca.pem')
    client_cert = os.path.join(BASE_DIR, '../assets/certs', 'node-registry.pem')
    client_key = os.path.join(BASE_DIR, '../assets/certs', 'node-registry-key.pem')
    # headers = { "Authorization": "Bearer c2Il5dOKae12hz5mT6Gxk7LXYHrW2xwe" }
    ep = '/api/v1/nodes'
    content = requests.get(master + ep, verify=ca_cert,
                           cert=(client_cert, client_key)).json()
    hostinfo_list = []
    for i in content['items']:
        hostinfo_dict = {}
        hostinfo_dict['hostname'] = i['metadata']['name']
        hostinfo_dict['hostip'] = i['status']['addresses'][0]['address']
        # hostinfo_dict['allocatable'] = i.status.allocatable
        # models.HostList(hostname=hostinfo_dict['hostname'], hostip=hostinfo_dict['hostip']).save()
        hostinfo_list.append(hostinfo_dict)

    return hostinfo_list


def list_resources():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    master = 'https://k8s-master-elb.allbright.local:443'
    ca_cert = os.path.join(BASE_DIR, '../assets/certs', 'ca.pem')
    client_cert = os.path.join(BASE_DIR, '../assets/certs', 'node-registry.pem')
    client_key = os.path.join(BASE_DIR, '../assets/certs', 'node-registry-key.pem')
    namespace = ['default', 'kube-system']
    type_list = [
        {'Node': '/api/v1/nodes'},
        {'Namespace': '/api/v1/namespaces'},
        {'Pod': '/api/v1/namespaces/' + namespace[1] + '/pods'},
        {'StorageClasses': '/apis/storage.k8s.io/v1beta1/storageclasses'},
        {'Deployment': '/apis/apps/v1beta1/deployments'},
        {'Statefulset': '/apis/apps/v1beta1/statefulsets'},
        {'Daemonset': '/apis/extensions/v1beta1/daemonsets'},
        {'Ingress': '/apis/extensions/v1beta1/ingresses'},
        {'Service': '/api/v1/services'}
    ]
    result = []
    for element in type_list:
        for k, v in element.items():
            result_dict = {}
            content = requests.get(master + v, verify=ca_cert, cert=(client_cert, client_key)).json()
            amount = len(content['items'])

            result_dict['resource_type'] = k
            result_dict['resource_num'] = amount
            result.append(result_dict)

    return result
