from __future__ import print_function

from operator import itemgetter

from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from kubernetes import client, config, watch
from django.template import loader
from django.utils.safestring import mark_safe
import kubernetes
# Create your views here.
import requests, os, json, subprocess, paramiko
from jinja2 import Template, Environment, FileSystemLoader
import base64
# from . import models
import json, time
from django.http import StreamingHttpResponse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def generate_config(hostName, hostIP):
    with open(os.path.join(BASE_DIR, 'pkg', 'addhost_config.tpl'), 'r') as tfile:
        data = tfile.read()
    tplfile = Template(data)
    with open(os.path.join(BASE_DIR, 'nodes', 'archive', 'addhost_config.py'), 'w') as outfile:
        outfile.write(tplfile.render(**{'hostname': hostName,
                                        'hostip': hostIP,
                                        'domain': 'allbright.local',
                                        'cacert': os.path.join(BASE_DIR, 'assets', 'certs','ca.pem'),
                                        'cakey': os.path.join(BASE_DIR, 'assets', 'certs', 'ca-key.pem'),
                                        'registry_ca': os.path.join(BASE_DIR, 'assets', 'certs', 'ca.crt'),
                                        'ssl_conf': os.path.join(BASE_DIR, 'nodes', 'archive', 'worker-openssl.conf'),
                                        'tpl_path': os.path.join(BASE_DIR, 'assets', 'templates'),
                                        'conf_archive_path': os.path.join(BASE_DIR, 'nodes', 'archive'),
                                        'cert_archive_path': os.path.join(BASE_DIR, 'assets', 'certs'),
                                        }))

    return True


def addhost(request):
    if request.method == 'POST':
        form_data = request.POST.get('formdata')
        form_label = request.POST.get('formlabel')
        form_schedulable = request.POST.get('formschedulable')
        formdata_list = form_data.split('&')
        formlabel_list = form_label.split('&')
        hostList = proc_addhost_frm(formdata_list)
        labelList = comb_addhost_label_frm(formlabel_list)

        generate_config(hostName=hostList[0]['add_host_name'], hostIP=hostList[1]['add_host_ip'])

        from nodes.archive.addhost_config import general_list, deploy_list

        create_remote_dir(general_list[0]['nodeinfo_list']['hostip'], collect_deploy_list(deploy_list))

        render_files(deploy_list[1]['render_file_list'], local_tpl_path=general_list[2]['local_path_list']['tpl_path'],
                     local_archive_path=general_list[2]['local_path_list']['conf_archive_path'],
                     hostname=hostList[0]['add_host_name'],
                     hostip=hostList[1]['add_host_ip'],
                     host_fqdn=hostList[0]['add_host_name'] + '.allbright.local',
                     masterurl='https://k8s-master-elb.allbright.local:443',
                     cacert=deploy_list[2]['netcopy_list'][0]['files'][0],
                     nodecert=deploy_list[0]['generate_list'][0]['files'][0],
                     nodekey=deploy_list[0]['generate_list'][0]['files'][1],
                     label_content=labelList,
                     sch_opt=form_schedulable[-1]
                     )
        generate_ssl_files(local_cert_path=general_list[2]['local_path_list']['conf_archive_path'],
                           nodecert=deploy_list[0]['generate_list'][0]['files'][0],
                           nodekey=deploy_list[0]['generate_list'][0]['files'][1],
                           hostname=hostList[0]['add_host_name'],
                           domain=general_list[0]['nodeinfo_list']['domain'],
                           cacert=general_list[1]['cert_files']['cacert'],
                           cakey=general_list[1]['cert_files']['cakey'],
                           ssl_conf=general_list[1]['cert_files']['ssl_conf'],
                           digit=2048)

        copy_files_to_remote(collect_copy_list(dlist=deploy_list),
                             hostip=hostList[1]['add_host_ip'],
                             auth_user='root',
                             auth_passwd='winner',
                             local_archive_path=general_list[2]['local_path_list']['conf_archive_path'],
                             mode=644,
                             )

        exec_flannel_script_once(hostip=hostList[1]['add_host_ip'], auth_user='root',
                                 auth_passwd='winner', )
        del_local_cert(hostList[0]['add_host_name'])

        masterurl = 'https://k8s-master-elb.allbright.local:443'
        ca_cert = os.path.join(BASE_DIR, 'assets/certs', 'ca.pem')
        client_cert = os.path.join(BASE_DIR, 'assets/certs', 'node-registry.pem')
        client_key = os.path.join(BASE_DIR, 'assets/certs', 'node-registry-key.pem')
        # headers = "Authorization: Bearer c2Il5dOKae12hz5mT6Gxk7LXYHrW2xwe"
        endpoint = '/api/v1/nodes'

        while True:
            # resp = requests.get(masterurl + endpoint, headers=headers).json()
            resp = requests.get(masterurl + endpoint, verify=ca_cert,
                                cert=(client_cert, client_key)).json()
            for eachnode in resp['items']:
                if eachnode['metadata']['name'] == hostList[0]['add_host_name']:

                    if eachnode['status']['conditions'][-1]['reason'] == 'KubeletReady':
                        # break
                        return HttpResponse(json.dumps({'status': 201}))
                else:
                    time.sleep(2)
                    continue
                    # return HttpResponse(json.dumps({'status': 201}))

def del_local_cert(host):
    import subprocess
    from nodes.archive import addhost_config

    path = addhost_config.general_list[2]['local_path_list']['conf_archive_path']
    os.chdir(path)
    print(path)
    subprocess.call('sudo rm -f ' + host + '*', shell=True)


def render_files(*args, **kwargs):
    xlist = []
    for row in args[0]:  # Construct list for all files that need to be rendered.
        for each in dict(row)['files']:
            xlist.append(each)  # #####
    for eachfile in xlist:
        with open(kwargs['local_tpl_path'] + '/' + eachfile + '.tpl', 'r') as tfile:
            data = tfile.read()
            tempfile = Template(data)
        with open(kwargs['local_archive_path'] + '/' + eachfile, 'w') as outfile:
            outfile.write(tempfile.render(**{'hostname': kwargs['hostname'], 'hostip': kwargs['hostip'],
                                             'host_fqdn': kwargs['host_fqdn'], 'masterurl': kwargs['masterurl'],
                                             'cacert': kwargs['cacert'], 'nodecert': kwargs['nodecert'],
                                             'nodekey': kwargs['nodekey'],
                                             'label_content': kwargs['label_content'],
                                             'sch_opt': str(kwargs['sch_opt'])}))
    return True


def generate_ssl_files(**kwargs):
    import subprocess

    path = kwargs['local_cert_path']
    print(path)
    os.chdir(path)
    # Generate Node keypair
    subprocess.call('openssl genrsa -out ' + kwargs['nodekey'] + ' ' + str(kwargs['digit']), shell=True)
    subprocess.call(
        'openssl req -new -key ' + kwargs['nodekey'] + ' -out ' + kwargs['hostname'] + '.csr' + ' -subj "/CN=' + kwargs[
            'hostname'] + '.' + kwargs['domain'] + '"' + ' -config ' + kwargs['ssl_conf'], shell=True)
    subprocess.call(
        'openssl x509 -req -in ' + kwargs['hostname'] + '.csr' + ' -CA ' + kwargs['cacert'] + ' -CAkey ' + kwargs[
            'cakey'] + ' -CAcreateserial -out ' + kwargs['nodecert'] + ' -days 365 -extensions v3_req -extfile ' +
        kwargs['ssl_conf'], shell=True)
    # return True


def collect_copy_list(dlist):
    path_list = []
    for eachlist in dlist:
        for eachdir in eachlist.keys():
            for y in eachlist[eachdir]:
                path_list.append(y)

    # print ('PathList :%s' % path_list)
    return path_list


def copy_files_to_remote(*args, **kwargs):
    os.chdir(kwargs['local_archive_path'])
    transport = paramiko.Transport((kwargs['hostip']), 22)
    transport.connect(username=kwargs['auth_user'], password=kwargs['auth_passwd'])
    sftp = paramiko.SFTPClient.from_transport(transport)
    for eachpath in args[0]:
        for eachfile in eachpath['files']:
            if 'system:' in eachfile:
                continue
            else:
                sftp.put(eachfile, eachpath['remote_dir'] + '/' + eachfile)
                if eachfile in ['kubelet', 'kube-gen-token.sh', 'mk-docker-opts.sh', 'deploy-script.sh']:
                    sftp.chmod(path=eachpath['remote_dir'] + '/' + eachfile, mode=int(755))
                else:
                    sftp.chmod(path=eachpath['remote_dir'] + '/' + eachfile, mode=int(kwargs['mode']))
    sftp.close()
    transport.close()
    return True


def proc_addhost_frm(arg_list):
    proc_list = []
    for item in arg_list:
        proc_dict = {}
        proc_dict[item.split('=')[0]] = item.split('=')[1]
        proc_list.append(proc_dict)
    return proc_list


def comb_addhost_label_frm(arg_list):
    proc_list = []
    for row in range(0, len(arg_list), 2):
        arg_dict = {}
        arg_dict[arg_list[row][0:14]] = arg_list[row][15:]
        arg_dict[arg_list[row + 1][0:14]] = arg_list[row + 1][15:]
        proc_list.append(arg_dict)
    return proc_list


def collect_deploy_list(dlist):
    path_list = []
    for eachlist in dlist:
        for eachdir in eachlist.keys():
            for y in eachlist[eachdir]:
                if y['remote_dir'] not in path_list:
                    path_list.append(y['remote_dir'])
    return path_list


def create_remote_dir(ipaddr, *args, **kwargs):
    auth_user = 'root'
    auth_passwd = 'winner'
    t = paramiko.Transport((ipaddr), 22)
    t.connect(username=auth_user, password=auth_passwd)
    sftp = paramiko.SFTPClient.from_transport(t)
    for each_remote_path in args[0]:
        mkdir_p(sftp, each_remote_path)

    # sftp.close()
    print('closed')
    # t.close()
    return True


def mkdir_p(sftp, remote_dir):
    dir_path = str()
    for dir_folder in remote_dir.split("/"):
        if dir_folder == "":
            continue
        dir_path += r"/{0}".format(dir_folder)
        try:
            sftp.listdir(dir_path)
        except IOError:
            sftp.mkdir(dir_path)
    return True


def exec_flannel_script_once(**kwargs):
    import time
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(kwargs['hostip'], 22, kwargs['auth_user'], kwargs['auth_passwd'])
    console_cmd = "sh /opt/bin/deploy-script.sh "
    stdin, stdout, stderr = ssh.exec_command(console_cmd)
    ssh.close()
    return True


# def stream_generator():
#     import time
#     return u'data: %s\n\n' % ('XXXX')
#     # time.sleep(5)
#
# def push_notification(request):
#             resp = StreamingHttpResponse(streaming_content=(stream_generator()), content_type="text/event-stream")
#             resp['Cache-Control'] = 'no-cache'
#             return resp




def render_k8s_app():
    pass


def restart_services():
    pass
