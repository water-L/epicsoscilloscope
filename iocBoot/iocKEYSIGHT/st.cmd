#!../../bin/linux-x86_64/KEYSIGHT

#- You may have to change KEYSIGHT to something else
#- everywhere it appears in this file

< envPaths
epicsEnvSet "STREAM_PROTOCOL_PATH" "$(TOP)/db"
epicsEnvSet "P" "$(P=KEYSIGHT)"
epicsEnvSet "R" "$(R=Test)"

cd "${TOP}"

## Register all support components
dbLoadDatabase "dbd/KEYSIGHT.dbd"
KEYSIGHT_registerRecordDeviceDriver pdbbase

## Load record instances
#dbLoadRecords("db/xxx.db","user=root")
dbLoadRecords("db/KEYSIGHTdata.db","user=root")

vxi11Configure("KEYSIGHT","192.168.2.3",0,0.0,"inst0",0,0)
dbLoadRecords("db/KEYSIGHTdata.db","P=$(P),R=$(R),PORT=KEYSIGHT,A=0") 

cd "${TOP}/iocBoot/${IOC}"
iocInit

## Start any sequence programs
#seq sncxxx,"user=root"
