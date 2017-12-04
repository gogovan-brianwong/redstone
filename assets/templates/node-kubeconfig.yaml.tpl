apiVersion: v1
kind: Config
clusters:
- name: local
  cluster:
    certificate-authority: /etc/kubernetes/ssl/{{ cacert }}
    server: {{ masterurl }}
users:
- name: kubelet
  user:
    client-certificate: /etc/kubernetes/ssl/{{ nodecert }}
    client-key: /etc/kubernetes/ssl/{{ nodekey }}
contexts:
- context:
    cluster: local
    user: kubelet
  name: kubelet-cluster.local
current-context: kubelet-cluster.local
