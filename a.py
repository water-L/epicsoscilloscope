import threading
import numpy as np
from pcaspy import Driver, SimpleServer
import time

prefix = "A:"
LENGTH = 2000
pvdb = {
    'x' : {'type':'float','count':LENGTH,'prec':16},
    'y' : {'type':'float','count':LENGTH,'prec':16},
}

class myDriver(Driver):
    def __init__(self):
        Driver.__init__(self)
        xdata = open('//home//luo-yz//Desktop//datax.dat','r')
        ydata = open('//home//luo-yz//Desktop//datay.dat','r')
        self.x = xdata.read().splitlines()
        self.y = ydata.read().splitlines()
        self.x = np.array(list(map(float,self.x)))
        self.y = np.array(list(map(float,self.y)))
        self.eid = threading.Event()
        self.tid = threading.Thread(target = self.calc)
        self.tid.setDaemon(True)
        self.tid.start()

    def write(self,reason,value):
        status = True
        if reason == 'Run':
            if not self.getParam('Run') and value == 1:
                self.eid.set()
                self.eid.clear()
        if status:
            self.setParam(reason,value)
        return status

    def calc(self):
        i = 0
        while True:
            if i==1000000:
                i = 0
                time.sleep(0.05)
            else:
                Xdata = self.x[i:i+LENGTH]
                Ydata = self.y[i:i+LENGTH]
                self.setParam('x',Xdata)
                self.setParam('y',Ydata)
                self.updatePVs()
                i += LENGTH
                time.sleep(0.05)

if __name__ == '__main__':
    server = SimpleServer()
    server.createPV(prefix, pvdb)
    driver = myDriver()

    while True:
        server.process(0.1)

