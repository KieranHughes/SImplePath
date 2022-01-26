from mininet.net import Mininet
from mininet.node import RemoteController
# from mininet.node import OVSController
from mininet.cli import CLI
from mininet.clean import cleanup
from mininet.log import setLogLevel, info
#from rlcode import networkEnvironment
import time
from tensorforce import Agent, Environment
from mininet.net import Mininet
import os
import subprocess
import time
# import iperf3




class Network():
    # net = Mininet( controller=OVSController)
    net = None
    #nodesList = ['h1', 'h2','h3','h4','h5']
    nodesList = ['h1', 'h2','h3']
    def createNet(self):

        self.net = Mininet(controller=RemoteController)
        info('*** Adding controller\n')
        self.net.addController(name='c0', ip='0.0.0.0', port=6633)

        info('*** Adding hosts\n')
        h1 = self.net.addHost('h1', ip='10.0.0.1', mac='00:00:00:00:00:01')  # external attacker

        h2 = self.net.addHost('h2', ip='10.0.1.1', mac='00:00:00:00:00:02')  # Corp network machine A
        h3 = self.net.addHost('h3', ip='10.0.1.2', mac='00:00:00:00:00:03')  # Corp network machine B
        h4 = self.net.addHost('h4', ip='10.0.1.3', mac='00:00:00:00:00:04')  # Engineering Station
        h5 = self.net.addHost('h5', ip='10.0.1.4', mac='00:00:00:00:00:05')  # Engineering Station
    #    h5 = self.net.addHost('h5', ip='10.0.2.2', mac='00:00:00:00:00:05')  # HMI
#
#        h6 = self.net.addHost('h6', ip='10.0.3.1', mac='00:00:00:00:00:06')  # Composition Controller
#        h7 = self.net.addHost('h7', ip='10.0.3.2', mac='00:00:00:00:00:07')  # Flow Controller
#        h8 = self.net.addHost('h8', ip='10.0.3.3', mac='00:00:00:00:00:08')  # Pressure Controller


        info( '*** Adding switches\n' )
        s1 = self.net.addSwitch( 's1' ) # external 'router'
        s2 = self.net.addSwitch( 's2' ) # Corporate bus
#        s3 = self.net.addSwitch( 's3' ) # Control bus
#        s4 = self.net.addSwitch( 's4' ) # CAN bus


        info( '*** Creating links\n' )
        self.net.addLink( h1, s1 )

        self.net.addLink( h2, s2 )
        self.net.addLink( h3, s2 )
        self.net.addLink( h4, s2 )
        self.net.addLink( h5, s2 )
    #    self.net.addLink( h5, s3 )

    #    self.net.addLink( h6, s4 )
    #    self.net.addLink( h7, s4 )
    #    self.net.addLink( h8, s4 )


        info( '*** Linking Corp network to Control Network and Control Network to CAN\n' )
        self.net.addLink( s1, s2 )
    #    self.net.addLink( s2, s3 )
    #    self.net.addLink( s3, s4 )

        #info( '*** Starting network\n')
        #net.start()

        #info( '*** Running CLI\n' )
        # CLI( net )

        #info( '*** Stopping network' )
        #net.stop()
    def disableNodeInterface(self, nodeName, interface):
        node = self.net.getNodeByName(nodeName)
        if self.checkAlive(nodeName) == 'up':
            node.cmd("ifconfig " + interface + " down")
            time.sleep(0.3)

    def enableNodeInterface(self, nodeName, interface):
        node = self.net.getNodeByName(nodeName)
        if self.checkAlive(nodeName) == 'up':
            node.cmd("ifconfig " + interface + " up")
            time.sleep(0.3)



    def shutdown_host(self, nodeName):
        node = self.net.getNodeByName(nodeName)
        node.terminate()
        time.sleep(0.3)


    def startHost(self, nodeName):
        node = self.net.getNodeByName(nodeName)
        node.startShell()
        time.sleep(0.3)

    def startNetwork(self):
        #net = self.net
        self.net.start()
        #CLI( self.net )

    def stopNetwork(self):
    #    time.sleep(3)
        self.net.stop()


    #def startAllHosts(self):
        #for i in self.nodesList:
        #    host = self.net.getNodeByName(i)
        #    host.start()

    def checkAlive(self, nodeName):
        node = self.net.getNodeByName(nodeName)
        try:
            output = node.cmd("pwd")
            if(str(output) == "None"):
                return "down"
            else:
                return "up"
        except:
            print(nodeName + ' down')
            return "down"

    def canReach(self, pingerNodeName, destNodeName):
        failString = "unreachable"
        failString2 = '100%'
        pingerNodeName = self.net.getNodeByName(pingerNodeName)
        destNodeName = self.net.getNodeByName(destNodeName)
        ip = destNodeName.IP
        stringIP = str(ip)
        start = stringIP.find("10.")
        end = start + 8
        destAddr = stringIP[start:end]
        #print(destAddr)
        try:
            output = pingerNodeName.cmd("fping -c1 -t100 " + destAddr)
            #print(str(output))
            if failString in output:
                return False
            elif failString2 in output:
                return False
            else:
                return True
        except:
            return False
