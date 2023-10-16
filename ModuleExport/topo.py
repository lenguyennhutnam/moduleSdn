from mininet.net import Containernet
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
setLogLevel('info')

net = Containernet(controller=Controller)

info('*** Adding controller\n')

info('*** Adding host\n')

info('*** Adding switches\n')

info('*** Creating links\n')

info('*** Starting network\n')
net.build()

info('*** Starting controllers\n')
for controller in net.controllers:
    controller.start()

info('*** Starting switches\n')

info('*** Running CLI\n')
CLI(net)

info('*** Stopping network\n')
net.stop()
