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
	
def dumpArgsDecorator(func):
	#From http://wiki.python.org/moin/PythonDecoratorLibrary
	"This decorator dumps out the arguments passed to a function before calling it"
	argnames = func.func_code.co_varnames[:func.func_code.co_argcount]
	fname = func.func_name
	
	def echo_func(*args,**kwargs):
		#TODO: enable logging
		#logging.debug("Function %s is called"%fname)
		#i=0
		#for argument_name in argnames:
		#	logging.debug("\tArgument [%s]=[%s]"%(argument_name, args[i]))
		#	i+=1
		#for item in kwargs.items():
		#	logging.debug("\tKeyword argument [%s]=[%s]"%(item, kwargs[item]))
#		msg = fname, ":", ', '.join(
#			'%s=%r' % entry
#			for entry in zip(argnames,args) + kwargs.items())
#		logging.debug(msg)
		print fname, ":", ', '.join(
			'%s=%r' % entry
			for entry in zip(argnames,args) + kwargs.items())
		return func(*args, **kwargs)
	return echo_func


class executeInWorkerThreadDecorator(object):
	def __init__(self, f):
		#print "Inside __init__()"
		#Doc on decorators http://www.artima.com/weblogs/viewpost.jsp?thread=240845
		self.f = f

	def __call__(self, *args):
		#TODO: add support for kwargs
		globals.workerThreadInstance.postWork(
			lambda: self.f(*args)
		)
		#print "After self.f(*args)"



class executeInGUIThreadDecorator(object):
	#TODO: enable and test
	#def __init__(self, f):
	#	#print "Inside __init__()"
	#	#Doc on decorators http://www.artima.com/weblogs/viewpost.jsp?thread=240845
	#	self.execFunc = f
	#
	#def __call__(self, *args):
	#	#print "Inside __call__()"
	#	#print "Sending to other thread"
	#	wx.CallAfter(
	#		lambda: self.execFunc(*args)
	#	
	pass

	
if not wx:
  executeInGUIThread = dummyFunction