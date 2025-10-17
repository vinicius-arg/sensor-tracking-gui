from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel

from zenithgui.view.components.sidebar import SideBar
from zenithgui.view.components.dashboard import Dashboard

from zenithgui import config

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)

        self._load_sensors()
        self._create_widgets()
        self._create_layouts()
        self._promote_signals()
        self._promote_buttons()
        self._apply_styles()

        self.full_history = self.dashboard.full_history
        self.window_data_processed = int(0)
    
    def _load_sensors(self):
        self.sensors = config.DATA_MAP

    def _create_widgets(self):
        self.sidebar = SideBar(self, self.sensors)
        self.dashboard = Dashboard(self)

        self.info = self.dashboard.info
        
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

    def update_data(self, rocket_data: dict):
        for name, data in rocket_data.items():
            if name in self.dashboard.graphs:
                g = self.dashboard.graphs[name]         
                g.curve.setData(data)
                # Atualização de último valor
                last_value = data[-1]
                g.current.setText(f"{last_value:.2f}")

                if self.checkbox.isChecked():
                    self._save_data(rocket_data)

    def _save_data(self, rocket_data):
        self.window_data_processed += 1

        if self._data_window_snapshotted():
            self._save_data_to_history(rocket_data)
            self.window_data_processed = 0

    def _data_window_snapshotted(self):
        return self.window_data_processed == config.DATA_WINDOW_LENGTH
    
    def _save_data_to_history(self, rocket_data: dict):
        for name, data in rocket_data.items():
            if name in self.dashboard.graphs:
                self.full_history.setdefault(name, [])
                self.full_history[name].extend(data)

    def show_sensor_details(self):
        ...