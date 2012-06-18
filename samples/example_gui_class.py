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
This example is to show how to use workerthread functions and decorators for class methods 
"""

import sys, os
import wx
import time

sys.path.append(os.path.realpath(".."))
import workerthread







	

class MyFrame(wx.Frame):
	def __init__(self, *args, **kwds):
		# begin wxGlade: MyFrame.__init__
		kwds["style"] = wx.DEFAULT_FRAME_STYLE
		wx.Frame.__init__(self, *args, **kwds)
		self.button_1 = wx.Button(self, -1, "Press me")
		self.text_ctrl_1 = wx.TextCtrl(self, -1, "Result will be here.", style=wx.TE_READONLY | wx.TE_CENTRE)
		self.__set_properties()
		self.__do_layout()
		self.Bind(wx.EVT_BUTTON, self.on_button_pressed, self.button_1)
		self.Center()
		
	def notifyGUIThread(self, message):
		self.text_ctrl_1.SetValue(message)
		
	@workerthread.executeInGUIThreadDecorator
	def notifyOnProcessFinishInGUIThread(self=None, message=""):
		self.text_ctrl_1.SetValue("Finished:"+message)
			
	def someLongWorkingFunction(self):
		print "\tsomeLongWorkingFunction starts in worker thread"
		i=0
		while i<5:
			time.sleep(2)
			workerthread.executeInGUIThread(
					lambda: self.notifyGUIThread("Processing:%s"%i)
				)
			
			print "\tsomeLongWorkingFunction: Doing some long work."
			if i==3:
				print "\tsomeLongWorkingFunction: i=3. Will notify GUI"
				workerthread.executeInGUIThread(
					lambda: self.notifyGUIThread("We are halfway to the end.")
				)
			i+=1
		#END while i<10:
		print "\tsomeLongWorkingFunction finished processing"
		self.notifyOnProcessFinishInGUIThread(self, "long processing: finished")
		
	@workerthread.executeInWorkerThreadDecorator	
	def someLongWorkingFunctionDecoratedForWorkerThread(self):
		print "\tsomeLongWorkingFunction starts in worker thread"
		i=0
		while i<5:
			time.sleep(2)
			workerthread.executeInGUIThread(
					lambda: self.notifyGUIThread("Processing:%s"%i)
				)
			
			print "\tsomeLongWorkingFunction: Doing some long work."
			if i==3:
				print "\tsomeLongWorkingFunction: i=3. Will notify GUI"
				workerthread.executeInGUIThread(
					lambda: self.notifyGUIThread("We are halfway to the end.")
				)
			i+=1
		#END while i<10:
		print "\tsomeLongWorkingFunction finished processing"
		self.notifyOnProcessFinishInGUIThread(self, "long processing: finished")
		
	
		
	
		
	def on_button_pressed(self, event):
		print "Will start long task"
		workerthread.executeInWorkerThread(
			self.someLongWorkingFunction
			#You do not need lambda, if function does not take parameters
			)
		print "Will also post decorated logn working function"
		self.someLongWorkingFunctionDecoratedForWorkerThread(self)
		

	def __set_properties(self):
		# begin wxGlade: MyFrame.__set_properties
		self.SetTitle("workerthead WXPython test frame (class methods)")
		self.text_ctrl_1.SetMinSize((500, 50))
		self.text_ctrl_1.SetFont(wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: MyFrame.__do_layout
		sizer_1 = wx.BoxSizer(wx.VERTICAL)
		sizer_2 = wx.BoxSizer(wx.VERTICAL)
		sizer_2.Add(self.button_1, 0, wx.ALL | wx.EXPAND, 10)
		sizer_2.Add(self.text_ctrl_1, 0, wx.ALL | wx.EXPAND, 10)
		sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
		self.SetSizer(sizer_1)
		sizer_1.Fit(self)
		self.Layout()
		# end wxGlade

applicationFrame = None

# end of class MyFrame
if __name__ == "__main__":
	global applicationFrame
	app = wx.PySimpleApp(0)
	wx.InitAllImageHandlers()
	applicationFrame = MyFrame(None, -1, "")
	app.SetTopWindow(applicationFrame)
	applicationFrame.Show()
	#Next line will block until wx application loop is working
	app.MainLoop()
	print "GUI looop finished"
	workerthread.finishThreadAndWaitForCompletion()
	print "Worker thread finished"
