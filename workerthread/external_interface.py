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
Packaging link: http://guide.python-distribute.org/introduction.html

Documentation links:

http://epydoc.sourceforge.net/

http://www.oracle.com/technetwork/java/javase/documentation/index-jsp-135444.html



"""
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
	#	
	pass




def trace(f):
	#From http://wiki.python.org/moin/PythonDecoratorLibrary#Line_Tracing_Individual_Functions
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