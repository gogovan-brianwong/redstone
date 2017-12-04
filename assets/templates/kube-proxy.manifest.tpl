apiVersion: v1
kind: Pod
metadata:
  name: kube-proxy
  namespace: kube-system
  labels:
    k8s-app: kube-proxy
spec:
  hostNetwork: true
  dnsPolicy: ClusterFirst
  containers:
  - name: kube-proxy
    image: registry.allbright.local:5000/hyperkube:v1.7.2
    imagePullPolicy: IfNotPresent
    resources:
      limits:
        cpu: 500m
        memory: 2000M
      requests:
        cpu: 150m
        memory: 64M
    command:
    - /hyperkube
    - proxy
    - --v=2
    - --master={{ masterurl }}
    - --kubeconfig=/etc/kubernetes/node-kubeconfig.yaml
    - --bind-address={{ hostip }}
    - --cluster-cidr=10.233.64.0/18
    - --proxy-mode=iptables
    securityContext:
      privileged: true
    volumeMounts:
    - mountPath: /etc/ssl/certs
      name: ssl-certs-host
      readOnly: true
    - mountPath: /etc/kubernetes/node-kubeconfig.yaml
      name: "kubeconfig"
      readOnly: true
    - mountPath: /etc/kubernetes/ssl
      name: "etc-kube-ssl"
      readOnly: true
    - mountPath: /var/run/dbus
      name: "var-run-dbus"
      readOnly: false
  volumes:
  - name: ssl-certs-host
    hostPath:
      path: /usr/share/ca-certificates
  - name: "kubeconfig"
    hostPath:
      path: "/etc/kubernetes/node-kubeconfig.yaml"
  - name: "etc-kube-ssl"
    hostPath:
      path: "/etc/kubernetes/ssl"
  - name: "var-run-dbus"
    hostPath:
      path: "/var/run/dbus"
