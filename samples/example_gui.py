import sys, os
import wx
import time

sys.path.append(os.path.realpath(".."))
import workerthread

def notifyGUIThread(message):
	applicationFrame.text_ctrl_1.SetValue(message)

@workerthread.executeInWorkerThreadDecorator	
def notifyOnProcessFinishInGUIThread(message):
	applicationFrame.text_ctrl_1.SetValue("Long function finished with message:"+message)

def someLongWorkingFunction():
	print "\tsomeLongWorkingFunction starts in worker thread"
	i=0
	while i<10:
		time.sleep(2)
		workerthread.executeInGUIThread(
				lambda: notifyGUIThread("Processing:%s"%i)
			)
		
		print "\tsomeLongWorkingFunction: Doing some long work."
		if i==5:
			print "\tsomeLongWorkingFunction: i=5. Will notify GUI"
			workerthread.executeInGUIThread(
				lambda: notifyGUIThread("We are halfway to the end.")
			)
		i+=1
	#END while i<10:
	print "\tsomeLongWorkingFunction finished processing"
	notifyOnProcessFinishInGUIThread("long processing: finished")
	

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
		# end wxGlade
		
	def on_button_pressed(self, event):
		print "Will start long task"
		workerthread.executeInWorkerThread(
			someLongWorkingFunction
			#You do not need lambda, if function does not take parameters
			)
		

	def __set_properties(self):
		# begin wxGlade: MyFrame.__set_properties
		self.SetTitle("workerthead WXPython test frame")
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
