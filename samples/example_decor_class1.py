import time
import os, sys

sys.path.append(os.path.realpath(".."))
import workerthread


class Printer:
	@workerthread.executeInWorkerThreadDecorator
	@workerthread.dumpArgsDecorator
	def printFromWorkerThread(message):
		print "\tprintFromWorkerThread %s Before sleep"%message
		i=0
		while i<5:
			time.sleep(2)
			print "\tprintFromWorkerThread %s Sleeping"%message
			i+=1
		print "\tprintFromWorkerThread %s After sleep. Finished"%message



if __name__ == '__main__':
	printer1 = Printer()
	
	printer1.printFromWorkerThread("Message 1")
	print "Message 1 task was posted to worker thread"
	
	printer1.printFromWorkerThread("Message 2")
	print "Message 2 task was posted to worker thread"
	
	
	
	i=0
	while i<6:
		time.sleep(3)
		print "main thread sleeping"
		i+=1
	print "Main thread sleep finished. Will wait for workerthread to finish"
	
	workerthread.finishThreadAndWaitForCompletion()