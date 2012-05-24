"""
Previous versions are in workerthread.py of AndroidFileSyncClient project.
"""

import sys
import traceback
import urllib
import urllib2
import datetime
import logging

try:
    import wx
except ImportError:
    wx = None

"""
  traceback doc: http://docs.python.org/library/traceback.html
"""

if wx == None:
	pass
else:#if wx == None:
	class ExceptionDialog(wx.Dialog):
		URL_2SUBMIT = "http://verneronweb.com/php_receive/i.php"	
	
		def __init__(self, whatText, canIDoText, reportText):
			kwds = {}
			kwds["style"] = wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP
			wx.Dialog.__init__(self, None, -1, "", **kwds)

			self.whatText = whatText
			self.canIDoText = canIDoText
			self.reportText = reportText
		
			self.whatHappenedTextCtrl_copy = wx.TextCtrl(self, -1, self.whatText, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2 | wx.NO_BORDER)
			self.whatHappenedSizer_copy_staticbox = wx.StaticBox(self, -1, "What happened")
			self.whatCanIDoTextCtrl = wx.TextCtrl(self, -1, self.canIDoText, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2 | wx.NO_BORDER)
			self.whatCanIDoSizer_staticbox = wx.StaticBox(self, -1, "What can I do")
			self.programOutputTextCtrl = wx.TextCtrl(self, -1, self.reportText, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2 | wx.NO_BORDER)
			self.progOutputSizer_staticbox = wx.StaticBox(self, -1, "Programm output, which will be sent")
			self.text_ctrl_1 = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE | wx.TE_RICH2)
			self.yourDescriptionSizer_staticbox = wx.StaticBox(self, -1, "Please provide your comment, description of the situation")
			self.sendReport2DeveloperSizer_staticbox = wx.StaticBox(self, -1, "Send report to developer")
			self.sendButton = wx.Button(self, -1, "Send report and comment")
			self.cancelButton = wx.Button(self, -1, "Cancel (don't send)")

			self.__set_properties()
			self.__do_layout()
		
			self.Bind(wx.EVT_BUTTON, self.on_send_button, self.sendButton)
			self.Bind(wx.EVT_BUTTON, self.on_cancel_button, self.cancelButton)
		
			self.Center()
			self.text_ctrl_1.SetFocus()
		
		def on_send_button(self, event):
			url = ExceptionDialog.URL_2SUBMIT
			values = {'report' : self.reportText.encode("utf-8"),
				'user_comment' : self.text_ctrl_1.GetValue().encode("utf-8"),
			  'version' : "undefined" }
			data = urllib.urlencode(values)
			req = urllib2.Request(url, data)
			the_page = "Error receiving the page. This is dummy text."
			try:
				response = urllib2.urlopen(req)
				the_page = response.read()
			except Exception as e:
				pass
			self.EndModal(wx.ID_OK)
		
		def on_cancel_button(self, event):
			self.EndModal(wx.ID_CANCEL)

		def __set_properties(self):
			# begin wxGlade: MyDialog2.__set_properties
			self.SetTitle("Error report window")
			self.SetSize((699, 427))
			# end wxGlade

		def __do_layout(self):
			MainVertSizer_copy = wx.BoxSizer(wx.VERTICAL)
			bottomButtonsSizer = wx.BoxSizer(wx.HORIZONTAL)
			self.sendReport2DeveloperSizer_staticbox.Lower()
			sendReport2DeveloperSizer = wx.StaticBoxSizer(self.sendReport2DeveloperSizer_staticbox, wx.HORIZONTAL)
			self.yourDescriptionSizer_staticbox.Lower()
			yourDescriptionSizer = wx.StaticBoxSizer(self.yourDescriptionSizer_staticbox, wx.HORIZONTAL)
			self.progOutputSizer_staticbox.Lower()
			progOutputSizer = wx.StaticBoxSizer(self.progOutputSizer_staticbox, wx.HORIZONTAL)
			self.whatCanIDoSizer_staticbox.Lower()
			whatCanIDoSizer = wx.StaticBoxSizer(self.whatCanIDoSizer_staticbox, wx.HORIZONTAL)
			self.whatHappenedSizer_copy_staticbox.Lower()
			whatHappenedSizer_copy = wx.StaticBoxSizer(self.whatHappenedSizer_copy_staticbox, wx.HORIZONTAL)
			whatHappenedSizer_copy.Add(self.whatHappenedTextCtrl_copy, 1, wx.EXPAND, 0)
			MainVertSizer_copy.Add(whatHappenedSizer_copy, 2, wx.EXPAND, 0)
			whatCanIDoSizer.Add(self.whatCanIDoTextCtrl, 1, wx.EXPAND, 0)
			MainVertSizer_copy.Add(whatCanIDoSizer, 2, wx.EXPAND, 0)
			progOutputSizer.Add(self.programOutputTextCtrl, 1, wx.EXPAND, 0)
			sendReport2DeveloperSizer.Add(progOutputSizer, 1, wx.EXPAND, 0)
			yourDescriptionSizer.Add(self.text_ctrl_1, 1, wx.EXPAND, 0)
			sendReport2DeveloperSizer.Add(yourDescriptionSizer, 1, wx.EXPAND, 0)
			MainVertSizer_copy.Add(sendReport2DeveloperSizer, 3, wx.EXPAND, 0)
			bottomButtonsSizer.Add((20, 10), 1, 0, 0)
			bottomButtonsSizer.Add(self.sendButton, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
			bottomButtonsSizer.Add(self.cancelButton, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
			MainVertSizer_copy.Add(bottomButtonsSizer, 1, wx.EXPAND, 0)
			self.SetSizer(MainVertSizer_copy)
			self.Layout()
	# end of class ExceptionDialog
#END else:#if wx == None:


def call_exception_dialog_NONGUI_thread(whatText, canIDoText, additionalReport = None, excpt = None):
	ex_type, ex_value, ex_trace = 	sys.exc_info()
	expt_text = traceback.format_exception(ex_type, ex_value, ex_trace)
	
	resultStr = "Error generated time:%s \n\n"%datetime.datetime.now()
	for line in expt_text:
		resultStr +=line
	if additionalReport<>None:
		resultStr += "\n\n Additional information:\n\t%s"%additionalReport
	wx.CallAfter(lambda: callDialogModal(whatText=whatText,
		canIDoText = canIDoText,
		resultStr = resultStr)
		)#CallAfter
	
def callDialogModal(whatText, canIDoText, resultStr):
	dialog = ExceptionDialog(
		whatText=whatText,
		canIDoText = canIDoText,
		reportText = resultStr
		)
	app = wx.GetApp()
	currTopWin = app.GetTopWindow()
	currTopWin.Hide()
	app.SetTopWindow(dialog)
	dialog.ShowModal()
	currTopWin.Show()
	app.SetTopWindow(currTopWin)
	

def call_exception_dialog(whatText, canIDoText, additionalReport = None, excpt = None):
	ex_type, ex_value, ex_trace = 	sys.exc_info()
	expt_text = traceback.format_exception(ex_type, ex_value, ex_trace)
	
	resultStr = "Error generated time:%s \n\n"%datetime.datetime.now()
	for line in expt_text:
		resultStr +=line
	if additionalReport<>None:
		resultStr += "\n\n Additional information:\n\t%s"%additionalReport
	dialog = ExceptionDialog(
		whatText=whatText,
		canIDoText = canIDoText,
		reportText = resultStr
		)
	dialog.ShowModal()
	