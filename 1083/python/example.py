import sys

from PySide2.QtCore import QSize, Qt
from PySide2.QtWidgets import *


class GraphicsView(QGraphicsView):
    def sizeHint(self):
        # Return scene size by default
        return QSize(500, 500)

    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene())
        self.scene().addText('ABC')
        self.scale(20, 20)

    def test(self):
        self.scale(0.9, 0.9)
        # self.update() <= This doesn't help either


class Test(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        self.setLayout(layout)

        view = GraphicsView()
        layout.addWidget(view)

        auto_button = QPushButton('auto')
        auto_button.clicked.connect(view.test, Qt.AutoConnection) # Also doesn't work with DirectConnection
        layout.addWidget(auto_button)

        queued_button = QPushButton('queued')
        queued_button.clicked.connect(view.test, Qt.QueuedConnection)
        layout.addWidget(queued_button)


app = QApplication(sys.argv)
view = Test()
view.show()
sys.exit(app.exec_())
