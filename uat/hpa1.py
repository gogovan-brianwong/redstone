from __future__ import print_function
import time, os
import kubernetes.client
from kubernetes.client.rest import ApiException
from pprint import pprint

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
kubernetes.config.load_kube_config(os.path.join(BASE_DIR, 'assets/certs', 'kubeconfig-dev.yaml'))

api_instance = kubernetes.client.AppsV1beta1Api()
name = 'redis-redis' # str | name of the Deployment
namespace = 'kube-system' # str | object name and auth scope, such as for teams and projects
pretty = 'true' # str | If 'true', then the output is pretty printed. (optional)
exact = 'true' # bool | Should the export be exact.  Exact export maintains cluster-specific fields like 'Namespace'. (optional)
export = 'true' # bool | Should this value be exported.  Export strips fields that a user can not specify. (optional)

try:
    api_response = api_instance.read_namespaced_deployment(name, namespace, pretty=pretty, exact=exact, export=export)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AppsV1beta1Api->read_namespaced_deployment: %s\n" % e)



