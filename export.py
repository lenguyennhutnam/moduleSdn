import os


class Host:
    def __init__(self, name, ip, dimage='ubuntu:trusty'):
        self.name = name
        self.ip = ip
        self.dimage = dimage


class Switch:
    def __init__(self, name, cls=None):
        self.name = name
        self.cls = cls


class Link:
    def __init__(self, node1, node2,
                 port1=None, port2=None, cls=None):
        self.node1 = node1
        self.node2 = node2
        self.port1 = port1
        self.port2 = port2
        self.cls = cls


class Controller:
    def __init__(self, name, controller=None):
        self.switches = []
        self.name = name
        self.controller = controller


class Topo:
    def __init__(self):
        self.controllers = []
        self.hosts = []
        self.switches = []
        self.links = []

    # create new node to topology
    def addController(self, name, controller=None):
        newController = Controller(name, controller)
        self.controllers.append(newController)
        return newController

    def addHost(self, name, ip, dimage='ubuntu:trusty'):
        newHost = Host(name, ip, dimage)
        self.hosts.append(newHost)
        return newHost

    def addSwitch(self, name, cls=None):
        newSwitch = Switch(name, cls)
        self.switches.append(newSwitch)
        return newSwitch

    def addLink(self, node1, node2, port1=None, port2=None, cls=None):
        newLink = Link(node1, node2, port1, port2, cls)
        self.links.append(newLink)
        return newLink

    # create python script for each node
    def addCtrlerScript(self, c):
        script = f"{c.name} = net.addController('{c.name}'"\
            f"{'' if c.controller is None else ', controller=' + c.controller})\n"
        return script

    def addHostScript(self, host):
        script = f"{host.name} = net.addDocker('{host.name}', "\
            f"ip='{host.ip}', dimage='{host.dimage}')\n"
        return script

    def addSwitchScript(self, switch):
        script = f"{switch.name} = net.addSwitch('{switch.name}'" \
            f"{'' if switch.cls is None else ', cls=' + switch.cls})\n"
        return script

    def addLinkScript(self, link):
        script = f"{link.node1} = net.addLink('{link.node1}', '{link.node2}'"\
            f"{'' if link.port1 is None else ', port1=' + link.port1}"\
            f"{'' if link.port2 is None else ', port2=' + link.port2}"\
            f"{'' if link.cls is None else ', cls=' + link.cls})\n"
        return script


def exportTopo(topo):
    importMininet = (
        "from mininet.net import Containernet\n"
        "from mininet.node import Controller\n"
        "from mininet.cli import CLI\n"
        "from mininet.link import TCLink\n"
        "from mininet.log import info, setLogLevel\n"
        "setLogLevel('info')\n\n")
    dirpath = os.path.dirname(__file__)
    # default export filename is topo.py
    with open(os.path.join(dirpath, "topo.py"), "w") as f:
        f.write(importMininet)
        f.write("net = Containernet(controller=Controller)\n")
        f.write("\ninfo('*** Adding controller\\n')\n")
        for controller in topo.controllers:
            f.write(topo.addCtrlerScript(controller))
        # f.write("net.addController('c0')\n")

        # add hosts
        f.write("\ninfo('*** Adding host\\n')\n")
        for host in topo.hosts:
            f.write(topo.addHostScript(host))

        # add switches
        f.write("\ninfo('*** Adding switches\\n')\n")
        for switch in topo.switches:
            f.write(topo.addSwitchScript(switch))

        # add links
        f.write("\ninfo('*** Creating links\\n')\n")
        for link in topo.links:
            f.write(topo.addLinkScript(link))
        # f.write("info('*** Testing connectivity\\n')\n")

        # build network
        f.write("\ninfo('*** Starting network\\n')\n")
        f.write("net.build()\n")

        # start controllers
        f.write("\ninfo('*** Starting controllers\\n')\n")
        f.write("for controller in net.controllers:\n"
                "   controller.start()\n")

        # start switches
        f.write("\ninfo('*** Starting switches\\n')\n")

        f.write("\ninfo('*** Running CLI\\n')\n")
        f.write("CLI(net)\n")
        f.write("\ninfo('*** Stopping network\\n')\n")
        f.write("net.stop()\n")


if __name__ == '__main__':
    topo = Topo()
    topo.addController('c0')
    topo.addController('c1')
    
    topo.addHost('h1', '192.168.1.1')
    topo.addHost('h2', '192.168.1.2')
    topo.addHost('h3', '192.168.1.3')
    topo.addHost('h4', '192.168.1.4')

    topo.addSwitch('s1')
    topo.addSwitch('s2')

    topo.addLink('s1', 'h1', '3', '0')
    topo.addLink('s1', 'h2', '2', '0')
    topo.addLink('s2', 'h3', '1', '0')
    topo.addLink('s2', 'h4', '2', '0')
    topo.addLink('s1', 's2', cls='TCLink')
    exportTopo(topo)
