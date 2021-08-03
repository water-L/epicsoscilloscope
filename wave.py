import threading
import numpy as np
import time
from epics import PV
from pcaspy import Driver, SimpleServer

prefix = "KEYSIGHT:"
LENGTH = 25000

pvdb = {
    'Run': { 'type' : 'enum','enums': ['STOP', 'RUN'],'asyn':True},
    'Xdata':{'type':'float','count':LENGTH,'prec':6,'unit':'mus'},
    'Ydata':{'type':'float','count':LENGTH,'prec':6,'unit':'V'},
}

class myDriver(Driver):
    def __init__(self):
        Driver.__init__(self)
        self.signal = PV('KEYSIGHT:Getwave')
        self.Xorigin = PV('KEYSIGHT:Xorigin')
        self.Yorigin = PV('KEYSIGHT:Yorigin')
        self.Xincrement = PV('KEYSIGHT:Xincrement')
        self.Yincrement = PV('KEYSIGHT:Yincrement')
        self.Timebase = PV('KEYSIGHT:Timebase')
        self.Wave = PV('KEYSIGHT:Wavedata')
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
        while True:
            self.signal.put(1)
            xor = self.Xorigin.get()
            yor = self.Yorigin.get()
            xin = self.Xincrement.get()
            yin = self.Yincrement.get()
            tim = self.Timebase.get()
            wav = self.Wave.get()

            xdata = (np.array(range(LENGTH))*xin+xor+tim)*1.0E6
            ydata = wav*yin+yor

            self.setParam('Xdata',xdata)
            self.setParam('Ydata',ydata)
            self.updatePVs()

            time.sleep(0.5)

if __name__ == '__main__':
    server = SimpleServer()
    server.createPV(prefix, pvdb)
    driver = myDriver()

    while True:
        server.process(0.1)

