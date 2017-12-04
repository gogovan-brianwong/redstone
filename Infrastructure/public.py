import json, paramiko
from datetime import datetime
from decimal import Decimal
from django.shortcuts import render
from kubernetes import client
from kubernetes.client.rest import ApiException
from Infrastructure.Authentication import APIAuth
import jinja2
import queue
import threading
import contextlib
import time
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor


class JsonCustomSerializer(json.JSONEncoder):

    def default(self, field):

        if isinstance(field, datetime):
            return field.strftime('%Y-%m-%d %H:%M:%S')


        elif isinstance(field, Decimal):
            return str(field)

        else:
            return json.JSONEncoder.default(self,field)

# class J2RenderHandler(object):
#
#     def __init__(self, tpl_path, tpl_file):
#
#         self.Env = jinja2.Environment
#         self.Loader = jinja2.FileSystemLoader
#         self.tpl_path = tpl_path
#         self.tpl_file = tpl_file
#
#     @property
#     def render_to_obj(self):
#         instance = self.Env(loader=jinja2.FileSystemLoader(self.tpl_path))
#         j2_obj = instance.get_template(self.tpl_file)
#         return j2_obj


def check_login(func):
    def wrapper(self, *args, **kwargs):
        uid = self.session.get('username', None)
        isLogin = self.session.get('is_logined', None)
        traceID = self.session.get('traceid', None)
        userrole = self.session.get('group_from', None)
        if uid and isLogin:
            return func(self, *args, **kwargs)
        else:
            return render(self, 'thanks_login.html')

    return wrapper


def getAllNamespaces():
    api_instance = client.CoreV1Api()
    pretty = 'true'
    timeout_seconds = 30
    watch = 'false'
    try:
        api_response = api_instance.list_namespace(pretty=pretty, timeout_seconds=timeout_seconds, watch=watch)
        ns_list = []

        for row in api_response.items:
            ns_dict = {}
            ns_dict['ns_name'] = row.metadata.name
            ns_dict['ns_status'] = row.status.phase
            ns_list.append(ns_dict)
        return ns_list

    except ApiException as e:
        print("Exception occurred")


def getHost():
    master = APIAuth()
    ep = '/api/v1/nodes'
    content = master.connect_get(resourceEndpoint=ep).json()
    hostinfo_list = []
    for i in content['items']:
        hostinfo_dict = {}
        hostinfo_dict['hostname'] = i['metadata']['name']
        hostinfo_dict['hostip'] = i['status']['addresses'][0]['address']
        # hostinfo_dict['allocatable'] = i.status.allocatable
        # models.HostList(hostname=hostinfo_dict['hostname'], hostip=hostinfo_dict['hostip']).save()
        hostinfo_list.append(hostinfo_dict)
    return hostinfo_list

class BooleanHandler:

    def __init__(self, option):
        self.option = option

    def __bool__(self):
        if self.option == 'false':
            return False
        else:
            return True


class ArrayHandler:

    def __init__(self, arry):
        self.array = arry

    @property
    def toDict(self):
        if isinstance(self.array, list):
            _result = {}

            for row in self.array:
                label_dict = {}
                label = row.split('=')
                label_dict[label[0]] = label[1]
                _result.update(label_dict)
            return _result
        else:
            return False

class ResourceBaseHandler:

    def __init__(self, api_instance=None):

        self.api_instance = api_instance
        self.instance = None

    @property
    def get_instance(self):

        if self.instance:
            return self.instance
        else:
            self.instance = self.api_instance
            return self.instance


    def stopKubelet(self, ipaddr, **kwargs):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect((ipaddr), 22, kwargs['user'], kwargs['passwd'])
            console_cmd = "systemctl daemon-reload && systemctl stop kubelet.service.png && systemctl restart docker"
            stdin, stdout, stderr = ssh.exec_command(console_cmd)
            ssh.close()
            return True
        except Exception as e:
            return False


    def getAllRemotePath(self, *args):
        path_list = []
        for eachlist in args[0]:
            for row in eachlist.values():
                for each in row:
                    path_list.append(each['remote_dir'])

        return path_list


    def del_remote_dir(self, ipaddr, *args, **kwargs):

        transport = paramiko.Transport((ipaddr), 22)
        transport.connect(username=kwargs['user'], password=kwargs['passwd'])
        sftp = paramiko.SFTPClient.from_transport(transport)

        for each_remote_path in args[0]:
            try:
                self.rm(sftp, each_remote_path)
            except IOError:
                continue
        # sftp.close()
        return True


    def rm(self, sftp_conn, path):

        import os
        files = sftp_conn.listdir(path)

        for f in files:
            filepath = os.path.join(path, f)
            try:
                sftp_conn.remove(filepath)
            except IOError:
                continue
                # rm(sftp_conn, path)
        sftp_conn.rmdir(path)
        return True


# class ThreadPool():
#
#     StopEvent = object()
#
#     def __init__(self, max_num, max_task_num=None, *args, **kwargs):
#         super(ThreadPool,self).__init__()
#         if max_task_num:
#             self.q = queue.Queue(max_task_num)
#         else:
#             self.q = queue.Queue()
#         self.q2 = queue.Queue()
#         self.max_num = max_num
#         self.cancel = False
#         self.terminal = False
#         self.generate_list = []
#         self.free_list = []
#
#
#     def run(self, func, args, callback=None):
#         """
#         线程池执行一个任务
#         :param func: 任务函数
#         :param args: 任务函数所需参数
#         :param callback: 任务执行失败或成功后执行的回调函数，回调函数有两个参数1、任务函数执行状态；2、任务函数返回值（默认为None，即：不执行回调函数）
#         :return: 如果线程池已经终止，则返回True否则None
#         """
#         if self.cancel:
#             return
#         if len(self.free_list) == 0 and len(self.generate_list) < self.max_num:
#
#             self.generate_thread()
#
#         w = (func, args, callback,)
#         self.q.put(w)
#
#
#     def generate_thread(self):
#         """
#         创建一个线程
#         """
#         t = threading.Thread(target=self.call)
#
#         t.start()
#
#     def call(self):
#         """
#         循环去获取任务函数并执行任务函数
#         """
#
#         current_thread = threading.currentThread()
#         self.generate_list.append(current_thread)
#
#         event = self.q.get()
#         alist = []
#         while event != ThreadPool.StopEvent:
#             func, arguments, callback = event
#             try:
#                 result = func(*arguments)
#                 success = True
#                 alist.append(result)
#             except Exception as e:
#                 success = False
#                 result = None
#
#             if callback is not None:
#                 try:
#
#                     callback(success,result)
#
#
#                 except Exception as e:
#                     pass
#
#             with self.worker_state(self.free_list, current_thread):
#                 if self.terminal:
#                     event = ThreadPool.StopEvent
#                 else:
#                     event = self.q.get()
#         else:
#
#             self.generate_list.remove(current_thread)
#
#         return alist
#
#
#     def close(self):
#         """
#         执行完所有的任务后，所有线程停止
#         """
#         self.cancel = True
#         full_size = len(self.generate_list)
#         while full_size:
#             self.q.put(ThreadPool.StopEvent)
#             full_size -= 1
#
#     def terminate(self):
#         """
#         无论是否还有任务，终止线程
#         """
#         self.terminal = True
#
#         while self.generate_list:
#             self.q.put(ThreadPool.StopEvent)
#
#         self.q.queue.clear()
#
#     @contextlib.contextmanager
#     def worker_state(self, state_list, worker_thread):
#         """
#         上下文
#         """
#         """
#         用于记录线程中正在等待的线程数
#         """
#         state_list.append(worker_thread)
#         try:
#             yield   # run:
#                     # if self.terminal:
#                     #   event = StopEvent
#                     # else:
#                     #   event = self.q.get()
#         finally:
#             state_list.remove(worker_thread)

class TPBaseHandler(ThreadPoolExecutor):

    def __init__(self, max_threads):
        ThreadPoolExecutor.__init__(self)
        self.max_workers = max_threads


    def _to_dict(self, fn, *args):
        alist = args[0][0]
        item_dict = { self.submit(fn, eachitem): eachitem for eachitem in alist }
        return item_dict


    def run_as(self, fn, *args, **kwargs):

        item_list = []
        for item in concurrent.futures.as_completed(self._to_dict(fn, args)):
            try:
                data = item.result()
                item_list.append(data)
            except Exception as e:
                print(e)
        return item_list








