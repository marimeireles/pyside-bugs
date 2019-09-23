from PySide2 import QtCore, QtWidgets, QtNetwork
from PySide2.QtCore import QCoreApplication
import objgraph
import sys
import gc

class App:
    def __init__(self, url):
        self.url = url
        self.app = QtWidgets.QApplication(sys.argv)
        self.timer = QtCore.QTimer(self.app)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self._tick)
        self.manager = QtNetwork.QNetworkAccessManager(self.app)
        self.request = None

    def run(self):
        self.timer.start()
        sys.exit(self.app.exec_())

    def _tick(self):
        print("TICK")
        if self.request is not None:
            return
        objgraph.show_growth()
        print(objgraph.typestats())

        self.request = QtNetwork.QNetworkRequest()
        self.request.setUrl(QtCore.QUrl(self.url))
        self.request.setRawHeader(b"User-Agent", b"Test")
        self.reply = self.manager.get(self.request)
        self.reply.finished.connect(self._finished)

    def _finished(self):
        print("FINISHED")
        self.reply.close()
        self.reply.finished.disconnect()
        self.reply.deleteLater()
        # print(sys.getrefcount(self.reply))
        # del self.reply
        # print(sys.getrefcount(self.reply))
        # print(self.reply)
        gc.collect()
        self.request = self.reply = None

App('http://www.google.com').run()

#test it using qtthreads

#when I use QCoreApplication it still crashes so, there is no diff between
    #using QCoreApplication or QApplication

#when I use del also crashes
    #QNetwork increases and it's never deleted. the diff here for using
    #deleteLater() is that the weakref counter increases by 1
    #but even though this was supposed to remove at least one QNetwork(right?)
    #it doesn't happen

#this might be related to the ownership of the get method, used in line 31
    #/sources/pyside2/PySide2/QtCore/typesystem_core_common.xml
    #QNetworkAccessManager's get function
    #it might be a problem on this shiboken of this class
    #it might be a problem on the cpp implementation (that I don't even
    #know where it is :/)