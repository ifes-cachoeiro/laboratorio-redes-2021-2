#!/usr/bin/python
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi


def topology(remote_controller):
    "Create a network."
    net = Mininet_wifi()

    info("*** Adding stations/hosts\n")

    h1_redeA = net.addHost("h1RedeA", ip="192.168.1.1/24")
    h2_redeA = net.addHost("h2RedeA", ip="192.168.1.2/24")
    
    roteador1 = net.addHost("roteador1", ip="192.168.1.254/24")
    roteador2 = net.addHost("roteador2", ip="192.168.2.254/24")
    
    h1_redeB = net.addHost("h1RedeB", ip="192.168.20.1/24")
    h2_redeB = net.addHost("h2RedeB", ip="192.168.20.2/24")

    info("*** Adding Switches (core)\n")

    switch1 = net.addSwitch("switch1")
    switch2 = net.addSwitch("switch2")

    info("*** Creating links\n")

    net.addLink(h1_redeA, switch1, bw=1000)
    net.addLink(h2_redeA, switch1, bw=1000)
    
    net.addLink(h1_redeB, switch2, bw=1000)
    net.addLink(h2_redeB, switch2, bw=1000)

    net.addLink(roteador1, switch1, bw=1000)
    net.addLink(roteador1, switch2, bw=1000)
    net.addLink(roteador1, roteador2, bw=1000)
    info("*** Starting network\n")
    net.start()
    net.staticArp()

    info("*** Applying switches configurations\n")

    switch1.cmd("ovs-ofctl add-flow {} \"actions=output:NORMAL\"".format(switch1.name))
    switch2.cmd("ovs-ofctl add-flow {} \"actions=output:NORMAL\"".format(switch2.name))

    roteador1.cmd("ifconfig roteador1-eth1 192.168.20.254/24")
    h1_redeA.cmd("ip route add default via 192.168.1.254")
    h2_redeA.cmd("ip route add default via 192.168.1.254")

    h1_redeB.cmd("ip route add default via 192.168.20.254")
    h2_redeB.cmd("ip route add default via 192.168.20.254")
    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    remote_controller = False
    topology(remote_controller)
