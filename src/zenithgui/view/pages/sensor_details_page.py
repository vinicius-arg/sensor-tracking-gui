from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import QTimer

from zenithgui.config import Config
from zenithgui.util import ThemeUtils
from zenithgui.view.components.graph import Graph

class SensorDetailsPage(QDialog):
    def __init__(self, parent, name, keys):
        super().__init__()

        self.parent_page = parent
        self.graph_keys = keys
        self.name = name

        self.graphs: dict[str, Graph] = {}
        self.update_graphs_timer = QTimer()

        self.__create_widgets()
        self.__create_layouts()
        self.__connect_signals()
        self.__apply_styles()


    def __create_widgets(self):
        self.title = QLabel(self.name)
        self.graph_grid = QGridLayout()
        

    def __create_layouts(self):
        self.content = QVBoxLayout()
        self.content.addWidget(self.title)
        self.content.addLayout(self.graph_grid)

        self.parent_page.create_graphs(self.graph_keys, self.graphs, self.graph_grid)
        self.update_graphs_timer.start(Config.UI_UPDATE_MS_TIME)

        self.setLayout(self.content)


    def __update_graphs(self):
        self.parent_page.update_graphs(self.graphs)


    def __connect_signals(self):
        self.update_graphs_timer.timeout.connect(self.__update_graphs)


    def __apply_styles(self):
        ThemeUtils.setup_and__apply_stylesheets(self)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#1e1e1e"))
        self.setPalette(palette)

        self.title.setProperty("class", "title")

