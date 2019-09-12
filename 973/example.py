import sys
import webbrowser
import permissions
from output.html import HTMLOutput
from output.pdf import PDFOutput
from output.xl import XLOutput
from output.csv import CSVOutput
from PySide2 import QtCore, QtWidgets, QtGui
#for WebChannel js->py
from PySide2.QtWebChannel import QWebChannel
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import *
from PySide2.QtCore import QSize, QUrl, Qt, Slot
from PySide2.QtWebEngineWidgets import QWebEngineView
from viewer_data.ViewerDataGenerator import ViewerDataGenerator
import os
from . import scheme
from .viewer import Viewer
from .reference_holder import Referencer
from . import export_files

import shared



class ReportMenu(QMainWindow):
    has_config = True
    reportname = "generic"
    licencedata = {"lanrs" : {}, "bsnrs" : {}}#for demo buy

    def __init__(self, data, datacontainer, title="HonorarPlus", visible=True):
        QMainWindow.__init__(self)
        self.rid = Referencer.register(self)
        self.datacontainer = datacontainer
        self.data = data
        self.setMinimumSize(QSize(800, 600))
        self.setWindowTitle(title)
        self.late_init()
        if visible:
            self.showMaximized()
        self.activateWindow()
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon( scriptDir + os.path.sep + 'logo.png'))

    def late_init(self):
        webpage = HTMLOutput(self.data, "Data")
        webpagetask = shared.threadpool.submit(webpage.output)
        scheme.SchemeHandler.register(webpagetask.result, self.reportname)
        self.loader = QWebEngineView()

        # self.loader.setUrl(QUrl(r"https://www.google.de"))
        self.loader.setUrl(QUrl("conapp://" + self.reportname))
        self.loader.setContextMenuPolicy(Qt.PreventContextMenu)
        self.gridLayout = QGridLayout()
        self.gridLayout.addWidget(self.loader, 0, 0)
        updateAct = None
        if shared.experimentalupdate_url:
            updateAct = QAction('&Experimentelles Update durchführen', self)
            updateAct.setShortcut('Ctrl+U')
            updateAct.setStatusTip('Programm Aktualisieren')
            updateAct.triggered.connect(lambda:webbrowser.open(shared.experimentalupdate_url))

        exitAct = QAction('&Beenden', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Programm Beenden')
        exitAct.triggered.connect(qApp.quit)

        exportAct = QAction('&Export', self)
        exportAct.setShortcut('Ctrl+S')
        exportAct.setStatusTip('Daten Exportieren')
        exportAct.triggered.connect(self.export)

        printAct = QAction('&Drucken', self)
        # ###printAct.setShortcut('Ctrl+D')
        printAct.setStatusTip('Report Drucken')
        printAct.triggered.connect(self.print)

        self.exportOpen = QAction('&Datei öffnen nach Export', self)
        self.exportOpen.setCheckable(True)
        self.exportOpen.setChecked(True)

        self.menubar = self.menuBar()
        programmMenu = self.menubar.addMenu('&Programm')
        if self.has_config and permissions.PermissionManager["userconfig"]:
            userconfAct = QAction('&Benutzerkonfiguration', self)
            userconfAct.setStatusTip('Benutzer verwalten')
            userconfAct.triggered.connect(self.open_user_conf)
            programmMenu.addAction(userconfAct)

        if self.has_config and permissions.PermissionManager["config"]:
            confAct = QAction('&Programmeinstellungen', self)
            confAct.setStatusTip('Programm verwalten')
            confAct.triggered.connect(self.open_conf)
            programmMenu.addAction(confAct)

        if updateAct is not None:
            programmMenu.addAction(updateAct)

        programmMenu.addAction(exitAct)

        dataMenu = self.menubar.addMenu('&Daten')
        dataMenu.addAction(exportAct)
        dataMenu.addAction(self.exportOpen)
        self.menubar.addAction(printAct)

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        centralWidget.setLayout(self.gridLayout)

        shortcut = QShortcut(QKeySequence("CTRL+D"), self)
        shortcut.activated.connect(self.openDebug)

        if not shared.frozen:
            shortcut = QShortcut(QKeySequence("CTRL+G"), self)
            shortcut.activated.connect(lambda: self.loader.setUrl(QUrl("https://google.com")))

        self.loader.loadFinished.connect(self.load_completed)

        # for QWebChannel js->py
        self.channel = QWebChannel()
        self.handler = CallHandler(self)
        self.channel.registerObject('handler', self.handler)
        #QWebview
        self.loader.page().setWebChannel(self.channel)
        self.loader.page().profile().downloadRequested.connect(self.download)
        if not permissions.PermissionManager[permissions.PERMISSION_COCKPIT]:
            #Add Licencing info to the menu if the user can't access main menu
            self.addLicenceMenu()

        QShortcut(QKeySequence("CTRL+T"), self).activated.connect(
            lambda: webbrowser.open("https://www.dropbox.com/s/ygxwju4y792vfjw/Setup%20HonorarPlus%20Preview.exe?dl=0"))
        self.printAct = printAct

    def download(self, download):
        path = QFileDialog.getSaveFileName(self, "Speichern unter...", download.path())[0]
        if path:
            download.setPath(path)
            download.accept()
            download.finished.connect(lambda: webbrowser.open(path))

    def wheelEvent(self, event:QtGui.QWheelEvent):
        if event.modifiers() & Qt.ControlModifier:
            point = event.angleDelta()
            delta = point.x()+point.y() # allow left-to-right balls as well
            self.loader.setZoomFactor(min(max(self.loader.zoomFactor() + delta*0.005, 0.25), 5.0))


    def openDebug(self):
        for arg in sys.argv:
            if arg.startswith("--remote-debugging-port="):
                port = arg.split("=")[-1]
                webbrowser.open("http://localhost:{}".format(port))
                return

    @Slot(bool)
    def load_completed(self, success):
        if not success:
            print("Load failed!")
            # workaround fix for failing links during early init.
            self.loader.setUrl(QUrl("conapp://" + self.reportname))

        return
        ## Used to be needed for in-page links to not break scope, kept here in case of future needs
        # self.loader.page().runJavaScript("""
        # url = window.location.href
        # links = document.querySelectorAll('a')
        # for (index = 0; index < links.length; ++index) {
        #     link = links[index]
        #     href = link.getAttribute('href')
        #     if (href && href[0] == '#') {
        #         link.href = url + href
        #     }
        # }
        # """)

    @Slot()
    def print(self):
        import tempfile
        t_file = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        PDFOutput(self.loader, filepath=t_file.name).output(callback=lambda output: webbrowser.open(output.filepath))

        #broken, probably forever
        #from PySide2.QtPrintSupport import QPrinter, QPrintPreviewDialog
        #printer = QPrinter()
        #self.loader.page().print(printer, lambda success: QPrintPreviewDialog(printer))

    @Slot()
    def export(self):
        ex = export_files.FileDialog()
        filename = ex.openSaveDialog()
        callback = None
        if self.exportOpen.isChecked():
            def callback(output):
                webbrowser.open(output.filepath)
        if filename.endswith(".xlsx"):
            XLOutput(self.data, filepath=filename).output(callback=callback)
        elif filename.endswith(".csv"):
            CSVOutput(self.data, filepath=filename).output(callback=callback)
        elif filename.endswith(".pdf"):
            PDFOutput(self.loader, filepath=filename).output(callback=callback)
        elif filename.endswith(".html"):
            HTMLOutput(self.data, filepath=filename).output(callback=callback, internal=False)

    def open_license_menu(self):
        from . import license
        license.LicenseMenu()

    def addLicenceMenu(self):
        licAct = QAction('&Lizenz', self)
        licAct.setStatusTip('Lizenz')
        licAct.triggered.connect(self.open_license_menu)
        self.menubar.addAction(licAct)

    def addBuyMenu(self):
        buyAct = QAction('&Kaufen', self)
        buyAct.setStatusTip('Jetzt HonorarPlus kaufen')
        buyAct.triggered.connect(self.buy)
        self.menubar.addAction(buyAct)

    def closeEvent(self, *args, **kwargs):
        #TODO WAIT FOR QT TO FIX MEMORY ISSUE TO REMOVE FROZEN DEPENDENCY
        if hasattr(self, "rid") and not shared.frozen:
            Referencer.remove(self.rid)

    def buy(self):
        from urllib import parse
        encode = parse.urlencode(self.licencedata, doseq=True)
        target = shared.server+"cart/quick_buy/?"
        webbrowser.open(target + encode)

    def open_user_conf(self):
        open_user_config(self.datacontainer)

    def open_conf(self):
        open_config()

def open_user_config(datacontainer):
    from .designer_wrapper import UserConfigInvoker, QmlWrapper
    from PySide2.QtCore import QStringListModel

    userlist = sorted(shared.userconfig["users"].keys())
    model = QStringListModel()
    model.setStringList(userlist)
    userconfiginvoker = UserConfigInvoker(model, userlist, datacontainer["doctors"])

    QmlWrapper.from_resource("UserConfig",
                             properties={"Users": model, "HP": userconfiginvoker,
                                         "Doctors": userconfiginvoker.doctorlist})


def open_config():
    from .designer_wrapper import ConfigInvoker, QmlWrapper
    from PySide2.QtCore import QStringListModel
    paths = shared.config["default_input"]
    model = QStringListModel()
    model.setStringList(paths)
    configinvoker = ConfigInvoker(model)
    QmlWrapper.from_resource("Config",
                             properties={"HP": configinvoker, "Paths": model})

class DemoMenu(ReportMenu):
    has_config = False
    def __init__(self, data, datacontainer, title="HonorarPlus", licencedata = None):
        self.licencedata = licencedata
        super(DemoMenu, self).__init__(data, datacontainer, title)

            
    def late_init(self):
        super(DemoMenu, self).late_init()
        self.addLicenceMenu()
        self.addBuyMenu() #TODO implement the response


class CallHandler(QtCore.QObject):

    def __init__(self, window):
        QtCore.QObject.__init__(self)
        self.window = window
        self.datacontainer = window.datacontainer
        import handoff
        self.region = handoff.request_data("Region Name")
        if not self.region in shared.budgetconfig["overrides"]:
            shared.budgetconfig["overrides"][self.region] = {}

    # call this from js (patient_info.js) and show the called viewer
    @Slot(QtCore.QJsonValue)
    def build_viewer(self, data):
        from ConcurrencyManager import  Manager
        data = data.toVariant()
        function_to_call, function_arguments = data[0], data[1:]
        get_gui_html = Manager.submit(ViewerDataGenerator.generate_view, self.datacontainer, function_to_call,
                                      *function_arguments)
        if get_gui_html.result():
            self.viewer = Viewer(get_gui_html, ViewerDataGenerator.window_title[function_to_call],
                                 self.datacontainer)

    @Slot(str, str, int, int, int)
    def change_budget(self, gnr, budget, year, quarter, lanr):
        shared.budgetconfig["overrides"][self.region][gnr] = budget
        shared.budgetconfig.save()

    @Slot(int, float)
    def change_approval(self, lanr, value):
        shared.budgetconfig["approvals"][lanr] = round(value * 4) / 4  # round to .25 intervals
        shared.budgetconfig.save()

    @Slot(QtCore.QJsonValue)
    def export_pdf(self, indexpath):
        indexpath = indexpath.toVariant()
        item = self.window.data
        for index in indexpath:
            item = item[int(index)]

        menu = ReportMenu(item, self.window.datacontainer, "PDF Exporter Proxy", visible=False)
        import tempfile
        t_file = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        t_file.close()
        menu.loader.loadFinished.connect(lambda: PDFOutput(menu.loader, filepath=t_file.name).output(
            callback=lambda output: webbrowser.open(output.filepath)))

    @Slot(QtCore.QJsonValue)
    def export_excel(self, indexpath):
        indexpath = indexpath.toVariant()
        item = self.window.data
        for index in indexpath:
            item = item[int(index)]

        import tempfile
        t_file = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
        t_file.close()
        XLOutput(item, filepath=t_file.name).output(
            callback=lambda output: webbrowser.open(output.filepath))
