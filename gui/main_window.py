from PyQt5 import QtWidgets
from gui.overview_tab import OverviewTab


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, curves, parent=None):
        super().__init__(parent)

        self.setWindowTitle("VAnalyzer 9000")
        self.resize(1400, 800)

        self.tabs = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tabs)

        self.overview_tab = OverviewTab(curves)
        self.tabs.addTab(self.overview_tab, "Overview")
