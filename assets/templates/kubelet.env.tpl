# logging to stderr means we get it in the systemd journal
KUBE_LOGGING="--logtostderr=true"
KUBE_LOG_LEVEL="--v=2"
# The address for the info server to serve on (set to 0.0.0.0 or "" for all interfaces)
KUBELET_ADDRESS="--address={{ hostip }}"
# The port for the info server to serve on
# KUBELET_PORT="--port=10250"
# You may leave this blank to use the actual hostname
KUBELET_HOSTNAME="--hostname-override={{ hostname }}"
KUBELET_ARGS="--pod-manifest-path=/etc/kubernetes/manifests --pod-infra-container-image=gcr.io/google_containers/pause-amd64:3.0  --node-status-update-frequency=10s  --cluster-dns=10.233.0.3 --cluster-domain=cluster.local --resolv-conf=/etc/resolv.conf --kubeconfig=/etc/kubernetes/node-kubeconfig.yaml --require-kubeconfig \
--register-schedulable={% if sch_opt == "1" %}true{% else %}false{% endif %} \
--node-labels=node-role.kubernetes.io/node=true,{% for eachlabel in label_content %}{{ eachlabel.host_label_key }}={{ eachlabel.host_label_val }},{% endfor %}"
# Should this cluster be allowed to run privileged docker containers
KUBE_ALLOW_PRIV="--allow-privileged=true"
KUBELET_CLOUDPROVIDER=""
