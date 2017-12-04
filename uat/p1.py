import paramiko
#
#
def del_remote_dir(*args, **kwargs):
    auth_user = 'root'
    auth_passwd = 'winner'

    # ssh = paramiko.SSHClient()
    # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ssh.connect(kwargs['ipaddr'], username='brian', password='winner')
    # stdin, stdout, stderr = ssh.exec_command("mkdir -p /etc/{kubernetes/ssl,kubernetes/tokens, kubernetes/manifests, kubernetes, docker/certs.d/registry.allbright.local:5000, systemd/system, flannel/certs} ; mkdir -p /opt/bin")

    t = paramiko.Transport((kwargs['ipaddr']), 22)
    t.connect(username=auth_user, password=auth_passwd)
    sftp = paramiko.SFTPClient.from_transport(t)
    # print(args[0][0], args[0][2])

    # sftp.mkdir('/etc/kubernetes/ssl',mode=755)
    # # sftp.mkdir(args[0][1])
    for each_remote_path in args[0]:
        try:
        # sftp = paramiko.SFTPClient.from_transport(t)
        # mkdir_p(sftp, each_remote_path)
            rm(sftp,each_remote_path)
        except IOError:
            continue
    # sftp.close()
    # print ('closed')
    # # t.close()
    return True

def rm(sftp_conn, path):
    import os
    files = sftp_conn.listdir(path)

    for f in files:
        filepath = os.path.join(path, f)
        try:
            sftp_conn.remove(filepath)
        except IOError:
            continue
    sftp_conn.rmdir(path)




if __name__ == '__main__':
    a1 = [ '/etc/kubernetes/ssl', '/etc/kubernetes/tokens', '/etc/kubernetes/manifests', '/etc/kubernetes', '/opt/bin' ]
    del_remote_dir(a1, ipaddr='192.168.151.18')


# import paramiko, socket
# # paramiko.util.log_to_file('/tmp/paramiko.log')
# # Open a transport
#
# hostip = "192.168.151.18"
# port = 22
# transport = paramiko.Transport(hostip, port)
#
# # Auth
#
# password = "brian"
# username = "winner"
# transport.connect(username=username, password=password)
#
# # Go!
#
# sftp = paramiko.SFTPClient.from_transport(transport)
#
# # Download
#
# filepath = '/etc/passwd'
# localpath = '/home/remotepasswd'
# sftp.get(filepath, localpath)
#
# # Upload
#
# # filepath = '/home/foo.jpg'
# # localpath = '/home/pony.jpg'
# # sftp.put(localpath, filepath)
#
# # Close
#
# sftp.close()
# transport.close()
