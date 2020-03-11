import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from nodeeditor.utils import loadStylesheets
from nodeeditor.node_editor_window import NodeEditorWindow
from rapidmac_sub_window import RAPMACSubWindow
from rapidmac_drag_listbox import QDMDragListbox
from nodeeditor.utils import dumpException, pp
from rapidmac_conf import *

# images for the dark skin
# import qss.nodeeditor_dark_resources

DEBUG = False


class RapidMACWindow(NodeEditorWindow):
    def initUI(self):
        self.name_company = 'IIST'
        self.name_product = 'RapidMAC prototyper'

        self.stylesheet_filename = os.path.join(os.path.dirname(__file__), "qss/nodeeditor.qss")
        loadStylesheets(
            os.path.join(os.path.dirname(__file__), "qss/nodeeditor-dark.qss"),
            self.stylesheet_filename
        )

        self.empty_icon = QIcon(".")

        if DEBUG:
            print("Registered nodes:")
            pp(RAPMAC_NODES)


        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setViewMode(QMdiArea.TabbedView)
        self.mdiArea.setDocumentMode(True)
        self.mdiArea.setTabsClosable(True)
        self.mdiArea.setTabsMovable(True)
        self.setCentralWidget(self.mdiArea)

        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)

        self.createNodesDock()

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()

        self.readSettings()

        self.setWindowTitle("RapidMAC prototyper")

    def closeEvent(self, event):
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            event.ignore()
        else:
            self.writeSettings()
            event.accept()


    def createActions(self):
        super().createActions()

        self.actClose = QAction("Cl&ose", self, statusTip="Close the active window", triggered=self.mdiArea.closeActiveSubWindow)
        self.actCloseAll = QAction("Close &All", self, statusTip="Close all the windows", triggered=self.mdiArea.closeAllSubWindows)
        self.actTile = QAction("&Tile", self, statusTip="Tile the windows", triggered=self.mdiArea.tileSubWindows)
        self.actCascade = QAction("&Cascade", self, statusTip="Cascade the windows", triggered=self.mdiArea.cascadeSubWindows)
        self.actNext = QAction("Ne&xt", self, shortcut=QKeySequence.NextChild, statusTip="Move the focus to the next window", triggered=self.mdiArea.activateNextSubWindow)
        self.actPrevious = QAction("Pre&vious", self, shortcut=QKeySequence.PreviousChild, statusTip="Move the focus to the previous window", triggered=self.mdiArea.activatePreviousSubWindow)

        self.actSeparator = QAction(self)
        self.actSeparator.setSeparator(True)

        self.actAbout = QAction("&About", self, statusTip="Show the application's About box", triggered=self.about)

        self.actGenerate = QAction("&Generate", self, statusTip = "Generate code for Contiki", triggered = self.generate_all)
        self.actGenerateHeader = QAction("Generate Header", self, statusTip = "Generate header file for Contiki", triggered = self.generate_header)
        self.actGenerateMACDriver = QAction("Generate MAC Driver", self, statusTip = "Generate MAC driver file for Contiki", triggered = self.generate_macdriver)

    def getCurrentNodeEditorWidget(self):
        """ we're returning NodeEditorWidget here... """
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    def onFileNew(self):
        try:
            subwnd = self.createMdiChild()
            subwnd.widget().fileNew()
            subwnd.show()
        except Exception as e: dumpException(e)

    def onFileOpen(self):
        fnames, filter = QFileDialog.getOpenFileNames(self, 'Open graph from file')

        try:
            for fname in fnames:
                if fname:
                    existing = self.findMdiChild(fname)
                    if existing:
                        self.mdiArea.setActiveSubWindow(existing)
                    else:
                        # we need to create new subWindow and open the file
                        nodeeditor = RAPMACSubWindow()
                        if nodeeditor.fileLoad(fname):
                            self.statusBar().showMessage("File %s loaded" % fname, 5000)
                            nodeeditor.setTitle()
                            subwnd = self.createMdiChild(nodeeditor)
                            subwnd.show()
                        else:
                            nodeeditor.close()
        except Exception as e: dumpException(e)

    def generate_all(self):
        self.generate_header()
        self.generate_macdriver()

    def generate_header(self):
        pass

    def generate_macdriver(self):
        nodes_in_scene = self.mdiArea.currentSubWindow().widget().scene.nodes
        starter_nodes = []
        for node in nodes_in_scene:
            if node.node_type == NODE_TYPE_START:
                starter_nodes.append(node)

        for node in starter_nodes:
            node.generate_code()

    def about(self):
        QMessageBox.about(self, "RapidMAC prototyper",
                "For rapid prototyping of multiple access control (MAC) protocols"
                "for the Contiki operating system\n\n"
                "Developed by:\n"
                "Sherine Padma\nVineeth B. S.\nGovind A. M.\nReuben\n\n"
                "Funded by an IIST FASTTRACK project")

    def createMenus(self):
        super().createMenus()

        self.contikiMenu = self.menuBar().addMenu("&Contiki Code")
        self.updateContikiMenu()
        self.contikiMenu.aboutToShow.connect(self.updateContikiMenu)

        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.actAbout)

        self.editMenu.aboutToShow.connect(self.updateEditMenu)

    def updateMenus(self):
        # print("update Menus")
        active = self.getCurrentNodeEditorWidget()
        hasMdiChild = (active is not None)

        self.actSave.setEnabled(hasMdiChild)
        self.actSaveAs.setEnabled(hasMdiChild)
        self.actClose.setEnabled(hasMdiChild)
        self.actCloseAll.setEnabled(hasMdiChild)
        self.actTile.setEnabled(hasMdiChild)
        self.actCascade.setEnabled(hasMdiChild)
        self.actNext.setEnabled(hasMdiChild)
        self.actPrevious.setEnabled(hasMdiChild)
        self.actSeparator.setVisible(hasMdiChild)

        self.actGenerate.setEnabled(hasMdiChild)
        self.actGenerateHeader.setEnabled(hasMdiChild)
        self.actGenerateMACDriver.setEnabled(hasMdiChild)

        self.updateEditMenu()

    def updateEditMenu(self):
        try:
            # print("update Edit Menu")
            active = self.getCurrentNodeEditorWidget()
            hasMdiChild = (active is not None)

            self.actPaste.setEnabled(hasMdiChild)

            self.actCut.setEnabled(hasMdiChild and active.hasSelectedItems())
            self.actCopy.setEnabled(hasMdiChild and active.hasSelectedItems())
            self.actDelete.setEnabled(hasMdiChild and active.hasSelectedItems())

            self.actUndo.setEnabled(hasMdiChild and active.canUndo())
            self.actRedo.setEnabled(hasMdiChild and active.canRedo())
        except Exception as e: dumpException(e)

    def updateContikiMenu(self):
        self.contikiMenu.clear()

        self.contikiMenu.addAction(self.actGenerate)
        self.contikiMenu.addAction(self.actGenerateHeader)
        self.contikiMenu.addAction(self.actGenerateMACDriver)
        

    def updateWindowMenu(self):
        self.windowMenu.clear()

        toolbar_nodes = self.windowMenu.addAction("Toolbars")
        toolbar_nodes.setCheckable(True)
        toolbar_nodes.triggered.connect(self.onWindowNodesToolbar)

        toolbar_nodes.setChecked(self.nodesDock_MAC_NODES.isVisible())
        toolbar_nodes.setChecked(self.nodesDock_CSRC_NODES.isVisible())


        self.windowMenu.addSeparator()

        self.windowMenu.addAction(self.actClose)
        self.windowMenu.addAction(self.actCloseAll)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actTile)
        self.windowMenu.addAction(self.actCascade)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actNext)
        self.windowMenu.addAction(self.actPrevious)
        self.windowMenu.addAction(self.actSeparator)

        windows = self.mdiArea.subWindowList()
        self.actSeparator.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, child.getUserFriendlyFilename())
            if i < 9:
                text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.getCurrentNodeEditorWidget())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)

    def onWindowNodesToolbar(self):
        if self.nodesDock_MAC_NODES.isVisible() or self.nodesDock_CSRC_NODES.isVisible():
            self.nodesDock_MAC_NODES.hide()
            self.nodesDock_CSRC_NODES.hide()
        else:
            self.nodesDock_MAC_NODES.show()
            self.nodesDock_CSRC_NODES.show()

    def createToolBars(self):
        pass

    def createNodesDock(self):
        self.nodesListWidget_MAC_NODES = QDMDragListbox(OP_MAC_NODES_START)
        self.nodesDock_MAC_NODES = QDockWidget("Contiki MAC driver functions")
        self.nodesDock_MAC_NODES.setWidget(self.nodesListWidget_MAC_NODES)
        self.nodesDock_MAC_NODES.setFloating(False)

        self.nodesListWidget_CSRC_NODES = QDMDragListbox(OP_CSRC_NODES_START)
        self.nodesDock_CSRC_NODES = QDockWidget("C programming")
        self.nodesDock_CSRC_NODES.setWidget(self.nodesListWidget_CSRC_NODES)
        self.nodesDock_CSRC_NODES.setFloating(False)

        self.addDockWidget(Qt.RightDockWidgetArea, self.nodesDock_MAC_NODES)
        self.addDockWidget(Qt.RightDockWidgetArea, self.nodesDock_CSRC_NODES)


    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createMdiChild(self, child_widget=None):
        nodeeditor = child_widget if child_widget is not None else RAPMACSubWindow()
        subwnd = self.mdiArea.addSubWindow(nodeeditor)
        subwnd.setWindowIcon(self.empty_icon)
        # nodeeditor.scene.addItemSelectedListener(self.updateEditMenu)
        # nodeeditor.scene.addItemsDeselectedListener(self.updateEditMenu)
        nodeeditor.scene.history.addHistoryModifiedListener(self.updateEditMenu)
        nodeeditor.addCloseEventListener(self.onSubWndClose)
        return subwnd

    def onSubWndClose(self, widget, event):
        existing = self.findMdiChild(widget.filename)
        self.mdiArea.setActiveSubWindow(existing)

        if self.maybeSave():
            event.accept()
        else:
            event.ignore()


    def findMdiChild(self, filename):
        for window in self.mdiArea.subWindowList():
            if window.widget().filename == filename:
                return window
        return None


    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)