from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class ConnectionPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Olá da connection page"))

        self.setLayout(layout)
