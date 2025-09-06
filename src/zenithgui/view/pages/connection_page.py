from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt

class ConnectionPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#1e1e1e"))
        self.setPalette(palette)

        self._create_widgets()
        self._create_layouts()
        self._connect_signals()


    def _create_widgets(self):
        # Widgets do lado esquerdo
        self.btn_label = QLabel("Connect to LoRa")
        self.btn_label.setProperty("class", "title")
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.setObjectName("LoRaConnectButton")

        # Widgets do lado direito
        self.label = QLabel("Adicionar botões de sensores...")
        ...

    def _create_layouts(self):
        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignCenter)
        left_layout.setContentsMargins(20, 20, 20, 20)
        left_layout.addWidget(self.btn_label)
        left_layout.addWidget(self.connect_btn)

        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignCenter)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.addWidget(self.label)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, stretch=1)
        main_layout.addLayout(right_layout, stretch=2)

        self.setLayout(main_layout)

    def _connect_signals(self):
        ...