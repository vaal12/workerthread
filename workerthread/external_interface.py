"""
Packaging link: http://guide.python-distribute.org/introduction.html

Documentation links:

http://epydoc.sourceforge.net/

http://www.oracle.com/technetwork/java/javase/documentation/index-jsp-135444.html

"""

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
		globals.workerThreadInstance.postWork(function2execute, result_callback)
	else:
		globals.workerThreadInstance.postWorkTimed(function2execute, delay_ms)
	
def executeInGUIThread(function2execute):
	wx.CallAfter(function2execute)
	
def finishThreadAndWaitForCompletion():
	globals.workerThreadInstance.abortAndWaitForCompletion()
	
	
if not wx:
  executeInGUIThread = dummyFunction