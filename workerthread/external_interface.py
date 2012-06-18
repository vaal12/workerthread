#
# Copyright 2012 by Alexey Vassiliev
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
This module provides a user/external inteface to the workerthread library.
All functions/decorators listed here are intended to be used in the user code.

"""
#Packaging link: http://guide.python-distribute.org/introduction.html
#
#Documentation links:
#
#http://epydoc.sourceforge.net/
#
#http://www.oracle.com/technetwork/java/javase/documentation/index-jsp-135444.html




#TODO: Think about adding http://wiki.python.org/moin/PythonDecoratorLibrary#Synchronization
#Synchronizing decorator

#TODO: add software licence to all files.

import sys
import os
import linecache

import globals
import workerthread
try:
	import wx
except ImportError:
	wx = None

def dummyFunction():
	"""
	This function is used to stub wx related functions in case wx is not present
	"""
	print "It seems that wxpython is not installed properly. \nThis function cannot work without wxpython.\n This is a stub, which is doing nothing"


def executeInWorkerThread(function2execute, delay_ms=0, result_callback=None):
	"""
	This function posts a function2execute function to workerthread queue for execution.
	@param function2execute: function to execute in the workerthread
	@type function2execute: function pointer or lambda expression
	@param delay_ms: delay after which function2execute will be executed.	
	@type delay_ms: delay in milliseconds
	@param result_callback: function to execute in the workerthread when result of function2execute is available. Function result_callback will receive a result returned by function2excute 
	@type result_callback: function pointer or lambda expression
	@return: nothing
	Note: delay between call to this function and actual execution cannot be exactly delay_ms. It is only guaranteed that function2execute will be executed on or after delay_ms is passed. For more on the queueing/execution of functions in workerthread, see package documentation.
	
	Example in - samples/example1.py
	"""
	if delay_ms == 0:
		globals.workerThreadInstance.postWork(function2execute, result_callback)
	else:#executeInWorkerThread
		globals.workerThreadInstance.postWorkTimed(function2execute, delay_ms)
	
def executeInGUIThread(function2execute):
	"""
	This function posts a function2execute to GUI thread queue for execution (WXPython only!).
	@param function2execute: function to execute in the workerthread
	@type function2execute: function pointer
	Note: only works if wxpython is properly installed and wx module can be imported. If this cannot be done then executeInGUIThread will be replaces with call to dummyFunction.
	"""
	wx.CallAfter(function2execute)
	
def finishThreadAndWaitForCompletion():
	"""
	This function notifies the workerthread that it should terminate and then waits for the workerthread to terminate.
	Note: This function will block until all delayed functions due to the moment of completion are executed (if there are functions due after stop point, they may be silently discarded) and all queued (non delayed) before this call functions are also executed (all non delayed functions after this call will be silently discarded).
	See any sample on this function.
	"""
	globals.workerThreadInstance.abortAndWaitForCompletion()
	
def dumpArgsDecorator(func):
	"""
	This is a helper decorator to be used for debugging. This decorator dumps out the arguments passed to a function before calling it.
	
	Code is taken from U{http://wiki.python.org/moin/PythonDecoratorLibrary}
	Note: at the moment it only dumps arguments to stdout, in future I will add dumping those to log (via loggin module).
	
	Example of usage: samples\example_decor1.py 
	"""
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
	"""
	This decorator posts the decorated function to the workerthread for execution. 
	You do not need to call executeInWorkerThread functions. 
	No need to use lambdas in the code as any parameters can be passed as 
	Drawbacks: at the moment does not allow use of delay_ms and result_callback

	Example::
		@workerthread.executeInWorkerThreadDecorator
		def printFromWorkerThread(message):
			print "\tprintFromWorkerThread %s Before sleep"%message
			i=0
			while i<5:
				time.sleep(2)
				print "\tprintFromWorkerThread %s Sleeping"%message
				i+=1
			print "\tprintFromWorkerThread %s After sleep. Finished"%message
		
		printFromWorkerThread("Message 1")#This will execute in workerthread
		#This is exacly why I name functions with indication of workerthread otherwise
		# this can be quite confusing.
	
	See example: samples\example_decor1.py 
	"""
	#TODO: add parameter for delay and if possible for result_callback
	#TODO: test with class methods
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
	
	
	#TODO: test with class methods
	def __init__(self, f):
		#print "Inside __init__()"
		#Doc on decorators http://www.artima.com/weblogs/viewpost.jsp?thread=240845
		self.f = f

	def __call__(self, *args):
		#TODO: add support for kwargs
		executeInGUIThread(lambda: self.f(*args))
		#print "After self.f(*args)"




def trace(f):
	"""
	Decorator, which will trace with code line numbers execution of the function.
	Very useful for debugging. May be chained with other decorators::
		@workerthread.executeInWorkerThreadDecorator	
		@workerthread.trace
		def traceExampleFromWorkerThread(message):
			print "MEssage"
			print message
			return None
			
	See example of usage in samples\example_decor1.py 
	
	Code taken from U{http://wiki.python.org/moin/PythonDecoratorLibrary#Line_Tracing_Individual_Functions}
	"""
	def globaltrace(frame, why, arg):
			if why == "call":
					return localtrace
			return None

	def localtrace(frame, why, arg):
			if why == "line":
					# record the file name and line number of every trace
					filename = frame.f_code.co_filename
					lineno = frame.f_lineno

					bname = os.path.basename(filename)
					print "{}({}): {}".format(  bname, 
																			lineno,
																			linecache.getline(filename, lineno)),
			return localtrace

	def _f(*args, **kwds):
			sys.settrace(globaltrace)
			result = f(*args, **kwds)
			sys.settrace(None)
			return result

	return _f

	
if not wx:
  executeInGUIThread = dummyFunction