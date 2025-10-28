from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QCheckBox
from PyQt5.QtCore import Qt, pyqtSignal, QTimer

from zenithgui.config import Config

class ConnectionPage(QWidget):
    connection_requested = pyqtSignal(str, int, bool)
    available_ports_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#1e1e1e"))
        self.setPalette(palette)

        self.__create_widgets()
        self.__create_layouts()
        self.__connect_signals()

        self.__search_for_ports()


    def __create_widgets(self):
        # Widgets do lado esquerdo
        self.btn_label = QLabel("Connect to LoRa")
        self.btn_label.setProperty("class", "title")
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.setObjectName("LoRaConnectButton")

        # Widgets do lado direito
        self.port_label = QLabel("Connection's port")
        self.port_label.setProperty("class", "text")
        self.port_selector = QComboBox()
        self.port_selector.setProperty("class", "input")
        
        self.baudrate_label = QLabel("Connection's baud rate")
        self.baudrate_label.setProperty("class", "text")
        self.baudrate_selector = QComboBox()
        self.baudrate_selector.setProperty("class", "input")
        self.baudrate_selector.addItems(Config.SUPPORTED_BAUDRATES)
        self.baudrate_selector.setCurrentText(Config.DEFAULT_BAUDRATE)

        self.force_connection = QCheckBox("Force connection")
        self.force_connection.setProperty("class", "text")


    def __create_layouts(self):
        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignCenter)
        left_layout.setContentsMargins(20, 20, 20, 20)
        left_layout.addWidget(self.btn_label)
        left_layout.addWidget(self.connect_btn)

        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignCenter)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.addWidget(self.port_label)
        right_layout.addWidget(self.port_selector)
        right_layout.addWidget(self.baudrate_label)
        right_layout.addWidget(self.baudrate_selector)
        right_layout.addWidget(self.force_connection)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, stretch=1)
        main_layout.addLayout(right_layout, stretch=1)

        self.setLayout(main_layout)


    def __connect_signals(self):
        self.connect_btn.clicked.connect(self.__on_connection_request)
        self.port_selector.currentIndexChanged.connect(self.__on_port_selection)
        self.baudrate_selector.currentIndexChanged.connect(self.__on_baudrate_selection)


    def __search_for_ports(self):
        self.available_ports_requested.emit()
        if self.port_selector.count() == 0:
            QTimer.singleShot(3, self.__search_for_ports)


    def __on_connection_request(self):
        self.lora_port = self.port_selector.currentText()
        self.lora_baudrate = int(self.baudrate_selector.currentText())

        self.connection_requested.emit(
            self.lora_port, 
            self.lora_baudrate, 
            self.force_connection.isChecked())


    def __on_port_selection(self):
        self.lora_port = self.port_selector.currentText()


    def __on_baudrate_selection(self):
        self.lora_baudrate = int(self.baudrate_selector.currentText())
