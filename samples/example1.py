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
import time
import os, sys


sys.path.append(os.path.realpath(".."))
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
	print "Message 1 task was posted to worker thread"
	
	workerthread.executeInWorkerThread(
		lambda: printFromWorkerThread("Message 2")
	)
	print "Message 2 task was posted to worker thread"
	
	i=0
	while i<6:
		time.sleep(3)
		print "main thread sleeping"
		i+=1
	print "Main thread sleep finished. Will wait for workerthread to finish"
	
	workerthread.finishThreadAndWaitForCompletion()