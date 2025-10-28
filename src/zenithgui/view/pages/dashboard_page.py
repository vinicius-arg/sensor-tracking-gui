from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from zenithgui.view.components.sidebar import SideBar
from zenithgui.view.components.dashboard import Dashboard
from zenithgui.view.components.graph import Graph

from zenithgui.config import Config
from zenithgui.model.telemetry import StatusFlags
from zenithgui.util import FormatUtils

class DashboardPage(QWidget):
    GRAPH_GRID_COLUMNS = 3

    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)

        self.status = {}

        self._load_sensors()
        self._create_widgets()
        self._create_layouts()
        self._promote_signals()
        self._promote_buttons()
        self._apply_styles()

        self.full_history = self.dashboard.full_history
        self.window_data_processed = int(0)
        self.rocket_data = {}

        self.notification_label = self.dashboard.notification_label
    
    def _load_sensors(self):
        self.sensors = Config.ROCKET_DATA_MAP
        self.sensors_alias = Config.ROCKET_DATA_ALIAS

    def _create_widgets(self):
        self.dashboard = Dashboard(parent=self, status=self.status)
        self.sidebar = SideBar(parent=self)
        
    def _create_layouts(self):
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.sidebar, stretch=1)
        self.main_layout.addWidget(self.dashboard, stretch=4)

        self.setLayout(self.main_layout)  

    def _apply_styles(self):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#1e1e1e"))
        self.setPalette(palette)
        
    def _promote_signals(self):
        self.stop_tracking = self.dashboard.stop_tracking
        self.pause_tracking = self.dashboard.pause_tracking
        self.start_tracking = self.dashboard.start_tracking

    def _promote_buttons(self):
        self.start_btn = self.dashboard.start_btn
        self.pause_btn = self.dashboard.pause_btn
        self.stop_btn = self.dashboard.stop_btn
        self.checkbox = self.dashboard.checkbox
        self.file_handler = self.dashboard.file_handler

    def create_graphs(self, sensors, graph_list, graph_grid):
        sensors_to_plot = [e for e in sensors if e != "status"]
        for index, name in enumerate(sensors_to_plot, start=0):
            fancy_name = FormatUtils.get_fancy_name(name, Config.ROCKET_DATA_ALIAS)
            g = Graph(fancy_name).get_graph()
            row, col = divmod(index, self.GRAPH_GRID_COLUMNS)
            graph_grid.addWidget(g.frame, row, col)
            
            graph_list[name] = g

    def update_data(self, rocket_data: dict):
        self.rocket_data = rocket_data
        
    def update_graphs(self, graph_list):
        for name, data in self.rocket_data.items():
            if name == "status":
                self._update_status(data.flags)
            if name in graph_list:
                g = graph_list[name]         
                g.curve.setData(data)
                self._update_last_value(graph=g, value=data[-1])
                
                if self.checkbox.isChecked():
                    self._save_data(self.rocket_data)

    def _update_status(self, data):
        for field, _, _ in StatusFlags._fields_:
            if field != "reserved":
                self.status[field] = getattr(data, field)

    def _update_last_value(self, graph, value):
        graph.current.setText(f"{value:.2f}")

    def _save_data(self, rocket_data):
        self.window_data_processed += 1

        if self._data_window_snapshotted():
            self._save_data_to_history(rocket_data)
            self.window_data_processed = 0

    def _data_window_snapshotted(self):
        return self.window_data_processed == Config.DATA_WINDOW_LENGTH
    
    def _save_data_to_history(self, rocket_data: dict):
        for name, data in rocket_data.items():
            if name in self.dashboard.graphs:
                self.full_history.setdefault(name, [])
                self.full_history[name].extend(data)

    def update_page(self):
        self.update_graphs(self.dashboard.graphs)
        self.dashboard.update_component()