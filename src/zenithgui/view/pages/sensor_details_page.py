from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import QTimer

from zenithgui.view.components.graph import Graph
from zenithgui.config import config

class SensorDetailsPage(QDialog):
    def __init__(self, parent, name, keys):
        super().__init__()

        self.parent_page = parent
        self.graph_keys = keys
        self.name = name

        self.graphs: dict[str, Graph] = {}
        self.update_graphs_timer = QTimer()

        self._create_widgets()
        self._create_layouts()
        self._connect_signals()
        self._apply_styles()

    def _create_widgets(self):
        self.title = QLabel(self.name)
        self.graph_grid = QGridLayout()
        
    def _create_layouts(self):
        self.content = QVBoxLayout()
        self.content.addWidget(self.title)
        self.content.addLayout(self.graph_grid)

        self.parent_page.create_graphs(self.graph_keys, self.graphs, self.graph_grid)
        self.update_graphs_timer.start(config.GRAPH_UPDATE_MS_TIME)

        self.setLayout(self.content)

    def _auto_update_graphs(self):
        self.parent_page.update_graphs(self.graphs)

    def _connect_signals(self):
        self.update_graphs_timer.timeout.connect(self._auto_update_graphs)

    def _apply_styles(self):
            palette = self.palette()
            palette.setColor(QPalette.ColorRole.Window, QColor("#1e1e1e"))
            self.setPalette(palette)