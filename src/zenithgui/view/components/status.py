from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtCore import Qt

from zenithgui.config import Config
from zenithgui.util import FormatUtils

class QDisc(QWidget):
    """Widget customizado que desenha um círculo."""
    def __init__(self, size, state=False):
        super().__init__()
        self.setFixedSize(size, size)
        self.color = Qt.gray
        self.state = state


    def __update_color(self):
        self.color = Qt.green if self.state else Qt.gray


    def set_state(self, state: bool):
        if state != self.state:
            self.state = state
            self.__update_color()
            self.update()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(self.color, Qt.SolidPattern))
        painter.setPen(QPen(self.color))
        
        rect = self.rect()
        rect.adjust(5, 5, -5, -5) 
        painter.drawEllipse(rect)


class StatusIndicator(QWidget):
    """Armazena informações de um único indicador
    """
    def __init__(self, size, text, state=False):
        super().__init__()
        self.size = size
        self.text = text
        self.state: bool = state

        self.__create_widget()
        self.__create_layout()


    def __create_widget(self):
        self.light = QDisc(self.size)
        self.label = QLabel(self.text)


    def __create_layout(self):
        self.content = QHBoxLayout()
        self.content.addWidget(self.light)
        self.content.addWidget(self.label)

        self.setLayout(self.content)


    def set_state(self, state: bool):
        self.light.set_state(state)

class StatusMonitor(QWidget):
    def __init__(self, state):
        super().__init__()

        self.status = state

        self.status_indicators: dict[str, StatusIndicator] = {}
        self.status_alias = Config.STATUS_DATA_ALIAS

        self.__create_widget()
        self.__create_layout()
        self.__apply_styles()


    def __create_widget(self):
        for data in Config.STATUS_DATA:
            item = StatusIndicator(size=20, text=FormatUtils.get_fancy_name(data, Config.STATUS_DATA_ALIAS))
            self.status_indicators[data] = item
    

    def __create_layout(self):
        self.content = QHBoxLayout()
        for _, value in self.status_indicators.items():
            self.content.addWidget(value)

        self.content.addStretch()
        self.setLayout(self.content)


    def __apply_styles(self):
        for _, value in self.status_indicators.items():
            value.label.setProperty("class", "statusLabel")


    def update_component(self):
        for key, value in self.status.items():
            self.status_indicators[key].set_state(value == 1)

