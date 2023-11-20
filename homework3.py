from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, Controller, OVSSwitch
from mininet.cli import CLI
from mininet.link import TCLink, TCIntf
from mininet.log import setLogLevel

class Tree:
	def __init__(self):
	
		self.net = Mininet(controller = RemoteController, link=TCLink)
		self.controller = self.net.addController('c0', controller=RemoteController, ip='10.0.2.15', port=6653)		
		self.depth = 3
		self.fanout = 2
		self.numHosts = 8
		self.numSwitches = 7
		self.Hosts, self.Switches = dict(), dict()

	def create_topology(self):
		# Add Hosts and Switches
		for host in range(1,self.numHosts+1):
			self.Hosts["H" + str(host)] = self.net.addHost("h" + str(host))
		for switch in range(1,self.numSwitches+1):
			self.Switches["S" + str(switch)] = self.net.addSwitch("s" + str(switch), cls=OVSSwitch)

		# Add Links
		## link switches
		for d in range(1, self.depth+1):
			self.net.addLink(
			 self.Switches["S"+str(d)],
			 self.Switches["S"+str((d*2))])
			self.net.addLink(
			 self.Switches["S"+str(d)],
			 self.Switches["S"+str((d*2)+1)])
		## link Hosts
		numConns = abs((self.numHosts/2) - self.numSwitches)
		# Number of hosts to switch connections
		for conn in range(abs(numConns-self.numSwitches), self.numSwitches+1):
			self.net.addLink(
			  self.Switches["S"+str(conn)], 
			  self.Hosts["H"+str((conn*2) - self.numSwitches)])
			self.net.addLink(
			  self.Switches["S" + str(conn)],
			  self.Hosts['H'+str((conn*2)-self.numSwitches+1)])
	def start(self):
		self.net.build()
		self.controller.start()

		for switch in self.Switches:
			self.Switches[switch].start([self.controller])

		self.net.start()
	
	def cli(self):
		CLI(self.net)
	
	def ping(self, sender, receiver, timeout=None):
		send = self.net.get(sender)
		receive = self.net.get(receiver)
		print send, send.IP(), sender, receive, receive.IP(), receiver
		self.net.ping([send, receive],timeout)

	def pingall(self, timeout=None):
		self.net.pingAll(timeout)
	
	def iperf(self, sender, receiver, sec=10):
		send = self.net.get(sender)
		receive = self.net.get(receiver)
		print send, send.IP(), sender, receive, receive.IP(), receiver
		self.net.iperf(hosts=[send, receive], seconds=sec)

	def stop(self):
		self.net.stop()

def run():
	controller = RemoteController('c', '10.0.2.15', 6653)

if __name__ == '__main__':
	setLogLevel('info')
	topo = Tree()
	topo.create_topology()
	topo.start()
	raw_input("Press Enter to start Part1")
	print "pinging h1->h2"
	topo.ping("h1","h2")
	print "pinging h1->h5"
	topo.ping("h1","h5",100)
	raw_input("Press Enter to start Part 2")
	print "pinging h1->h5"
	topo.ping("h1","h5",100)
	topo.iperf("h1","h2")
	topo.iperf("h1", "h5")
	# topo.pingall(3)
	x = raw_input("use CLI? (y/n) [Default N]")
	if x:
		topo.cli()
	else:
		topo.stop()
