from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QPushButton, QVBoxLayout
from zenithgui.config import config

class SideBar(QWidget):
    def __init__(self, page, sensors: list):
        super().__init__()

        self.page = page
        self.sensors = sensors

        self._create_widgets()
        self._create_layouts()
        self._connect_signals()
        self._apply_styles()

    def _create_widgets(self):
        self.container = QFrame()

        self.app_name = QLabel(config.APP_NAME)
        self.subtitle = QLabel(config.APP_SUBTITLE)
        
        self.horizontal_bar = QFrame()
        self.horizontal_bar.setFrameShape(QFrame.HLine)
        self.horizontal_bar.setFrameShadow(QFrame.Sunken)

        self.sensors_buttons = []
        for sensor in ["All sensors", *self.sensors.keys()]:
            button = QPushButton(sensor)
            button.setProperty("class", "sidebarButton")
            self.sensors_buttons.append(button)

    def _create_layouts(self):
        self.container_layout = QVBoxLayout(self.container)

        self.container_layout.addWidget(self.app_name)
        self.container_layout.addWidget(self.subtitle)
        self.container_layout.addWidget(self.horizontal_bar)
        self.container_layout.addStretch()

        for sidebar_btn in self.sensors_buttons:
            self.container_layout.addWidget(sidebar_btn)

    def _connect_signals(self):
        for button in self.sensors_buttons:
            button.clicked.connect(self.page.show_sensor_details)

    def _apply_styles(self):
        self.subtitle.setWordWrap(True)
        self.container_layout.setContentsMargins(15, 15, 15, 15)

        self.app_name.setObjectName("AppTitle")
        self.subtitle.setObjectName("AppSubTitle")
        self.container.setObjectName("SideBar")