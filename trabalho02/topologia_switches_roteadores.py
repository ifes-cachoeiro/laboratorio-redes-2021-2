#!/usr/bin/python
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi


def topology(remote_controller):
    "Create a network."
    net = Mininet_wifi()

    info("*** Adding stations/hosts\n")

    h1_redeA = net.addHost("h1RedeA", ip="192.0.2.1/24")
    h2_redeA = net.addHost("h2RedeA", ip="192.0.2.2/24")
    
    roteador1 = net.addHost("roteador1", ip="192.0.2.254/24")
    roteador2 = net.addHost("roteador2", ip="10.10.100.2/24")
    roteador3 = net.addHost("roteador3", ip="10.10.102.2/24")
    roteador4 = net.addHost("roteador4", ip="10.10.101.2/24")
    
    info("*** Adding Switches (core)\n")

    switch1 = net.addSwitch("switch1")
    switch2 = net.addSwitch("switch2")

    info("*** Creating links\n")

    net.addLink(h1_redeA, switch1, bw=1000)
    net.addLink(h2_redeA, switch1, bw=1000)
    net.addLink(roteador1, switch1, bw=1000)
    net.addLink(roteador1, roteador2, bw=1000)
    net.addLink(roteador1, roteador3, bw=1000)
    net.addLink(roteador2, roteador4, bw=1000)

    info("*** Starting network\n")
    net.start()
    net.staticArp()

    info("*** Applying switches configurations\n")

    switch1.cmd("ovs-ofctl add-flow {} \"actions=output:NORMAL\"".format(switch1.name))
    switch2.cmd("ovs-ofctl add-flow {} \"actions=output:NORMAL\"".format(switch2.name))

    info("*** Running CLI\n")
    h1_redeA.cmd("ip route add default via 192.0.2.254")
    h2_redeA.cmd("ip route add default via 192.0.2.254")

    roteador1.cmd("ifconfig roteador1-eth1 10.10.100.1/24")
    roteador1.cmd("ifconfig roteador1-eth2 10.10.102.1/24")
    roteador1.cmd("ip route add 198.51.100.0/24 via 10.10.102.2")

    roteador2.cmd("ip route add 192.0.2.0/24 via 10.10.100.1")
    roteador3.cmd("ip route add 192.0.2.0/24 via 10.10.102.1")

    roteador2.cmd("ifconfig roteador2-eth1 10.10.101.1/24")
    roteador2.cmd("ip route add 198.51.100.0/24 via 10.10.101.2")

    roteador4.cmd("ip route add 192.0.2.0/24 via 10.10.101.1")

    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    remote_controller = False
    topology(remote_controller)
