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
This package provides a simple implementation and interface for one extra thread. Such thread is useful, when you need only a 'light' multithreading e.g. only for non blocking GUI or user input.
Such model - one user interaction thread and one worker thread is quite useful for the following scenarios:
	1. You are either not experienced with threads or do not have time to design a 	good thread interaction model.
	2. One execution thread for lengthy tasks (e.g. network or long processing) is 	really all you need. 
	3. You are tired/not sure how to synchronize threads properly. For this: one execution thread is ideal as all tasks you post there are executed consequtively, thus removing a need to any synchronization at all between them. User interaction 	thread is a different thing, but synchronization of 2 threads is so much easier to debug.
Drawbacks of the model is that you only have one worker thread and if you do extensive network/disk reading/writing you might need a bit more threads.
For this library I have in plan to provide "named" threads that is you will be able to create as many threads as you need with the same interface as current one thread has.

All user callable functions/decorators are collected in the external_interface.py file. Please read it's documentation for user functions.
Samples for the package are in the samples folder, but snippets of those will be copied in the documents. Also relevant samples will be linked from this documentation.

B{General usage notes:}
	1. Just import workerthread module and it will automatically start one instance of the workerthread. It will be only one instance regardless of the number of imports (sigleton pattern).
	2. Via workerthread.executeInWorkerThread function or @workerthread.executeInWorkerThreadDecorator post functions to execute in worker thread. Those functions will not block as they will just post tasks to the worker thread.
	3. No means to return values from tasks in workerthread are available, it is recommended to use result_callback function pointer to process result of the task. If you use Wxpython there is a helper function executeInGUIThread, which will reroute execution of the function back to GUI thread (to update widgets for example). See samples\example_gui.py .
	4. If you need to exit application call workerthread.finishThreadAndWaitForCompletion(). This function will block until all delayed functions due to the moment of completion are executed (if there are functions due after stop point, they may be silently discarded) and all queued (non delayed) before this call functions are also executed (all non delayed functions after this call will be silently discarded).
	Note on exit: generally you may exit the application without shutting down the worker thread, but python may complain on the exiting of the application while other threads are running.
	Note on naming: it is quite error prone to debug threading code, event with only 2 threads involved. I generally recommend naming functions, which will be executed in the workerthread as such (e.g. printFromWorkerThread(message)), so when reading the code it will be clear in which thread the code will be executed.


B{Platforms:} this package was written and tested on Python 2.7 platform on Windows.
At the moment I will not have resources to test this package on other version and/or OSes, so if you will have any experience running workerthread with those, please, let me know, so I will update this information.
This package only requires standard python modules (e.g. os, threading, Queue, time) if you intend to use the package with wxpython, obviously it will need to be properly installed your machine.

B{Lisense}: this library can be used in either open source or closed source (including for commercial purposes) freely, provided that attribution that this library is used is made. For formal lisence and Copyright, please see individual source files.
"""
from external_interface import *
import init_module
