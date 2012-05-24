import sys, os
#import wx

sys.path.append(os.path.realpath(".."))
import workerthread

workerthread.test2Print()

workerthread.finishThreadAndWaitForCompletion()