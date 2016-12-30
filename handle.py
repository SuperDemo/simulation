#-*- coding:utf-8 -*-

import select
import socket

import stack
from simulation import Trace

#
class Handle():
	""""""
	def __init__(self):
		self.func = []
		self.kevent = []
		self.currentk = ""

	def memoryparse(self, mem=""):
		"""['<send@plt>']<-['<func>']<-['<A2>']<-['<A3>']<-['<A5>']<-['<__libc_start_main@plt>']"""
		memlist = mem.split('<-')
		funclist = []
		for func in memlist:
			funclist.append(func[3:-3])
		return funclist


	def eventparse(self,example):
		"""<?xml version='1.0' encoding='gb2312' ?>
		<note id='39'>
		<title>ProblemAck</title>
		<message>A3</message></note>"""

		index1 = example.find(r"<message>")
		index2 = example.find(r"</message>")
		if index1 < 0 or index2 < 0:
			print "fail to parse the event message\n"
			return
		else:
			emessage = example[index1+9:index2]
			return emessage


def mileevent():
	currentmem = []
	currentmem = volstack.getdata(10)
	for self.currentk in currentmem:
		print "find milestone %s"%self.currentk



volstack = stack.Stack(10)
kernelstack = stack.Stack(30)

servers = [0, 0]
clients = [0, 0]

for i in range(2):
	servers[i] = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	servers[i].setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	servers[i].bind(('10.108.163.108', 21001 + i))
	servers[i].listen(5)

inputs = servers
outputs = []
count = 0

handle = Handle()

trajectory = Trace()
trajectory.xmlparse("event.xml")
trajectory.setstate("p3")
milestone = ['ACK', 'Fake', 'milestone']
miledict = {'ACK': 'milestone', 'Fake': 'fake'}

scount = 0
while 1:
	rs, ws, es = select.select(inputs,outputs,[],1)
	#print rs
	for r in rs:
		if r is servers[0]:
			print "connection from kernelclient"
			clientsock, clientaddr=r.accept()
			clients[0] = clientsock
			inputs.append(clientsock)
		elif r is servers[1]:
			print "connection from volclient"
			clientsock,clientaddr=r.accept()
			clients[1] = clientsock
			inputs.append(clientsock)
		elif r is clients[0]:
			#print "recv data from kernelclient"
			count = count + 1
			data=r.recv(1024)
			if not data:
				inputs.remove(r)
			else:
				#print data
				kerneldata = handle.eventparse(data)
				#print "event",kerneldata
				kernelstack.push(kerneldata)
				if kerneldata in milestone:
					print "milestone:", kerneldata
					handle.currentk = miledict[kerneldata]
					print "currentk:",handle.currentk
					handle.kevent.append(kerneldata)
					currentmem = []
					if volstack.isempty() is False:
						currentmem = volstack.getdata(10)
					for m in currentmem:
						if handle.currentk in m:
							print "find milestone %s"%kerneldata
							trajectory.trace.append(kerneldata)
							scount = scount + 1
							if len(trajectory.trace)> 50:
								print "轨迹：%s"%scount, trajectory.trace[-40:]
							else:
								print "轨迹：%s"%scount, trajectory.trace

					else:
						print "failed to find"

					#print "轨迹：", trajectory.trace
				else:
					trajectory.transition([kerneldata])
				#print "send data to kernelclient"
				#r.send("pass")
		elif r is clients[1]:
			print "recv data from volclient"
			data = r.recv(1024)
			if not data:
				inputs.remove(r)
			else:
				#print data
				voldata = []
				voldata = handle.memoryparse(data)
				#print voldata
				volstack.push(voldata)
				#print "get vol data:",volstack.getdata(10)
				#print "send data to client2"
				#r.send("you are client2")


"""
milestone = ['ACK']
initqueue = ['A1', 'S', 'A3', 'A2', 'A2', 'A5']
initqueue2 = ['A2', 'S', 'A3', 'A3', 'A2', 'A5']
t = Trace()
print t.xmlparse('event.xml')
print "------------"
t.setstate("p3")
t.transition(initqueue2)
print t.trace
"""