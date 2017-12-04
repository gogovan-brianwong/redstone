from __future__ import print_function

import os
import re
import string
import time

import jinja2
import kubernetes.client
from django.template.loader import render_to_string
from kubernetes.client.rest import ApiException
from Infrastructure.public import *
from dao.models import AppType, AppName
from Infrastructure.Authentication import APIAuth
from .Config import imagePullPolicy, serviceType, ingressAnnotations, imagePullSecrets
# Create your views here.


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# j2_instance = Environment(loader=jinja2.FileSystemLoader(os.path.join(BASEDIR,'templates','dashboard')),trim_blocks=True)
#         html_str = j2_instance.get_template('restart_block.html').render(top_restart_list=result[:10])

class AppIndexHandler():


    def __init__(self):

        self.AppNameObj = AppName()
        self.AppTypeObj = AppType()

    def fetch_all_apps(self, *args, **kwargs):


            obj = AppName()
            result = obj.fetch_all()
            ret = { 'data': self.constructAppInfo(result), 'apptype': self.constructAppType}

            return ret

    def fetch_specific_apptype(self, *args, **kwargs):
            mimetype = 'application/json'

            obj = AppName()
            result = obj.fetch_apptype(kwargs['select_apptype'])

            html = render_to_string('application/app_repo_list.html',
                                    {'data': self.constructAppInfo(result), 'apptype': self.constructAppType })
            ret = {'html': html}

            return ret

    def constructAppInfo(self,response, input_str=None):
        app_list = []
        for row in response:
            if input_str:
                if self.isAscii(input_str):

                    string = re.findall(input_str, row.appdetails, re.IGNORECASE)
                else:
                    string = re.findall(input_str, row.appdetails, re.LOCALE)

                if len(string) > 0:
                    appinfo = {}
                    appinfo['id'] = row.id
                    appinfo['name'] = row.appname
                    appinfo['details'] = row.appdetails
                    appinfo['typename'] = row.all_apptypes.values('typename')
                    appinfo['thumbnail_path'] = row.thumbnail_path
                    appinfo['version'] = row.app_repository.app_image.all_appversions.all().values('appversion')
                    app_list.append(appinfo)
            else:
                appinfo = {}
                appinfo['id'] = row.id
                appinfo['name'] = row.appname
                appinfo['details'] = row.appdetails
                appinfo['typename'] = row.all_apptypes.values('typename')
                appinfo['thumbnail_path'] = row.thumbnail_path
                appinfo['version'] = row.app_repository.app_image.all_appversions.all().values('appversion')
                app_list.append(appinfo)

        return app_list


    @property
    def constructAppType(self):
        ret = self.AppTypeObj.fetch_all()
        typename_list = [{'typename': x.typename, 'id': x.id } for x in ret ]

        return typename_list


    def isAscii(self, inputString):
        for eachChar in inputString:
            if eachChar not in string.ascii_letters:
                return False
        return True


    def search_app(self,*args, **kwargs):

        resp = self.AppNameObj.fetch_all()
        app_list = self.constructAppInfo(resp, kwargs['input_string'])

        html = render_to_string('application/app_repo_list.html',
                                {'data': app_list, 'apptype': self.constructAppType })
        ret = {'html': html}

        return ret

def check_input_str(func):
    def wrapper(self, *args, **kwargs):
        if kwargs['input_string']:
            string = re.findall(kwargs['input_string'], self.appdetails, re.IGNORECASE)
        else:
            string = re.findall(kwargs['input_string'], self.appdetails, re.LOCALE)
        if len(string) > 0:
            return func(self, *args, **kwargs)

    return wrapper

class AppDetailsHandler():

    response = {'data': '', 'status': 500, 'message': ''}

    def fetch_app_by_one(self,**kwargs):
        appimage_list = []
        obj = AppName()
        ret =obj.fetch_by_id(kwargs['appid'])

        for row in ret:
            appimage = {}
            appimage['image_path'] = row.app_repository.apprepository + '/' + row.app_repository.app_image.imagename
            appimage_list.append(appimage)
        '''
        :return
        {'resources_tab': True, 'id': 2, 'service_tab': True, 'app_name_id': 2, 'policy_tab': True,
         'account_tab': True, 'app_persist_tab': False, 'basic_tab': True, 'db_persist_tab': True}
        '''
        html = render_to_string('application/app_details.html', {'data':  ret, 'app_image': appimage_list, 'service_types': serviceType, 'app_image_pullpolicy': imagePullPolicy,
                                                                 'app_imagepullsecrets': imagePullSecrets }  )
        result = { 'html': html }
        return result

    def fetch_specific_app(self, **kwargs):

        appUID = kwargs['identifier']
        ep = '/apis/apps/v1beta1/deployments'
        obj = APIAuth()
        ret=obj.connect_get(resourceEndpoint=ep).json()
        try:

            for row in ret['items']:
                if appUID == row['metadata']['uid']:
                    return row
                else:
                    continue
        except Exception as e:

            return e

    def fetch_apptype(self):
        # obj = AppName()
        # ret =obj.fetch_all()
        result = AppIndexHandler.constructAppType
        return result

    def deploy_app(self,**kwargs):

        body_deploy_options = {}
            # body_basic = f1.cleaned_data.get('basic_frm')
            # # body_account = f1.cleaned_data['account_frm']
            # # body_app_storage = f1.cleaned_data['app_storage_frm']
            # # body_db_storage = f1.cleaned_data['db_storage_frm']
            # # body_resource = f1.cleaned_data['resource_frm']
            # # body_ingress = f1.cleaned_data['ingress_frm']
            # # body_custom = f1.cleaned_data['custom_frm']
            # # body_custom['select_app'] = request.POST.get('select_appname')
            #
        for itemDict in kwargs['deploy_list']:

            body_deploy_options.update(itemDict)
        obj = AppName()
        current_list = obj.fetch_value_by_id(kwargs['app_id'],['template_path', 'rendered_path', 'helm_repo'])

        with open(BASE_DIR + current_list[0]['template_path'], 'r') as template_f1:

            data = template_f1.read()
            tempfile = jinja2.Template(data)

        with open(BASE_DIR + current_list[0]['rendered_path'], 'w') as output_file:

            output_file.write(tempfile.render(**body_deploy_options))

        resp = AppDetailsHandler.__deployByHelm__(BASE_DIR + current_list[0]['rendered_path'], body_deploy_options['select_app'], body_deploy_options['app_detail_basic_appname'],
                                               current_list[0]['helm_repo'], AppDetailsHandler.__cbfunc__)

        return resp

    def delete_app(self, **kwargs):
        import paramiko
        response = {'data': '', 'message': '', 'status': False}
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('192.168.89.141', 22, 'root', 'winner')
            # chan = ssh.get_transport().open_session()
            console_cmd = "/opt/bin/helm" + " delete " + " --purge " + kwargs['app_name']
            stdin, stdout, stderr = ssh.exec_command(console_cmd)
            print(stdout.channel.recv_exit_status())
            if stdout.channel.recv_exit_status() == 0:
                ssh.close()
                response['status'] = True
            return response

        except Exception as e:
            response['status'] = False
            response['message'] = e
            return response


    @staticmethod
    def __deployByHelm__(release_path, select_app, app_name, helmrepo, callback):
        import paramiko

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('192.168.89.141', 22, 'root', 'winner')
        # chan = ssh.get_transport().open_session()
        del_prev_cmd = "/opt/bin/helm" + " delete " + " --purge " + app_name
        console_cmd = "/opt/bin/helm" + " install " + " -n " + app_name + " -f " + release_path + " " + helmrepo
        print(console_cmd)
        stdin, stdout, stderr = ssh.exec_command(del_prev_cmd)
        stdin, stdout, stderr = ssh.exec_command(console_cmd)
        print(stdout.channel.recv_exit_status())
        if stdout.channel.recv_exit_status() == 0:

            ret = callback(app_name, select_app)
            ssh.close()
            return ret
        else:
            ret = 500
            return ret

    @staticmethod
    def __cbfunc__(appname, selectApp):
        namespace = 'kube-system'
        response = {'status': ''}

        api_ret = AppOptionsHandler()
        ret = api_ret.list_namespaced_deployment(namespace=namespace, app_name=appname, select_app=selectApp)

        return ret



class AppOptionsHandler(kubernetes.client.AppsV1beta1Api, kubernetes.client.StorageV1Api, kubernetes.client.CoreV1Api):

    pretty = 'true'
    timeout_seconds = 56
    watch = 'false'
    response = {'status': 500, 'data': '', 'message': ''}

    def list_namespaced_deployment(self, namespace='kube-system', **kwargs):
        self.field_selector = "metadata.name=" + kwargs['app_name'] + "-" + kwargs['select_app']
        self.label_selector = 'heritage=Tiller'
        self.namespace = namespace

        try:
            api_response = self.list_namespaced_deployment_with_http_info(namespace, **kwargs)

            for row in api_response[0].items:
                for x in row.status.conditions:
                    if x.status == True:
                        break
                    else:
                        time.sleep(1)
                        continue
                self.response['status'] = 200
                return self.response
        except ApiException as e:
                self.response['status'] = 500
                self.response['message'] = e
                return self.response


    @property
    def list_storage_class(self, **kwargs):
        try:
            api_response = self.list_storage_class_with_http_info(**kwargs)
            return [ {'name': x.metadata.name } for x in api_response[0].items ]

        except ApiException as e:
            self.response['status'] = 500
            self.response['message'] =e
            return self.response

    @property
    def list_deployment_for_all_namespaces(self, **kwargs):

        self.label_selector = 'heritage=Tiller'

        api_response = self.list_deployment_for_all_namespaces_with_http_info(label_selector=self.label_selector)
        resources_list = []
        for row in api_response[0].items:
            resource_dict = {}
            resource_dict['name'] = row.metadata.name
            resource_dict['uid'] = row.metadata.uid
            resource_dict['namespace'] = row.metadata.namespace
            resource_dict['replicas'] = row.spec.replicas
            resource_dict['labels'] = row.metadata.labels
            resource_dict['containers'] = row.spec.template.spec.containers
            resource_dict['status'] = row.status.conditions[0].status
            resources_list.append(resource_dict)

        content_str = render_to_string('application/all_deployed_app.html', {'data': resources_list})
        result = {'html': content_str}
        return result


    def list_namespaced_secret(self, namespace, **kwargs):

        self.namespace = namespace
        api_response = self.list_namespaced_secret_with_http_info(namespace=self.namespace)
        data = { 'body': [ { 'name': x.metadata.name } for x in api_response[0].items ], 'ingress_annote': ingressAnnotations }
        return data













