import time

import workerthread

def printFromWorkerThread(message):
	print "\tprintFromWorkerThread %s Before sleep"%message
	i=0
	while i<5:
		time.sleep(2)
		print "\tprintFromWorkerThread %s Sleeping"%message
		i+=1
	print "\tprintFromWorkerThread %s After sleep. Finished"%message
	
	
if __name__ == '__main__':
	workerthread.executeInWorkerThread(
		lambda: printFromWorkerThread("Message 1")
	)
	
	workerthread.executeInWorkerThread(
		lambda: printFromWorkerThread("Message 2")
	)
	
	i=0
	while i<6:
		time.sleep(3)
		print "main thread sleeping"
		i+=1
	print "Main thread sleep finished. Will wait for workerthread to finish"
	
	workerthread.finishThreadAndWaitForCompletion()