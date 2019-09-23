from PySide2 import QtCore, QtWidgets, QtNetwork
from PySide2.QtCore import QCoreApplication
import objgraph
import sys

class App:
    def __init__(self, url):
        self.url = url
        self.app = QCoreApplication(sys.argv)
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
        print(self.reply)
        self.request = self.reply = None

App('http://www.google.com').run()

#test it using qtthreads

#when I del stuff it obviously works
#when I use QCoreApplication it still crashes so, there is no diff between
    #using QCoreApplication or QApplication