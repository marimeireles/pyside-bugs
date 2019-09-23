from PyQt5 import QtCore, QtWidgets, QtNetwork
import objgraph
import sys

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
        self.request = self.reply = None

App('http://www.google.com').run()

