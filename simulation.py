#-*- coding:utf-8 -*-

from xml.dom.minidom import parse,parseString #

class Trace:

	def __init__(self):

		self.currentstate = ''
		self.systemmodel = {}
		self.modelgraph = {}
		self.trace = []
		self.win = []

	def xmlparse(self,xmlname):
		"""need to fix"""
		self.systemmodel = {}
		flag = False
		doc = parse(xmlname)
		for node1 in doc.getElementsByTagName('state'):
			state = node1.getAttribute('currentState')
			self.systemmodel[state] = {}
			skipattr = {}

			for node2 in node1.getElementsByTagName('nextskip'):
				event = node2.getAttribute('AVAevent')
				if node2.childNodes:
					skipattr[event] = node2.childNodes[0].data

			self.systemmodel[state] = skipattr

		return self.systemmodel


	"""
	def model2graph(self):
		for m in self.systemmodel:
			self.modelgraph[m] = self.systemmodel[m].values()


	def buildtrace(self,root = None ,EventQueue = []):
		queue = []
		order = []
		visited = {}

		def bfs():
				while len(queue) > 0:
					node = queue.pop(0)
					visited[node] = True

					for m in self.systemmodel[node].keys():
						if m in EventQueue:
							self.trace.append(m)

					if node == "end":
						continue

					for n in self.systemgraph[node]:
						if (not n in visited) and (not n in queue):
							queue.append(n)
							order.append(n)


		try:
			if root:
				queue.append(root)
				order.append(root)
				bfs()
		except Exception,e:
			print "root is None"

		print self.trace
		return self.trace
	"""

	def setstate(self, state=""):
		self.currentstate = state
		return self.currentstate

	def transition(self, eventqueue=[]):

		i = 0
		flag = 0
		nextstate = ""
		state = ""
		event = ""
		oldevent = ""

		state = self.currentstate  #当前状态
		queuelen = len(eventqueue)

		while len(eventqueue) > 0:
			event = eventqueue.pop(0)
			if event not in self.systemmodel[state].keys():
				self.win.append(event)
			else:
				nextstate = self.systemmodel[state][event]
				self.trace.append(event)
				state = nextstate
				#flag = 1

			if len(self.win) > 0:# and flag == 1:  #每次都对窗口的事件进行匹配  ；flag = 1时候，匹配成功则对窗口里事件匹配
				#flag = 0
				for ele in self.win:
					if ele in self.systemmodel[state].keys():
						nextstate = self.systemmodel[state][ele]
						self.trace.append(ele)
						state = nextstate
						self.win.remove(ele)

		if len(self.win) > 40:
			del self.win[0:20]

		self.currentstate = state



