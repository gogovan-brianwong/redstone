#!/bin/sh

# Docker service need to be added "--insecure-registry=registry.allbright.local" prior to login registry
echo '192.168.151.15  registry.allbright.local' >> /etc/hosts

systemctl enable docker && systemctl daemon-reload && systemctl restart docker

docker login registry.allbright.local -u guest -p Allbright1


systemctl enable kubelet.service && systemctl daemon-reload && systemctl restart kubelet.service

sleep 1

/opt/bin/mk-docker-opts.sh -d /run/flannel/flannel_docker_opts.env -i

systemctl restart docker

#docker run --restart=always  -h=`hostname` -d -e SLEEP_TIME=30 -e HOST_IFACE=`ip a |grep en |grep inet |awk -F " " '{print $NF}'` -e HOST_IPV4=`ip a |grep en |grep inet |awk -F " " '{print $2}'|cut -f1 -d'/'` registry.allbright.local:5000/collect_metrics:v3