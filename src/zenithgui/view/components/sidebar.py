from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QPushButton, QVBoxLayout
from zenithgui.config import config

class SideBar(QFrame):
    def __init__(self, page, sensors: list):
        super().__init__()

        self.page = page
        self.sensors = sensors

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

        self.sensors_buttons = []
        for sensor in ["All sensors", *self.sensors.keys()]:
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
            button.clicked.connect(self.page.show_sensor_details)

    def _apply_styles(self):
        self.subtitle.setWordWrap(True)
        self.content.setContentsMargins(15, 15, 15, 15)
        self.setMinimumWidth(200)

        self.app_name.setObjectName("AppTitle")
        self.subtitle.setObjectName("AppSubTitle")
        self.setObjectName("SideBar")