#!/usr/bin/python
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi


def topology(remote_controller):
    "Create a network."
    net = Mininet_wifi()

    info("*** Adding stations/hosts\n")

    h1RA = net.addHost("h1RA", ip="192.0.2.1/24")
    h2RA = net.addHost("h2RA", ip="192.0.2.2/24")
    h1RB = net.addHost("h1RB", ip="203.0.113.1/24")
    h2RB = net.addHost("h2RB", ip="203.0.113.2/24")

    r1 = net.addHost("r1", ip="192.0.2.254/24")
    r2 = net.addHost("r2", ip="10.10.100.2/24")
    r3 = net.addHost("r3", ip="10.10.102.2/24")
    r4 = net.addHost("r4", ip="10.10.103.2/24")
    r5 = net.addHost("r5", ip="10.10.105.2/24")
    r6 = net.addHost("r6", ip="10.10.201.2/24")
    r7 = net.addHost("r7", ip="203.0.113.254/24")

    info("*** Adding Switches (core)\n")

    switch1 = net.addSwitch("switch1")
    switch2 = net.addSwitch("switch2")

    info("*** Creating links\n")

    net.addLink(h1RA, switch1, bw=1000)
    net.addLink(h2RA, switch1, bw=1000)
    net.addLink(r1, switch1, bw=1000)
    net.addLink(r1, r2, bw=1000)
    net.addLink(r1, r3, bw=1000)
    net.addLink(r3, r4, bw=1000)
    net.addLink(r2, r4, bw=1000)
    net.addLink(r4, r5, bw=1000)
    net.addLink(r5, r6, bw=1000)
    
    net.addLink(h1RB, switch2, bw=1000)
    net.addLink(h2RB, switch2, bw=1000)
    net.addLink(r7, switch2, bw=1000)
    net.addLink(r7, r6, bw=1000)

    info("*** Starting network\n")
    net.start()
    net.staticArp()

    info("*** Applying switches configurations\n")

    switch1.cmd("ovs-ofctl add-flow {} \"actions=output:NORMAL\"".format(switch1.name))
    switch2.cmd("ovs-ofctl add-flow {} \"actions=output:NORMAL\"".format(switch2.name))

    h1RA.cmd("ip route add default via 192.0.2.254")
    h2RA.cmd("ip route add default via 192.0.2.254")
    h1RB.cmd("ip route add default via 203.0.113.254")
    h2RB.cmd("ip route add default via 203.0.113.254")

    r1.cmd("ifconfig r1-eth1 10.10.100.1/24")
    r1.cmd("ifconfig r1-eth2 10.10.102.1/24")
    r1.cmd("ip route add 203.0.113.0/24 via 10.10.102.2")

    r2.cmd("ifconfig r2-eth1 10.10.101.1/24")
    r2.cmd("ip route add 203.0.113.0/24 via 10.10.101.2")
    r2.cmd("ip route add 192.0.2.0/24 via 10.10.100.1")

    r3.cmd("ifconfig r3-eth1 10.10.103.1/24")
    r3.cmd("ip route add 203.0.113.0/24 via 10.10.103.2")
    r3.cmd("ip route add 192.0.2.0/24 via 10.10.102.1")

    r4.cmd("ifconfig r4-eth1 10.10.101.2/24")
    r4.cmd("ifconfig r4-eth2 10.10.105.1/24")
    r4.cmd("ip route add 203.0.113.0/24 via 10.10.105.2")
    r4.cmd("ip route add 192.0.2.0/24 via 10.10.101.1")

    r5.cmd("ip route add 192.0.2.0/24 via 10.10.105.1")
    r5.cmd("ifconfig r5-eth1 10.10.201.1/24")
    r5.cmd("ip route add 203.0.113.0/24 via 10.10.201.2")

    r6.cmd("ifconfig r6-eth1 10.10.202.1/24")
    r6.cmd("ip route add 203.0.113.0/24 via 10.10.202.2")
    r6.cmd("ip route add 192.0.2.0/24 via 10.10.201.1")

    r7.cmd("ifconfig r7-eth1 10.10.202.2/24")
    r7.cmd("ip route add 192.0.2.0/24 via 10.10.202.1")

    info("*** Running CLI\n")

    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    remote_controller = False
    topology(remote_controller)