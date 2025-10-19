from PyQt5.QtWidgets import QLabel, QFrame, QPushButton, QVBoxLayout
from functools import partial

from zenithgui.view.pages.sensor_details_page import SensorDetailsPage
from zenithgui.config import config

class SideBar(QFrame):
    def __init__(self, parent):
        super().__init__()

        self.parent_page = parent
        self.sensors = config.ROCKET_DATA_MAP

        self._create_widgets()
        self._create_layouts()
        self._connect_signals()
        self._apply_styles()

        self.setLayout(self.content)

    def _create_widgets(self):
        self.app_name = QLabel(config.APP_NAME)
        self.subtitle = QLabel(config.APP_SUBTITLE)
        
        self.horizontal_bar = QFrame()
        self.horizontal_bar.setFrameShape(QFrame.HLine)
        self.horizontal_bar.setFrameShadow(QFrame.Sunken)

        self.sensors_buttons: list[QPushButton] = []
        for sensor in self.sensors.keys():
            button = QPushButton(sensor)
            button.setProperty("class", "sidebarButton")
            self.sensors_buttons.append(button)

    def _create_layouts(self):
        self.content = QVBoxLayout(self)

        self.content.addWidget(self.app_name)
        self.content.addWidget(self.subtitle)
        self.content.addWidget(self.horizontal_bar)
        self.content.addStretch()

        for sidebar_btn in self.sensors_buttons:
            self.content.addWidget(sidebar_btn)

    def _connect_signals(self):
        for button in self.sensors_buttons:
            button.clicked.connect(partial(self._show_sensor_details, button.text()))

    def _apply_styles(self):
        self.subtitle.setWordWrap(True)
        self.content.setContentsMargins(15, 15, 15, 15)
        self.setMinimumWidth(200)

        self.app_name.setObjectName("AppTitle")
        self.subtitle.setObjectName("AppSubTitle")
        self.setObjectName("SideBar")
        
    def _show_sensor_details(self, name):
        graph_keys: list = self.sensors[name]

        dlg = SensorDetailsPage(self.parent_page, name, graph_keys)
        dlg.exec_()