import globals
import workerthread
try:
    import wx
except ImportError:
    wx = None

def dummyFunction():
    print "It seems that wxpython is not installed properly. \nThis function cannot work without wxpython.\n This is a stub, which is doing nothing"




def executeInWorkerThread(function2execute, delay_ms=0, result_callback=None):
	if delay_ms == 0:
		globals.workerThreadInstance.postWork(function2execute)
	else:
		globals.workerThreadInstance.postWorkTimed(function2execute, delay_ms)
	
def executeInGUIThread(function2execute):
	wx.CallAfter(function2execute)
	
def finishThreadAndWaitForCompletion():
	globals.workerThreadInstance.abortAndWaitForCompletion()
	
	
if not wx:
  executeInGUIThread = dummyFunction