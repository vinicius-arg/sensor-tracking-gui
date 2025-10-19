from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QCheckBox, QLabel
from PyQt5.QtCore import pyqtSignal, QTimer

from zenithgui.view.components.graph import Graph
from zenithgui.view.components.file_handler import FileHandler
from zenithgui.config import config

class Dashboard(QWidget):
    RECORD_SAMPLES_TEXT = "Record samples"
    START_TRACKING_TEXT = "Start tracking"
    PAUSE_TRACKING_TEXT = "Pause"
    STOP_TRACKING_TEXT = "Stop"

    start_tracking = pyqtSignal()
    pause_tracking = pyqtSignal()
    stop_tracking = pyqtSignal()

    def __init__(self, parent):
        super().__init__()

        self.parent_page = parent
        self.graphs: dict[str, Graph] = {}

        self.sensors_to_plot = config.TRACKABLE_DATA
        self.sensors_alias = config.ROCKET_DATA_ALIAS
        
        self.full_history: dict = {}
        self.update_graphs_timer = QTimer()

        self._create_widgets()
        self._create_layouts()
        self._connect_signals()
        self._apply_styles()

    def _create_widgets(self):
        self.start_btn = QPushButton(self.START_TRACKING_TEXT)
        self.pause_btn = QPushButton(self.PAUSE_TRACKING_TEXT)
        self.stop_btn = QPushButton(self.STOP_TRACKING_TEXT)
        self.checkbox = QCheckBox(self.RECORD_SAMPLES_TEXT)

        self.file_handler = FileHandler(rec=self.checkbox)

        self.notification_label = QLabel()

    def _create_layouts(self):
        self.content = QVBoxLayout()
        self.control_bar = QHBoxLayout()
        self.graph_grid = QGridLayout()

        self.control_bar.addWidget(self.start_btn)
        self.control_bar.addWidget(self.pause_btn)
        self.control_bar.addWidget(self.stop_btn)
        self.control_bar.addWidget(self.checkbox)
        self.control_bar.addWidget(self.file_handler)

        self.parent_page.create_graphs(config.TRACKABLE_DATA, self.graphs, self.graph_grid)
        self.update_graphs_timer.start(config.GRAPH_UPDATE_MS_TIME)

        self.content.addLayout(self.control_bar, stretch=1)
        self.content.addLayout(self.graph_grid, stretch=5)

        self.content.addWidget(self.notification_label)

        self.setLayout(self.content)

    def _connect_signals(self):
        self.update_graphs_timer.timeout.connect(self._auto_update_graphs)
        self.start_btn.pressed.connect(self.start_tracking.emit)
        self.pause_btn.pressed.connect(self.pause_tracking.emit)
        self.stop_btn.pressed.connect(self.stop_tracking.emit)

    def _auto_update_graphs(self):
        self.parent_page.update_graphs(self.graphs)

    def _apply_styles(self):
        self.start_btn.setProperty("class", "menuBtn")
        self.pause_btn.setProperty("class", "menuBtn")
        self.stop_btn.setProperty("class", "menuBtn")
        self.file_handler.setProperty("class", "input")
        self.checkbox.setProperty("class", "input")
        
        self.start_btn.setObjectName("StartBtn")
        self.stop_btn.setObjectName("StopBtn")
        self.notification_label.setObjectName("Info")

        self.graph_grid.setSpacing(15)
