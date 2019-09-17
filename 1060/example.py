import os
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtCore import QCoreApplication
from PySide2.QtWidgets import QAction

os.environ["QT_SCREEN_SCALE_FACTORS"] = "2"

app = QtWidgets.QApplication(["tray_icon_test"])
app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
app.setQuitOnLastWindowClosed(False)

icon_file = ("example.svg")
print(icon_file)
icon = QtGui.QIcon.fromTheme(icon_file)
tray_icon = QtWidgets.QSystemTrayIcon(icon)

quitAction = QAction("&Quit", tray_icon);
    # connect(quitAction, &QAction::triggered, qApp, &QCoreApplication::quit);

quitAction.triggered.connect(QCoreApplication.quit())
tray_icon.show()
app.exec_()
