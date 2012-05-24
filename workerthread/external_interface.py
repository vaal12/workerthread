import globals
import workerthread
try:
    import wx
except ImportError:
    wx = None

def dummyFunction():
    print "THis is a dummy function doing nothing"

def test2Print():
	print "test2Print - OK"

if not wx:
  test2Print = dummyFunction


def executeInWorkerThread(function2execute, delay_ms=0, result_callback=None):
	if delay_ms == 0:
		globals.workerThreadInstance.postWork(function2execute)
	else:
		globals.workerThreadInstance.postWorkTimed(function2execute, delay_ms)
	
def executeInGUIThread(function2execute, delay_ms=0, result_callback=None):
	print "executeInGUIThread Function stub"
	
def finishThreadAndWaitForCompletion():
	globals.workerThreadInstance.abortAndWaitForCompletion()