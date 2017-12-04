from django.shortcuts import render, HttpResponse, redirect
import os, paramiko, json
from nodes.archive import addhost_config
from stat import S_ISDIR

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def deletehost(request):
    if request.method == 'POST':
        hostname = request.POST.get('hostname')
        hostip = request.POST.get('ipaddr')
        auth_user = 'root'
        auth_passwd = 'winner'
        print(hostname, hostip)

        stopKubelet(hostip, user=auth_user, passwd=auth_passwd)
        if del_remote_dir(hostip, getAllRemotePath(addhost_config.deploy_list), user=auth_user,
                          passwd=auth_passwd, hostname=hostname) == True:

            return HttpResponse(json.dumps({'status': 201}))

        else:

            return HttpResponse(json.dumps({'status': 500}))
















