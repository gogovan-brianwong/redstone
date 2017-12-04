# Create your views here.
import os
import requests
import time

from django.http import StreamingHttpResponse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))




def scan_all_pods():
    master = 'https://k8s-master-elb.allbright.local:443'
    ca_cert = os.path.join(BASE_DIR, '../assets/certs', 'ca.pem')
    client_cert = os.path.join(BASE_DIR, '../assets/certs', 'node-registry.pem')
    client_key = os.path.join(BASE_DIR, '../assets/certs', 'node-registry-key.pem')
    namespace = 'kube-system'
    endpoint = '/api/v1/namespaces/' + namespace + '/pods'
    repl = requests.get(master + endpoint, verify=ca_cert, cert=(client_cert, client_key))
    content = repl.json()
    pod_status_list = []
    for eachpod in content['items']:
        pod_status_dic = {}
        if 'running' in eachpod['status']['containerStatuses'][0]['state'].keys():
            continue
        else:
            pod_status_dic['pod_error'] = eachpod['status']['containerStatuses'][0]['state'].values()
            pod_status_dic['pod_status'] = eachpod['status']['containerStatuses'][0]['ready']
            pod_status_dic['pod_name'] = eachpod['metadata']['name']
            pod_status_list.append(pod_status_dic)
    return pod_status_list


def stream_generator():

    for i in scan_all_pods():

        yield u'data: %s&%s&%s\n\n' % (i['pod_name'], i['pod_status'], i['pod_error'])
        time.sleep(30)







