"""
Previous versions are in workerthread.py of AndroidFileSyncClient project.
Main idea from http://wiki.wxpython.org/LongRunningTasks
Function parameters from: http://stackoverflow.com/questions/803616/passing-functions-with-arguments-to-another-function-in-python
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
		#print "Current time:%s"%currTime
		futureTime = currTime+(delayInterval_ms/1000.0)
		#print "Future time:%s"%futureTime
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

	def postWork(self, functionToExecute):
		self.worksQueue.put(functionToExecute)

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
					try:#This will block for 0.1 sec waiting for the non timed task
						func_2do = self.worksQueue.get(True, 2)
					except Exception as e:
						pass
			except Exception as e:
				pass#print "Some exception occured:%s"%e
			#END try:
			if func_2do==-1:
				break
			else:
				if isinstance(func_2do, collections.Callable):
					try:
						func_2do()
					except Exception as e:
						if not (wx==None):
							exception_window.call_exception_dialog_NONGUI_thread("Exception in WorkerThread",
										"Nothing can be done at the moment. Please send this report to developer",
										"WorkerThread exception executing user code")
			#END if func_2do==-1:
		self.abortionEvent.set()
	#END def run(self):

	def abort(self):
		"""abort worker thread."""
		# Method for use by main thread to signal an abort
		self.worksQueue.put(-1)
		
	def abortAndWaitForCompletion(self):
		self.abort()
		self.abortionEvent.wait()
		#self.join()
#End class WorkerThread(threading.Thread):