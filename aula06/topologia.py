#!/usr/bin/python
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
import time
import os

def run_router(router):
    name = router.name
    services = ["zebra", "ripd"]
    for srv in services:
        cmd = f"/usr/sbin/{srv} "
        cmd += f"-f /tmp/quagga/{srv}-{name}.conf -d -A 127.0.0.1 "
        cmd += f"-z /tmp/zebra-{name}.api -i /tmp/{srv}-{name}.pid "
        cmd += f"> /tmp/{srv}-{name}-router.log 2>&1"
        router.cmd(cmd)
        time.sleep(1)
    

def topology(remote_controller):
    "Create a network."
    net = Mininet_wifi()

    info("*** Adding stations/hosts\n")

    h1r1 = net.addHost("h1r1", ip="192.0.2.1/24")
    h2r2 = net.addHost("h2r2", ip="192.0.3.1/24")
    h3r3 = net.addHost("h3r3", ip="192.0.4.1/24")

    r1 = net.addHost("r1", ip="192.0.2.254/24")
    r2 = net.addHost("r2", ip="192.0.3.254/24")
    r3 = net.addHost("r3", ip="10.10.102.2/24")

    info("*** Adding Switches (core)\n")

    switch1 = net.addSwitch("switch1")
    switch2 = net.addSwitch("switch2")
    switch3 = net.addSwitch("switch3")

    info("*** Creating links\n")

    net.addLink(h1r1, switch1, bw=1000)
    net.addLink(r1, switch1, bw=1000)

    net.addLink(h2r2, switch2, bw=1000)
    net.addLink(r2, switch2, bw=1000)

    net.addLink(h3r3, switch3, bw=1000)
    net.addLink(r3, switch3, bw=1000)

    net.addLink(r1, r2, bw=1000)
    net.addLink(r1, r3, bw=1000)
    net.addLink(r2, r3, bw=1000)

    info("*** Starting network\n")
    net.start()
    net.staticArp()

    info("*** Applying switches configurations\n")

    switch1.cmd("ovs-ofctl add-flow {} \"actions=output:NORMAL\"".format(switch1.name))
    switch2.cmd("ovs-ofctl add-flow {} \"actions=output:NORMAL\"".format(switch2.name))
    switch3.cmd("ovs-ofctl add-flow {} \"actions=output:NORMAL\"".format(switch3.name))
    
    h1r1.cmd("ip route add default via 192.0.2.254")
    h2r2.cmd("ip route add default via 192.0.3.254")
    h3r3.cmd("ip route add default via 192.0.4.254")

    r1.cmd("ifconfig r1-eth1 10.10.100.1/24 up")
    r1.cmd("ifconfig r1-eth2 10.10.102.1/24 up")
    r2.cmd("ifconfig r2-eth1 10.10.100.2/24 up")
    r2.cmd("ifconfig r2-eth2 10.10.101.1/24 up")

    r3.cmd("ifconfig r3-eth1 10.10.102.2/24 up")
    r3.cmd("ifconfig r3-eth2 10.10.101.2/24 up")

    run_router(r1)
    run_router(r2)
    run_router(r3)

    info("*** Running CLI\n")

    CLI(net)

    info("*** Stopping network\n")
    net.stop()
    os.system("killall -9 zebra ripd bgpd ospfd > /dev/null 2>&1")


if __name__ == "__main__":
    os.system("rm -f /tmp/zebra-*.pid /tmp/ripd-*.pid /tmp/ospfd-*.pid")
    os.system("rm -f /tmp/bgpd-*.pid /tmp/*-router.log")
    os.system("rm -fr /tmp/zebra-*.api")
    os.system("mn -c >/dev/null 2>&1")
    os.system("killall -9 zebra ripd bgpd ospfd > /dev/null 2>&1")
    os.system("rm -fr /tmp/quagga")
    os.system("cp -rvf conf/ /tmp/quagga")
    os.system("chmod 777 /tmp/quagga -R")
    os.system("echo 'hostname zebra' > /etc/quagga/zebra.conf")
    os.system("chmod 777 /etc/quagga/zebra.conf")
    # os.system("systemctl start zebra.service")

    setLogLevel("info")
    remote_controller = False
    topology(remote_controller)
