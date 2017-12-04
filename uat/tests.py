
import psutil, os, socket
import netifaces as ni
import json, time
from pymongo import MongoClient
from bson.objectid import ObjectId

os.environ.setdefault('MONGODB_HOST','192.168.151.14' )

# MONGODB_MONGODB_SERVICE_HOST
#MONGODB_MONGODB_SERVICE_PORT
class SysInfo(object):

        def __init__(self):
                self.hostname = socket.gethostname()
                self.iface = ni.interfaces()[1]
                self.ipaddr = ni.ifaddresses(self.iface)[2][0]['addr']
                self.mem = psutil.virtual_memory()
                self.cpu_logical = psutil.cpu_count()
                self.cpu = psutil.cpu_count(logical=True)
                self.cpu_time = psutil.cpu_times()
                self.cpu_stats = psutil.cpu_stats()
                self.disk = psutil.disk_usage('/')
                self.users = psutil.users()

        def show_mem(self):
                showMem = {}
                showMem['total_mem'] = round(self.mem.total/(1024*1024*1024),2)
                showMem['used_mem'] = round(self.mem.used/(1024*1024*1024),2)
                showMem['free_mem'] = round(self.mem.free/(1024*1024*1024),2)
                # print(showMem)
                return showMem

        def show_cpu(self):
                showCPU = {}
                showCPU['cpu_phy_num'] = self.cpu
                showCPU['cpu_log_num'] = self.cpu_logical
                # print(showCPU)
                return showCPU

        def show_cpu_time(self):
                showCpuTime = {}
                showCpuTime['cpu_user_time'] = self.cpu_time.user
                showCpuTime['system_time'] = self.cpu_time.system
                showCpuTime['idle_time'] = self.cpu_time.idle
                showCpuTime['interrupt_time'] = self.cpu_stats.interrupts
                # print(showCpuTime)
                return showCpuTime

        # def show_disk(self):
        #         disk_list = []
        #         for disk in self.disk:
        #                 disk_dict = {}
        #                 try:
        #                         disk_info = psutil.disk_usage(disk.mountpoint)
        #                         disk_dict[ disk.mountpoint ] = {
        #                                 'Total': ( round(disk_info.total / (1024 * 1024 * 1024 ),2 )),
        #                                 'Used': ( round(disk_info.used / (1024 * 1024 * 1024 ),2 )),
        #                                 'Free': ( round(disk_info.free / (1024 * 1024 * 1024 ),2 )),
        #                                 'Percent': disk_info.percent
        #                         }
        #                         disk_list.append(disk_dict)
        #
        #                 except FileNotFoundError as msg:
        #                         # print(msg)
        #                         pass
        #         # print (disk_list)
        #         return disk_list


        def show_disk(self):
            showDisk = {}
            try:
                showDisk['total_space'] = round(self.disk.total / ( 1024 * 1024 * 1024),2 )
                showDisk['used_space'] = round(self.disk.used / ( 1024 * 1024 * 1024),2 )
                showDisk['free_space'] = round(self.disk.free / (1024 * 1024 * 1024), 2)
                showDisk['used_percent'] = self.disk.percent
            except FileNotFoundError as msg:
                pass

            return showDisk


        def show_user(self):
                user_list = []
                users = self.users

                for user in users:
                        user_dict = {}
                        user_dict['login_user'] = user.name
                        user_dict['login_host'] = user.host
                        user_list.append(user_dict)
                # print(user_list)
                return user_list[0]



def generate_metrics_list(**kwargs):
    import pprint
    client = MongoClient(os.environ['MONGODB_HOST'],27017)
    db = client.metrics
    col = db.host_metrics
    # col.insert(kwargs)
    # pprint.pprint(col.find_one({"_id": ObjectId("598ad6b9ea31eb42767f1620")}))
    # pprint.pprint(col.find_one())
    col.update_one({ '_id': ObjectId(getObjectID(node_name=kwargs['HostMetrics']['Hostname'], node_ip=kwargs['HostMetrics']['IPAddr']))}, { "$set": { 'HostMetrics': kwargs['HostMetrics'] }} , upsert=True )

    client.close()
    # with open('metric.json', 'w') as m1:
    #     m1.write(json.dumps(kwargs['metrics']))


def getObjectID(**kwargs):
    import time
    client = MongoClient(os.environ['MONGODB_HOST'], 27017)
    db = client.nodes_list
    col = db.nodes_info
    obj = col.find_one({ "Hostname": kwargs['node_name'] })
    try:

        if obj != None:
            oid= obj['_id']
            client.close()
            return oid

        else:
            col.insert({'Hostname': kwargs['node_name'], 'IPAddr': kwargs['node_ip'], 'Timestamp': int(time.time()) })
            obj = col.find_one({ "Hostname": kwargs['node_name'] })
            client.close()
            return obj['_id']

    except TypeError as terr:
        print("Error: {0}".format(terr))

        return False


if __name__ == "__main__":
    sysInfo = SysInfo()

    metrics_obj = {'HostMetrics': { 'Hostname': sysInfo.hostname, 'NIC': sysInfo.iface,
                                   'IPAddr': sysInfo.ipaddr, 'Memory': sysInfo.show_mem(),
                                   'CPU': sysInfo.show_cpu(), 'CPU_Time': sysInfo.show_cpu_time(),
                                   'Disk': sysInfo.show_disk(), 'Users': sysInfo.show_user(),
                                   'Timestamp': int(time.time()),
                                }
                   }
    generate_metrics_list(**metrics_obj)


