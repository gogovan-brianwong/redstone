import requests, os
from kubernetes import client, config
from kubernetes.client.rest import ApiException

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config.load_kube_config(os.path.join(BASE_DIR, '../assets/certs', 'kubeconfig-dev.yaml'))

# url = 'http://192.168.151.15:9090'
url = 'https://k8s-master-elb.allbright.local/api/v1/nodes/k8s-master-2/proxy/metrics'
ca_cert = os.path.join(BASE_DIR, '../assets/certs', 'ca.pem')
client_cert = os.path.join(BASE_DIR, '../assets/certs', 'node-registry.pem')
client_key = os.path.join(BASE_DIR, '../assets/certs', 'node-registry-key.pem')  # ep =


s = requests.get(url, verify=ca_cert, cert=(client_cert, client_key))

print(s.text)
