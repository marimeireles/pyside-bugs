import sys

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QUrl
from PySide2.QtQml import QQmlApplicationEngine, qmlRegisterType

from custom_view import CustomView

import qml_rc  # noqa: F401


if __name__ == "__main__":
   app = QApplication(sys.argv)
   qmlRegisterType(CustomView, "CustomView", 1, 0, "CustomView")
   engine = QQmlApplicationEngine()
   engine.load(QUrl("qrc:/main.qml"))

   if not engine.rootObjects():
       sys.exit(-1)

   sys.exit(app.exec_())
