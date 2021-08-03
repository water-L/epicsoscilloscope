TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = KEYSIGHT
# KEYSIGHT.dbd will be created and installed
DBD += KEYSIGHT.dbd

# KEYSIGHT.dbd will be made up from these files:
KEYSIGHT_DBD += base.dbd
KEYSIGHT_DBD += stream.dbd
KEYSIGHT_DBD += asyn.dbd
KEYSIGHT_DBD += drvVxi11.dbd
#KEYSIGHT_DBD += calc.dbd
# Include dbd files from all support applications:
#KEYSIGHT_DBD += xxx.dbd

# Add all the support libraries needed by this IOC
#KEYSIGHT_LIBS += xxx
KEYSIGHT_LIBS += asyn
KEYSIGHT_LIBS += stream
#kEYSIGHT_LIBS += calc
# KEYSIGHT_registerRecordDeviceDriver.cpp derives from KEYSIGHT.dbd
KEYSIGHT_SRCS += KEYSIGHT_registerRecordDeviceDriver.cpp

# Build the main IOC entry point on workstation OSs.
KEYSIGHT_SRCS_DEFAULT += KEYSIGHTMain.cpp
KEYSIGHT_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
#KEYSIGHT_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
KEYSIGHT_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

