import threading
import vxi11
from pcaspy import Driver, SimpleServer

pvdb = {
    'Acquire' : {
        'type':'enum','enums':['stop','start'],'asyn':True
    },
    'FUNCTION' : {'type':'string','value':'SIN',},
    'FREQUENCY' : {'type':'string','unit':'Hz','value':'10E3',},
    'AMPLITUDE' : {'type':'string','unit' : 'V','value':'1',},
    'OFFSET' : {'type':'string','unit':'V','value':'0',},
    'PHASE' : {'type':'string','unit':'deg','value':'0',},
}


class myDriver(Driver):
    def __init__(self):
        Driver.__init__(self)
        self.tid = None
        self.instr = vxi11.Instrument("192.168.2.2")

    def write(self,reason,value):
        status = True

        if reason == 'Acquire':
            self.setParam(reason,value)
            if self.tid is None and value == 1:
                self.tid = threading.Thread(target=self.getinfo)
                self.tid.start()
        elif reason == 'FUNCTION':
            self.instr.write('SOURce1:FUNCTION %s'%value)
        elif reason == 'FREQUENCY':
            self.instr.write('SOURce1:FREQUENCY %s'%value)
        elif reason == 'AMPLITUDE':
            self.instr.write('SOURce1:VOLTAGE %s'%value)
        elif reason == 'OFFSET':
            self.instr.write('SOURce1:VOLTAGE:OFFSET %s'%value)
        elif reason == 'PHASE':
            self.instr.write('SOURce1:PHASE %s'%value)
        else:
            status = False

        if status:
            self.setParam(reason,value)
        
        self.updatePVs()
        return status

    def getinfo(self):
        func = self.instr.ask('SOURce1:FUNCTION?')
        fre = self.instr.ask('SOURce1:FREQUENCY?')
        amp = self.instr.ask('SOURce1:VOLTAGE?')
        off = self.instr.ask('SOURce1:VOLTAGE:OFFSET?')
        phase = self.instr.ask('SOURce1:PHASE?')

        self.setParam('FUNCTION',func)
        self.setParam('FREQUENCY',fre)
        self.setParam('AMPLITUDE',amp)
        self.setParam('OFFSET',off)
        self.setParam('PHASE',phase)
        self.updatePVs()

        self.setParam('Acquire',0)
        self.callbackPV('Acquire')
        self.updatePVs()
        self.tid = None
    
if __name__ == '__main__':
    prefix = "AFG:"
    instr = vxi11.Instrument("192.168.2.2")
    server = SimpleServer()
    server.createPV(prefix, pvdb)
    driver = myDriver()

    while True:
        server.process(0.1)
