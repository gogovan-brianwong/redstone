namespace = ['default', 'kube-system']
type_list = [
    {'Node': '/api/v1/nodes'},
    {'Namespace': '/api/v1/namespaces'},
    {'Pod': '/api/v1/namespaces/' + namespace[1] + '/pods'},
    {'StorageClasses': '/apis/storage.k8s.io/v1beta1/storageclasses'},
    {'Deployment': '/apis/apps/v1beta1/deployments'},
    {'Statefulset': '/apis/apps/v1beta1/statefulsets'},
    {'Daemonset': '/apis/extensions/v1beta1/daemonsets'},
    {'Ingress': '/apis/extensions/v1beta1/ingresses'},
    {'Service': '/api/v1/services'}
]