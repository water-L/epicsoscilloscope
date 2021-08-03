# Epics Oscilloscope

## 平台

任意波形发生器：Tektronix AFG3052C

示波器：KEYSIGHT DSOS054A

电脑操作系统：Ubuntu 20.04

需要安装EPICS和PyDM

## 结构
![](https://github.com/water-L/epicsoscilloscope/blob/main/arc/Picture1.jpg)
![](https://github.com/water-L/epicsoscilloscope/blob/main/arc/Picture2.jpg)

## 介绍

1. 设备通讯：在本系统中，服务器端的IOC和用户端的OPI均存在与我的个人电脑中，通过不同的终端来运行。在与两台设备的通讯过程中，IOC均使用vxi11协议——在PCASpy中，这一协议及相关功能可通过pyvxi11包来获得，在StreamDevice中，与协议相关的功能通过其依赖的asyn模组来提供。

2. 波形发生器IOC：IOC1会从波形发生器上获取波形、频率、峰峰值、偏置和相位五个参数。在运行过程中，IOC1默认处于输出状态，即用户可随时通过改变IOC1中相应PV的值来改变示波器输出波形的各项参数。同时，IOC1中也设置了一个PV，用以实现IOC端与设备的参数同步。对应AFG.py文件。

3. 示波器IOC：IOC2会从示波器上获取波形数据（Waveform data）和相关参数，以及波形的频率、振幅。IOC中波形数据的刷新率为2Hz，在一次传输中IOC会读取25000个数据点的数据，并存储在Waveform类型的record中，而示波器的存储深度则设定为32768pts。

4. 波形数据处理IOC：由于IOC2是使用StreamDevice来搭建的，其本身并不支持对Waveform类型数据的计算，故采用了IOC3这种通过PCASpy来搭建的softIOC，以便使用python强大的数据处理功能来进行相关计算。对应wave.py文件。

5. 使用run文件运行

6. a.py为娱乐向文件，读取datax.dat和datay.dat中的数据播放bad apple。使用此功能可借助forfun.ui文件。
