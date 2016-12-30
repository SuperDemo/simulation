class Stack():
	def __init__(self,size=10):
		self.size = size
		self.stack = []
		self.top = -1
		
	def push(self,ele):
		if self.isfull():
			for i in range(self.size/2):
				self.stack.pop(0)
				#raise Exception("out of range")
			self.top = self.top - self.size/2
		
		else:
			self.stack.append(ele)
			self.top = self.top + 1

	def pop(self):
		if self.isempty():
			raise Exception("stack is  empty")

		else:
			self.top = self.top - 1
			return self.stack.pop()

	def getdata(self,datalen = 1):
		if self.isempty():
			raise Exception("stack is  empty")

		elif datalen > self.top:
			datalen = self.top

		return self.stack[0:datalen]

	def isfull(self):
		return self.top + 1 == self.size

	def isempty(self):
		return self.top == -1


