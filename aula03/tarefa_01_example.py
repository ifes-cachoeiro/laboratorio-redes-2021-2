#!/usr/bin/python
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi


def topology(remote_controller):
    "Create a network."
    net = Mininet_wifi()

    info("*** Adding datacenter\n")

    server1 = net.addHost("server1", ip="10.0.1.10", mac="00:00:00:00:01:01")
    server2 = net.addHost("server2", ip="10.0.1.11", mac="00:00:00:00:01:02")
    switchDC1 = net.addSwitch("switchDC1")
    switchDC1.cmd(
        'ovs-ofctl add-flow {} "actions=output:NORMAL"'.format(switchDC1.name)
    )

    info("*** Adding switches de nucleo\n")

    switchAG1 = net.addSwitch("switchAG1")
    switchAG1.cmd(
        'ovs-ofctl add-flow {} "actions=output:NORMAL"'.format(switchAG1.name)
    )

    info("*** Adding stations/AP/switches BLOCO 1\n")

    staBL101 = net.addStation(
        "staBL101",
        ip="10.0.1.111",
        mac="00:00:00:00:02:21",
        position="120,90,0",
    )
    staBL102 = net.addStation(
        "staBL102",
        ip="10.0.1.112",
        mac="00:00:00:00:02:21",
        position="60,60,0",
    )
    apBL101 = net.addAccessPoint(
        "apBL101",
        failMode="standalone",
        mac="00:00:00:00:00:10",
        ssid="BLOCO1",
        mode="g",
        channel="1",
        position="110,90,0",
    )
    apBL102 = net.addAccessPoint(
        "apBL102",
        failMode="standalone",
        mac="00:00:00:00:00:11",
        ssid="BLOCO1",
        mode="g",
        channel="11",
        position="50,50,0",
    )

    switchBL1 = net.addSwitch("switchBL1")
    switchBL1.cmd(
        'ovs-ofctl add-flow {} "actions=output:NORMAL"'.format(switchAG1.name)
    )

    info("*** Configuring propagation model\n")
    net.setPropagationModel(model="logDistance", exp=4)

    info("*** Configuring WiFi Nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")

    info("**** Creating links DC\n")
    net.addLink(server1, switchDC1, bw=1000)
    net.addLink(server2, switchDC1, bw=1000)

    info("**** Creating links DC-AG\n")
    net.addLink(switchDC1, switchAG1, bw=1000)

    info("**** Creating links AG-BLOCOS\n")
    net.addLink(switchAG1, switchBL1, bw=1000)

    info("**** Creating links BLOCO 1\n")
    net.addLink(apBL101, switchBL1, bw=100)
    net.addLink(apBL102, switchBL1, bw=100)
    net.addLink(staBL101, apBL101)
    net.addLink(staBL102, apBL102)

    info("*** Starting network\n")
    net.plotGraph(max_x=500, max_y=500)
    net.start()
    net.staticArp()

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    remote_controller = False
    topology(remote_controller)
