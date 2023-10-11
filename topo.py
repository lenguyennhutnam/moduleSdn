from mininet.net import Containernet
from mininet.node import Controller, Ryu
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
setLogLevel('info')

net = Containernet(controller=Controller)

info('*** Adding controller\n')
c0 = net.addController('c0', controller=Ryu)
c1 = net.addController('c1')

info('*** Adding host\n')
h1 = net.addDocker('h1', ip='192.168.1.1', dimage='ubuntu:trusty')
h2 = net.addDocker('h2', ip='192.168.1.2', dimage='ubuntu:trusty')
h3 = net.addDocker('h3', ip='192.168.1.3', dimage='ubuntu:trusty')
h4 = net.addDocker('h4', ip='192.168.1.4', dimage='ubuntu:trusty')

info('*** Adding switches\n')
s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')

info('*** Creating links\n')
s1 = net.addLink('s1', 'h1', port1=3, port2=0)
s1 = net.addLink('s1', 'h2', port1=2, port2=0)
s2 = net.addLink('s2', 'h3', port1=1, port2=0)
s2 = net.addLink('s2', 'h4', port1=2, port2=0)
s1 = net.addLink('s1', 's2', cls=TCLink)

info('*** Starting network\n')
net.build()

info('*** Starting controllers\n')
for controller in net.controllers:
    controller.start()

info('*** Starting switches\n')

net.get('s1').start([c0])

net.get('s2').start([c1])

info('*** Running CLI\n')
CLI(net)

info('*** Stopping network\n')
net.stop()
