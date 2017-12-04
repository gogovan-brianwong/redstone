apiVersion: {{ pod_api_version }}
kind: {{ pod_kind }}
metadata:
  name: {{ pod_name }}
  namespace: {{ pod_namespace }}
spec:
  containers:
  - image: busybox
    command: {{ pod_container_args }}  # [ sleep, "36000" ]
    imagePullPolicy: {{ pod_img_pull_policy }} #IfNotPresent
    name: busybox
  restartPolicy: Always
