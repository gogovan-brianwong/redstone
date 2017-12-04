# Create your views here.
from Infrastructure.public import *
import time, pprint
import kubernetes
from kubernetes.client.rest import ApiException
# from kubernetes.stream import ws_client

class PodHandler():

    endpoint = '/api/v1/namespaces/kube-system/pods'
    _instance = None

    def __init__(self, APIHelper):
        self.APIHelper = APIHelper

    def get_instance(self):

        if PodHandler._instance:
            return PodHandler._instance
        else:
            PodHandler._instance = self.APIHelper
            return PodHandler._instance

    def fetch_all_by(self):
        import re
        time_elapsed_list = []
        content = self.get_instance().connect_get(PodHandler.endpoint).json()
        content_list = content['items']
        current_epoch = int(time.time())
        status_pod = 'running'
        for row in content_list:
            if status_pod in row['status']['containerStatuses'][0]['state'].keys():

                str_time = re.sub(r'[T,Z]', " ",
                                  (str(row['status']['containerStatuses'][0]['state']['running']['startedAt']))).strip()
                pod_elapsed_time = current_epoch - int(time.mktime(time.strptime(str_time, '%Y-%m-%d %H:%M:%S')))

                minutes = pod_elapsed_time // 60 % 60

                row['status']['containerStatuses'][0]['state']['running']['elapsed_time'] = minutes


            else:
                continue
        return content_list, current_epoch

    def fetch_one_by_uid(self, uid):

        content = self.get_instance().connect_get(PodHandler.endpoint).json()
        for row in content['items']:
            if row['metadata']['uid'] == uid:
                return row


    def open_terminal(self, podname):
        api_instance = kubernetes.client.CoreV1Api()
        name = podname  # str | name of the Pod
        namespace = 'kube-system'  # str | object name and auth scope, such as for teams and projects
        command = 'uptime'  # str | Command is the remote command to execute. argv array. Not executed within a shell. (optional)
        container = 'container_example'  # str | Container in which to execute the command. Defaults to only container if there is only one container in the pod. (optional)
        stderr = True  # bool | Redirect the standard error stream of the pod for this call. Defaults to true. (optional)
        stdin = True # bool | Redirect the standard input stream of the pod for this call. Defaults to false. (optional)
        stdout = True  # bool | Redirect the standard output stream of the pod for this call. Defaults to true. (optional)
        tty = True  # bool | TTY if true indicates that a tty will be allocated for the exec call. Defaults to false. (optional)

        try:
            api_response = api_instance.connect_get_namespaced_pod_exec(name, namespace, command=command,
                                                                        stderr=stderr, stdin=stdin,
                                                                        stdout=stdout, tty=tty,
                                                                        _preload_content=False)
            api_response.run_forever()
            if api_response.peek_stdout(): print("STDOUT: ", api_response.read_stdout())
            if api_response.peek_stderr(): print("STDERR: ", api_response.read_stderr())
            # pprint.pprint(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->connect_get_namespaced_pod_exec: %s\n" % e)
