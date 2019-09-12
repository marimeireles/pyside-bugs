import os
from PySide2 import QtCore, QtWidgets, QtGui

os.environ["QT_SCREEN_SCALE_FACTORS"] = "2"

app = QtWidgets.QApplication(["tray_icon_test"])
app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
app.setQuitOnLastWindowClosed(False)

icon_file = os.path.join(os.path.dirname(__file__), "example.svg")
print(icon_file)
icon = QtGui.QIcon.fromTheme(icon_file)
tray_icon = QtWidgets.QSystemTrayIcon(icon)
tray_icon.show()

app.exec_()
