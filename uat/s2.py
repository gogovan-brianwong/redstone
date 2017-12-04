from kubernetes import client, config
from pprint import pprint
from kubernetes.client.rest import ApiException
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config.load_kube_config(os.path.join(BASE_DIR, 'assets/certs', 'kubeconfig-dev.yaml'))

api_instance = client.CoreV1Api()
pretty = 'true'
timeout_seconds = 10
watch = 'false'
try:
    api_response = api_instance.list_namespace(pretty=pretty, timeout_seconds=timeout_seconds, watch=watch)
    pprint(api_response)
except ApiException as e:
    print("Exception occurred")