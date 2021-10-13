#!/usr/bin/python
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi


def topology(remote_controller):
    "Create a network."
    net = Mininet_wifi()

    info("*** Adding stations/hosts\n")

    h1 = net.addHost("h1", ip="10.0.1.1", mac="00:00:00:00:01:01")
    h2 = net.addHost("h2", ip="10.0.1.2", mac="00:00:00:00:01:02")
    server1 = net.addHost("server1", ip="10.0.1.10", mac="00:00:00:00:01:0a")

    sta01 = net.addStation(
        "sta01",
        ip="10.0.1.21",
        mac="00:00:00:00:02:21",
        position="120,90,0",
    )
    sta02 = net.addStation(
        "sta02",
        ip="10.0.1.22",
        mac="00:00:00:00:02:22",
        position="190,90,0",
    )
    ap01 = net.addAccessPoint(
        "ap01",
        failMode="standalone",
        mac="00:00:00:00:00:10",
        ssid="BLOCO1",
        mode="g",
        channel="10",
        position="85,150,0",
    )
    ap02 = net.addAccessPoint(
        "ap02",
        failMode="standalone",
        mac="00:00:00:00:00:11",
        ssid="BLOCO2",
        mode="g",
        channel="2",
        position="150,150,0",
    )
    info("*** Adding Switches (core)\n")

    switch1 = net.addSwitch("switch1")
    switch2 = net.addSwitch("switch2")

    info("*** Configuring propagation model\n")
    net.setPropagationModel(model="logDistance", exp=4)

    info("*** Configuring WiFi Nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")

    net.addLink(h1, switch1, bw=1000)
    net.addLink(h2, switch1, bw=1000)
    net.addLink(server1, switch1, bw=1000)

    net.addLink(ap01, switch1, bw=1000)
    net.addLink(ap02, switch1, bw=1000)
    net.addLink(sta01, ap01)
    net.addLink(sta02, ap02)

    info("*** Starting network\n")
    net.plotGraph(max_x=250, max_y=200)
    net.start()
    net.staticArp()

    info("*** Applying switches configurations\n")

    switch1.cmd(
        'ovs-ofctl add-flow {} "actions=output:NORMAL"'.format(switch1.name)
    )
    switch2.cmd(
        'ovs-ofctl add-flow {} "actions=output:NORMAL"'.format(switch2.name)
    )

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    remote_controller = False
    topology(remote_controller)
