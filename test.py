from stack import Stack
s = Stack()
from simulation import  Trace


milestone = ['ACK', 'Fake']
initqueue = ['B2','A1', 'S','B1', 'A3', 'A2', 'A2', 'A5',]
initqueue2 = ['A2', 'S', 'A3', 'A3', 'A2', 'A5','B2']
t = Trace()
print t.xmlparse('event1.xml')
print "------------"
t.setstate("p0")
t.transition(initqueue)
print t.win
print t.trace

def memoryparse():
	memlist = []
	mem = "['<send@plt>']<-['<func>']<-['<A2>']<-['<A3>']<-['<A5>']<-['<__libc_start_main@plt>']"
	memlist = mem.split('<-')
	funclist = []
	for func in memlist:
		funclist.append(func[3:-3])
	return funclist





if __name__=='__main__':
	func = memoryparse()
	for m in func:
		s.push([m])
	print s.getdata(10)