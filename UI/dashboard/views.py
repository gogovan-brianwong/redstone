import logging
import os,random, jinja2
from django.shortcuts import redirect, render, HttpResponse
from django.template.loader import render_to_string
from django.views import View
from Infrastructure.Authentication import APIAuth
from Infrastructure.public import *
from dao import models
from operator import itemgetter
from jinja2 import Environment, BaseLoader

logger = logging.getLogger(__name__)

BASEDIR = os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__)))))


class UserLogin(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('passwd')
        # obj_list = models.UserDetails.objects.all()
        # for item in obj_list:
        if username == 'admin' and password == 'admin':
            request.session['username'] = username
            request.session['is_logined'] = True
            request.session['traceid'] = random.getrandbits(32)
            # request.session['group_from'] = item.group_type.grouptype
            resp = redirect('/common/dashboard/')
            # resp.set_signed_cookie('AAA','Cookieset!', salt='1qaz2wsx')
            return resp

        print('fail')
        error_msg = 'Wrong Login!Try again.'
        return render(request, 'login.html', {'error_message': error_msg })


class UserManagement(View):

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        logined_user = request.POST.get('username')
        if request.session.get('username',None) == logined_user:
            request.session.delete('username')
            return HttpResponse(json.dumps({'status': True }))
        else:
            redirect('/common/dashboard/')


@check_login
def dashboard(request):
    return render(request, 'dashboard.html')




class DashboardChart:

    def __init__(self):
        self.master = APIAuth()

    def get_top_restart_pod(self):

        namespace = 'kube-system'
        endpoint = '/api/v1/namespaces/' + namespace + '/pods'
        repl = self.master.connect_get(resourceEndpoint=endpoint).json()
        item_list = repl['items']
        with TPBaseHandler(max_threads=10) as TP:
            pod_list = TP.run_as(self.pod_action, item_list)
        result = sorted(pod_list, key=itemgetter('pod_restart_num'), reverse=True)
        html_str = render_to_string('dashboard/restart_block.html',{'top_restart_list': result[:10]})
        ret = {'html': html_str }
        return ret


    def pod_action(self, kwarg):

        pod_restart_dict = {}
        status_list = kwarg['status']['containerStatuses']
        pod_restart_dict['pod_restart_num'] = self._collect_restart_num(status_list)  # send list to collect_restart_num function to generate restart count for each pod
        pod_restart_dict['podname'] = kwarg['metadata']['name'].strip()
        pod_restart_dict['pod_located'] = kwarg['spec']['nodeName'].strip()

        if 'hostNetwork' in kwarg['spec'].keys():
            pod_restart_dict['hostnetwork'] = 'Static'
        else:
            pod_restart_dict['hostnetwork'] = 'Dynamic'
        return pod_restart_dict


    def _collect_restart_num(self, num_list):

        if len(num_list) > 1:
            total_num = 0
            for i in num_list:
                total_num += int(i['restartCount'])
            return total_num
        else:
            total_num = int(num_list[0]['restartCount'])
            return total_num


    def list_resources(self):

        from Infrastructure.conf.resource_list import type_list
        with TPBaseHandler(max_threads=10) as TP:
            result = TP.run_as(self.resource_action, type_list)

        html_str = render_to_string('dashboard/resource_list_block.html',{'resource_list': result[0]})
        ret = {'html': html_str}
        return ret

    def resource_action(self, tlist):

        from Infrastructure.conf.resource_list import type_list
        result = []

        for element in type_list:
            for k, v in element.items():
                result_dict = {}
                content = self.master.connect_get(resourceEndpoint=v).json()
                amount = len(content['items'])
                result_dict['resource_type'] = k
                result_dict['resource_num'] = amount
                result.append(result_dict)
        return result



def get_all_ns(request):
    return HttpResponse(json.dumps({'data': getAllNamespaces()}))


# def cal_cpu_metrics():
#
#     from conf.metric_opts import cpu_param
#     heapster_url = "/api/v1/proxy/namespaces/kube-system/services/heapster/api/v1/model"
#     cpu_metrics_list = []
#
#     headers = {'X-Frame-Options': None}
#     # headers = { "Authorization": "Bearer c2Il5dOKae12hz5mT6Gxk7LXYHrW2xwe" }
#     idx = 1
#     metric_type = 'CPU Used'
#     for row in getHost():
#         hostname = row['hostname']
#         hostip = row['hostip']
#         # allocatable = row['allocatable']
#         cpu_metric_dict = {}
#         host_cpu_metric_dict = {
#
#             "cpu_usage_rate": "/nodes/" + hostname + "/metrics/cpu/usage_rate",
#             "cpu_allocatable": "/nodes/" + hostname + "/metrics/cpu/node_allocatable"
#
#         }
#         master = APIAuth()
#         ep1 = heapster_url +  host_cpu_metric_dict['cpu_usage_rate']
#         cpu_usage = master.connect_get(resourceEndpoint=ep1).json()
#         ep2 = heapster_url + host_cpu_metric_dict['cpu_allocatable']
#         cpu_allocatable = master.connect_get(resourceEndpoint=ep2).json()
#         last_cpu_allocatable = int(cpu_allocatable['metrics'][-1]['value'])
#         last_cpu_usage = int((cpu_usage['metrics'][-1]['value']))
#         cpu_percentage = int(round(last_cpu_usage / last_cpu_allocatable, 2) * 100)
#         cpu_metric_dict['cpu_percent'] = cpu_percentage
#         cpu_metric_dict['maxvalue'] = cpu_param['maxValue']
#         cpu_metric_dict['hostip'] = hostip
#         cpu_metric_dict['cpu_usage'] = last_cpu_usage
#         cpu_metric_dict['cpu_allocatable'] = last_cpu_allocatable
#         cpu_metric_dict['hostname'] = hostname
#         cpu_metric_dict['gauge_id'] = 'gauge_' + str(idx)
#         cpu_metric_dict['canvas_id'] = 'canvas_' + str(idx)
#         cpu_metric_dict['metric_type'] = metric_type
#         cpu_metric_dict['host_metric_type'] = 'cpu_metric'
#         idx += 1
#         cpu_metrics_list.append(cpu_metric_dict)
#     print(type(cpu_metrics_list),cpu_metrics_list)
#     return cpu_metrics_list



    #
        #
        # def show_toprestart_pod(request):
        #     if request.method == 'GET':
        #         pass
        #
        #
        # def show_mem_metrics(request):
        #     if request.method == 'GET':
        #         return HttpResponse(json.dumps({'memory_data': cal_memory_metrics()}))
        #     if request.method == 'POST':
        #         pass
        #
        #
        # def show_fs_metrics(request):
        #     if request.method == 'GET':
        #         return HttpResponse(json.dumps({'fs_data': cal_fs_metrics()}))


        # def get_current_ttl_msg(request):
        #     import time
        #     unread_msg_num = ""
        #     if request.method == 'GET':
        #         unread_msg_num = len(models.PodAlert.objects(isViewed=False))
        #
        #     if request.method == 'POST':
        #         pod_name=request.POST.get('podname')
        #         pod_status=request.POST.get('podstatus')
        #         pod_error=request.POST.get('poderror')
        #         is_viewed = False
        #         models.PodAlert(podname=pod_name, podseverity=pod_status, podmessage=pod_error,
        #                         trigger_time=round(time.time()), isViewed=is_viewed).save()
        #
        #         unread_msg_num = len(models.PodAlert.objects(isViewed=False))
        #     return HttpResponse(json.dumps({'current_num': unread_msg_num }))


        # def push_alert(request):
        #
        #     resp = StreamingHttpResponse(streaming_content=(stream_generator()),content_type="text/event-stream")
        #     resp['Cache-Control'] = 'no-cache'
        #     return resp


# class Mapper():
#     __mapper_relation = {}
#
#     @staticmethod
#     def register(cls, value):
#         Mapper.__mapper_relation[cls] = value
#
#     @staticmethod
#     def exist(cls):
#         if cls in Mapper.__mapper_relation:
#             return True
#         return False
#
#     @staticmethod
#     def get_value(cls):
#         return Mapper.__mapper_relation[cls]
#
#
# class ResourceType(type):
#
#     def __call__(cls, *args, **kwargs):
#         obj = cls.__new__(cls, *args, **kwargs)
#         arg_list = list(args)
#         if Mapper.exist(cls):
#             value = Mapper.get_value(cls)
#             arg_list.append(value)
#         obj.__init__(*args, **kwargs)
#
#         return obj
#
#
# def broker():
#
#
#     while True:
#         chart = DashboardChart()
#         Group(const.GROUP_NAME).send({"text": json.dumps(
#             {'data1': chart.get_top_restart_pod(), 'data2': chart.list_resources()}, cls=JsonCustomSerializer)})
#         time.sleep(5)