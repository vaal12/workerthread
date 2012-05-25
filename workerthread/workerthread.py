"""
Previous versions are in workerthread.py of AndroidFileSyncClient project.
Main idea from http://wiki.wxpython.org/LongRunningTasks
Function parameters from: http://stackoverflow.com/questions/803616/passing-functions-with-arguments-to-another-function-in-python
"""


"""
1. If this does not stop by itself Ctrl+Pause/Break instead of Ctrl+C can stop all
python threads from console

"""

import threading
import Queue, collections
import time

try:
    import wx
except ImportError:
    wx = None

if not (wx==None):
	import exception_window


class TimedEvent:
	def __init__(self, function2Execute, delayInterval_ms):
		self.function2Execute = function2Execute
		currTime = time.time()
		futureTime = currTime+(delayInterval_ms/1000.0)
		self.time2Execute = futureTime
		
class WorkerThread(threading.Thread):
	"""Worker Thread Class."""
	def __init__(self):
		"""Init Worker Thread Class."""
		threading.Thread.__init__(self)
		self._want_abort = 0
		# This starts the thread running on creation, but you could
		# also make the GUI thread responsible for calling this
		self.worksQueue = Queue.Queue()
		self.timedList = []
		self.timedListLock = threading.Lock();
		self.abortionEvent = threading.Event()
		self.start()

	def postWorkTimed(self, functionToExecute, delay_ms):
		self.timedListLock.acquire()
		te = TimedEvent(functionToExecute, delay_ms)
		self.timedList.append(te)
		self.timedListLock.release()

	def postWork(self, functionToExecute, result_callback=None):
		self.worksQueue.put(
			(functionToExecute, result_callback)
			)

	def run(self):
		"""Run Worker Thread."""
		while True:
			#print "WorkerThread heartbeat"
			func_2do = None
			try:
				func_2do = None
				self.timedListLock.acquire()
				i=0
				currTime = time.time()
				while i<len(self.timedList):
					if currTime > self.timedList[i].time2Execute:
						func_2do = self.timedList[i].function2Execute
						self.timedList.pop(i)
						break
					i+=1
				self.timedListLock.release()
				if func_2do==None:
					try:#This will block for 2sec waiting for the non timed task
						#TODO: make waiting timeout settable from external_interface
						#of the workerthread
						(func_2do, result_callback) = self.worksQueue.get(True, 2)
						#print "Received func_2do:%s"%func_2do
					except Queue.Empty as empty_exception:
						#This is fine: Queue.Empty is supposed to be thrown when timeout is reached
						#http://docs.python.org/library/queue.html
						pass
			except Exception as e:
				pass
				print "Some exception occured in retrieval of the function to execute:%s"%e
			#END try:
			if func_2do==-1:
				#print "Function is -1 should stop"
				break
			else:#if func_2do==-1:
				if isinstance(func_2do, collections.Callable):
					execResult = None
					try:
						execResult = func_2do()
					except Exception as e:
						print "Exception in execution of the function in the workerthread"
						print e
						if not (wx==None):
							exception_window.call_exception_dialog_NONGUI_thread("Exception in WorkerThread",
										"Nothing can be done at the moment. Please send this report to developer",
										"WorkerThread exception executing user code")
					if result_callback <> None:
						try:
							result_callback(execResult)
						except Exception as e:
							print "Exception in execution of the result callback function in the workerthread"
							print e
					print "After result callback"
			#END else:#if func_2do==-1:
		self.abortionEvent.set()
	#END def run(self):

	def abort(self):
		"""abort worker thread."""
		# Method for use by main thread to signal an abort
		#TODO: make a Workthread event to be posted both to timedqueue and to normal
		#queues, which will have all the necessary fields
		self.worksQueue.put((-1, None))
		
	def abortAndWaitForCompletion(self):
		self.abort()
		self.abortionEvent.wait()
		#self.join()
#End class WorkerThread(threading.Thread):