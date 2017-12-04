import psutil

class SysInfo(object):

    def __init__(self):
        self.cpu_percent = psutil.cpu_percent(1,False)

    def showcpu(self):
        print (self.cpu_percent)




a = SysInfo()
a.showcpu()
