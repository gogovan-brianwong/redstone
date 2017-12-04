from kubernetes import client, config
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config.load_kube_config(os.path.join(BASE_DIR, 'assets/certs/kubeconfig-dev.yaml'))

v1 = client.CoreV1Api()

ret = v1.list_node() #Instantiate object from class list_node()

for i in ret.items:   # for-loop to find all key-value
    if i.metadata.name == 'k8s-master-1':
        for j in range(len(i.status.images)):

            a1 = (i.status.images[j].names[1])
            print ((a1.split('/')[-1]).split(':')[::])
        # print ('image:\tversion\n%s\t%s' % ((a1.split('/')[-1].split(':'))[0], (a1.split('/')[-1].split(':'))[1] ))









