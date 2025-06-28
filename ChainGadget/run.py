#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Switch
from mininet.log import setLogLevel
from mininet.cli import CLI
import os
from time import sleep
import termcolor as T


def log(s, col="green"):
    # Up to python3
    # print T.colored(s, col)
    print(T.colored(s,col))


class Router(Switch):
    ID = 0
    def __init__(self, name, **kwargs):
        kwargs['inNamespace'] = True
        Switch.__init__(self, name, **kwargs)
        Router.ID += 1
        self.switch_id = Router.ID

    def start(self, controllers):
        r = self.name
        log('Setting up %s...' % r)
        self.cmd("sudo sysctl -w net.ipv4.ip_forward=1")
        self.waitOutput()
        sleep(0.1)
        self.cmd("/usr/lib/frr/zebra -f ./conf/%s.conf -d -i /tmp/%s_zebra.pid > ./log/%s_zebra-stdout.log 2>&1" % (r, r, r), shell=True)
        self.waitOutput()
        self.cmd("/usr/lib/frr/ripd -f ./conf/%s.conf -d -i /tmp/%s_ripd.pid > ./log/%s_ripd-stdout.log 2>&1" % (r, r, r), shell=True)
        self.waitOutput()
        self.cmd("/usr/lib/frr/bgpd -f ./conf/%s.conf -d -i /tmp/%s_bgpd.pid > ./log/%s_bgpd-stdout.log 2>&1" % (r, r, r), shell=True)
        self.waitOutput()
        self.cmd("ifconfig lo up")
        self.waitOutput()

    def stop(self):
        self.deleteIntfs()


class MyTopo( Topo ):
    def build(self):
        r1 = self.addSwitch('r1')
        r2 = self.addSwitch('r2')
        b1 = self.addSwitch('b1')
        b2 = self.addSwitch('b2')
        e1 = self.addSwitch('e1')
        e2 = self.addSwitch('e2')

        self.addLink(r1, r2, intfName1="r1--r2", intfName2="r2--r1")
        self.addLink(r2, b2, intfName1="r2--b2", intfName2="b2--r2")
        self.addLink(b1, r1, intfName1="b1--r1", intfName2="r1--b1")
        self.addLink(b1, e1, intfName1="b1--e1", intfName2="e1--b1")
        self.addLink(b2, e2, intfName1="b2--e2", intfName2="e2--b2")



def main():
    os.system("rm -f /tmp/*.log /tmp/*.pid log/*")
    os.system("mn -c >/dev/null 2>&1")
    os.system("killall -9 zebra ripd bgpd > /dev/null 2>&1")
    net = Mininet(topo=MyTopo(), switch=Router, cleanup=True, controller=None)
    net.start()
    CLI(net)
    net.stop()
    os.system("killall -9 zebra ripd")


if __name__ == "__main__":
    main()