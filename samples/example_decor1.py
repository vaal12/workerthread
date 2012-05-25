import time
import os, sys

sys.path.append(os.path.realpath(".."))
import workerthread

@workerthread.executeInWorkerThreadDecorator
@workerthread.dumpArgsDecorator
def dumpMyArgumentsFromWorkerThread(message, key):
	print "This is print from dumpMyArguments"


@workerthread.executeInWorkerThreadDecorator
def printFromWorkerThread(message):
	print "\tprintFromWorkerThread %s Before sleep"%message
	i=0
	while i<5:
		time.sleep(2)
		print "\tprintFromWorkerThread %s Sleeping"%message
		i+=1
	print "\tprintFromWorkerThread %s After sleep. Finished"%message
	
@workerthread.executeInWorkerThreadDecorator	
@workerthread.trace
def traceExampleFromWorkerThread(message):
	print "MEssage"
	print message
	return None
	
	
	
if __name__ == '__main__':
	printFromWorkerThread("Message 1")
	print "Message 1 task was posted to worker thread"
	
	printFromWorkerThread("Message 2")
	print "Message 2 task was posted to worker thread"
	
	dumpMyArgumentsFromWorkerThread("Message to function", "Key to function")
	
	traceExampleFromWorkerThread("Message to trace")
	
	i=0
	while i<6:
		time.sleep(3)
		print "main thread sleeping"
		i+=1
	print "Main thread sleep finished. Will wait for workerthread to finish"
	
	workerthread.finishThreadAndWaitForCompletion()