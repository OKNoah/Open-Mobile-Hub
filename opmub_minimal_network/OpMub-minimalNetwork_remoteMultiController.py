#!/usr/bin/python

"""
OpMub-minimalNetwork_remoteController.py 
Open Mobile Hub

Create a minimal network of 1 remote controller, NS switches and NH hosts per switch.
The POX controller must be launched in another xterm :
> sudo python ./pox.py log.level --DEBUG hub
OR
> sudo python ./pox.py log.level --DEBUG l2_learning

Created by Barbara Collignon on Sept 9, 2013
Copyright (c) 2013 Beckersweet. All rights reserved.
"""

from mininet.link import TCLink
from mininet.node import CPULimitedHost
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

Switch = OVSKernelSwitch

def addHost( net, N ):
    "Add host hN to net"
    name = 'h%d' % N
    ip = '10.0.0.%d' % N
    # cpu = desired overall system CPU fraction
    cpu = 0.5/N
    # cores = (real) core(s) this host can run on
    core = 1 
    return net.addHost( name, ip=ip, cpu=cpu , core = core )

def addController(net,N, gateID): 
    "Add controller cN to net"
    name = 'c%d' % N
    ip = '127.0.0.%d' % N 
    return net.addController(name,ip=ip,port=gateID)

def addSwitch(net,N):
    "Add switch sN to net"
    name = 's%d' % N
    return net.addSwitch(name)

def multiSwitchNet(NS,NH):
    "Add 1 remote controller, NS switches & NH hosts per switch"
    port = 6633
    net = Mininet(controller=RemoteController, switch=Switch, host=CPULimitedHost, link=TCLink, build=False)

    k=3;
   
    #remote = addController(net,1,port) 
 
    lastSwitch = None 
    for i in range(1,NS+1) :
        # Add 1 remote controller per switch
        remote = addController(net,i,port)
        s = addSwitch(net,N=i)
        #net.addLink(s,remote)
        host = [addHost(net,n) for n in k,k+NH-1]
        for h in host :
            net.addLink(h,s,bw=10,delay='5ms',loss=1,max_queue_size=1000,use_htb=True)
        if lastSwitch :
            net.addLink(s,lastSwitch,bw=10,delay='5ms',loss=1,max_queue_size=1000,use_htb=True)
        lastSwitch = s  
        port = port + 1
        k=k+NH
    
    print "Starting network"
    net.start()

    print "Testing network"
    net.pingAll()

    print "Running CLI"
    CLI( net )

    print "Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )  # for CLI output
    multiSwitchNet(NS=5,NH=5)
