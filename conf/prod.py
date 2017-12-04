import os
from kubernetes import config

class BaseKubeconfig():

    def LoadConfig(self):
        BASE_CONF_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        conf = os.path.join(BASE_CONF_DIR, 'assets/certs/kubeconfig-prod.yaml')
        config.load_kube_config(config_file=conf)



