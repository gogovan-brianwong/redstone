---
  kind: "Pod"
  apiVersion: "v1"
  metadata:
    name: "flannel"
    namespace: "kube-system"
    labels:
      app: "flannel"
      version: "v0.1"
  spec:
    volumes:
      - name: "subnetenv"
        hostPath:
          path: "/run/flannel"
      - name: "etcd-certs"
        hostPath:
          path: "/etc/flannel/certs"
    containers:
      - name: "flannel-container"
        image: "quay.io/coreos/flannel:v0.6.2"
        imagePullPolicy: IfNotPresent
        resources:
          limits:
            cpu: 300m
            memory: 500M
          requests:
            cpu: 150m
            memory: 64M
        command:
          - "/bin/sh"
          - "-c"
          - "/opt/bin/flanneld -etcd-endpoints https://192.168.151.11:2379,https://192.168.151.12:2379,https://192.168.151.13:2379 -etcd-prefix /cluster.local/network -etcd-cafile /etc/flannel/certs/ca_cert.crt -etcd-certfile /etc/flannel/certs/cert.crt -etcd-keyfile /etc/flannel/certs/key.pem  -public-ip {{ hostip }}"
        ports:
          - hostPort: 10253
            containerPort: 10253
        volumeMounts:
          - name: "subnetenv"
            mountPath: "/run/flannel"
          - name: "etcd-certs"
            mountPath: "/etc/flannel/certs"
            readOnly: true
        securityContext:
          privileged: true
    hostNetwork: true
