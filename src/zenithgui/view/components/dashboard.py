from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QCheckBox, QLabel
from PyQt5.QtCore import pyqtSignal

from zenithgui.view.components.graph import Graph
from zenithgui.view.components.file_handler import FileHandler
from zenithgui.config import config

class Dashboard(QWidget):
    START_STR = "Start tracking"
    PAUSE_STR = "Pause"
    STOP_STR = "Stop"
    RECORD_STR = "Record samples"
    GRAPH_GRID_COLUMNS = 3

    start_tracking = pyqtSignal()
    pause_tracking = pyqtSignal()
    stop_tracking = pyqtSignal()

    def __init__(self, page):
        super().__init__()

        self.page = page
        self.graphs: dict[str, Graph] = {}
        self.full_history: dict[str, list] = {} #TODO Rastrear dados se checkbox is on, salvar qd stop
        self.sensors_to_plot = config.TRACKABLE_DATA
        self.sensors_alias = config.DATA_ALIAS

        self._create_widgets()
        self._create_layouts()
        self._connect_signals()
        self._apply_styles()

        self.setLayout(self.content)

    def _create_widgets(self):
        self.start_btn = QPushButton(self.START_STR)
        self.pause_btn = QPushButton(self.PAUSE_STR)
        self.stop_btn = QPushButton(self.STOP_STR)
        self.checkbox = QCheckBox(self.RECORD_STR)
        self.file_handler = FileHandler(self.checkbox)

        self.info = QLabel("*Information label") #TODO Notificações 

    def _create_layouts(self):
        self.content = QVBoxLayout()
        self.control_bar = QHBoxLayout()
        self.graph_grid = QGridLayout()

        self.control_bar.addWidget(self.start_btn)
        self.control_bar.addWidget(self.pause_btn)
        self.control_bar.addWidget(self.stop_btn)
        self.control_bar.addWidget(self.checkbox)
        self.control_bar.addWidget(self.file_handler)
        self._create_graphs()

        self.content.addLayout(self.control_bar, stretch=1)
        self.content.addLayout(self.graph_grid, stretch=5)

        self.content.addWidget(self.info)

    def _connect_signals(self):
        self.start_btn.pressed.connect(self.start_tracking.emit)
        self.pause_btn.pressed.connect(self.pause_tracking.emit)
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
        self.pause_btn.setProperty("class", "menuBtn")
        self.stop_btn.setProperty("class", "menuBtn")
        self.file_handler.setProperty("class", "input")
        self.checkbox.setProperty("class", "input")
        
        self.start_btn.setObjectName("StartBtn")
        self.stop_btn.setObjectName("StopBtn")
        self.info.setObjectName("Info")

        self.graph_grid.setSpacing(15)

    def _get_sensor_name(self, raw_name):
        for key, value in self.sensors_alias.items():
            if raw_name in key:
                return value