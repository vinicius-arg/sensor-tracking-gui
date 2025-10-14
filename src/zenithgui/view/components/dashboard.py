from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QCheckBox, QLineEdit
from PyQt5.QtCore import pyqtSignal

from zenithgui.view.components.graph import Graph
from zenithgui.config import config

class Dashboard(QWidget):
    START_STR = "Start tracking"
    STOP_STR = "Stop"
    SAVE_STR = "~/path/to/recordings"
    RECORD_STR = "Record samples"
    GRAPH_GRID_COLUMNS = 3

    stop_tracking = pyqtSignal()

    def __init__(self, page):
        super().__init__()

        self.page = page
        self.graphs: dict[str, Graph] = {}
        self.sensors_to_plot = config.TRACKABLE_DATA
        self.sensors_alias = config.DATA_ALIAS

        self._create_widgets()
        self._create_layouts()
        self._connect_signals()
        self._apply_styles()

    def _create_widgets(self):
        self.start_btn = QPushButton(self.START_STR)
        self.stop_btn = QPushButton(self.STOP_STR)
        self.record_checkbox = QCheckBox(self.RECORD_STR)
        self.save_path = QLineEdit(self.SAVE_STR)

    def _create_layouts(self):
        self.main_content = QVBoxLayout()
        self.control_bar = QHBoxLayout()
        self.graph_grid = QGridLayout()

        self.control_bar.addWidget(self.start_btn)
        self.control_bar.addWidget(self.stop_btn)
        self.control_bar.addWidget(self.record_checkbox)
        self.control_bar.addWidget(self.save_path)
        self._create_graphs()

        self.main_content.addLayout(self.control_bar, stretch=1)
        self.main_content.addLayout(self.graph_grid, stretch=5)

    def _connect_signals(self):
        self.stop_btn.pressed.connect(self.stop_tracking.emit)

    def _create_graphs(self):
        for name in self.sensors_to_plot:
            fancy_name = self._get_sensor_name(name)
            g = Graph(fancy_name).get_graph()
            row, col = divmod(g._id, self.GRAPH_GRID_COLUMNS)
            self.graph_grid.addWidget(g.frame, row, col)
            
            self.graphs[name] = g

    def _apply_styles(self):
        self.start_btn.setProperty("class", "menuBtn")
        self.stop_btn.setProperty("class", "menuBtn")
        self.save_path.setProperty("class", "input")
        self.graph_grid.setSpacing(15)

    def _get_sensor_name(self, raw_name):
        for key, value in self.sensors_alias.items():
            if raw_name in key:
                return value