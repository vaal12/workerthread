import time
import os, sys
#Previous version was in file ../example1.py

sys.path.append(os.path.realpath(".."))
import workerthread

def printFromWorkerThread2(message):
	print "\tprintFromWorkerThread %s Before sleep"%message
	i=0
	while i<5:
		time.sleep(2)
		print "\tprintFromWorkerThread %s Sleeping"%message
		i+=1
	print "\tprintFromWorkerThread %s After sleep. Finished"%message
	return message
	
	
def processResult(message):
	print "*"*30
	print "RESULT: received message:%s"%message
	print "*"*30
	
	
if __name__ == '__main__':
	workerthread.executeInWorkerThread(
		lambda: printFromWorkerThread2("Message 1"),
		result_callback = processResult
	)
	print "Message 1 task was posted to worker thread"
	
	workerthread.executeInWorkerThread(
		lambda: printFromWorkerThread2("Message 2"),
		delay_ms = 15000, #This should start approx 5 sec after finish of the first task
		result_callback = processResult
	)
	print "Message 2 task was posted to worker thread"
	
	i=0
	while i<6:
		time.sleep(3)
		print "main thread sleeping"
		i+=1
	print "Main thread sleep finished. Will wait for workerthread to finish"
	
	workerthread.finishThreadAndWaitForCompletion()