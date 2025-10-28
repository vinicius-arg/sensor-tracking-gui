from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon

from zenithgui.view.components.custom_msg import MessageWindow
from zenithgui.view.pages.connection_page import ConnectionPage
from zenithgui.view.pages.dashboard_page import DashboardPage
from zenithgui.config import Config

class MainWindow(QMainWindow):
    def __init__(self, screen, width, height, icon_path):
        super().__init__()
        x, y = self.align_center(screen, width, height)
        self.setWindowTitle(Config.APP_NAME)
        self.setGeometry(x, y, width, height)
        self.setWindowIcon(QIcon(icon_path))

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack) 

        # Criação de páginas
        self.connection_page = ConnectionPage()
        self.dashboard_page = DashboardPage()

        # Adição das páginas à pilha
        self.stack.addWidget(self.connection_page)
        self.stack.addWidget(self.dashboard_page)

        self._promote_signals()
        self._promote_buttons()

        # Variáveis promovidas
        self.notification_label = self.dashboard_page.notification_label
        self.history = self.dashboard_page.full_history

    def _promote_buttons(self):
        self.start_btn = self.dashboard_page.start_btn
        self.pause_btn = self.dashboard_page.pause_btn
        self.stop_btn = self.dashboard_page.stop_btn
        self.checkbox = self.dashboard_page.checkbox
        self.file_handler = self.dashboard_page.file_handler

    def _promote_signals(self):
        """Torna sinais de páginas internas à camada view visíveis a camadas superiores
        da aplicação. Reduz acoplamento."""

        self.connection_requested = self.connection_page.connection_requested
        self.available_ports_requested = self.connection_page.available_ports_requested
        self.start_tracking = self.dashboard_page.start_tracking
        self.pause_tracking = self.dashboard_page.pause_tracking
        self.stop_tracking = self.dashboard_page.stop_tracking

    def goto_dashboard_page(self):
        self.stack.setCurrentWidget(self.dashboard_page)

    def update_graphs(self, rocket_data):
        self.dashboard_page.update_data(rocket_data)

    def show_info_as_popup(self, success, message):
        dlg = MessageWindow("Information", message, success)
        dlg.exec_()

    def show_info_as_notification(self, success, message):
        if success:
            self.notification_label.setText(f"Info:: {message}")
            self.notification_label.setProperty("class", "info")
        else:
            self.notification_label.setText(f"Error:: {message}")
            self.notification_label.setProperty("class", "error")

        self.notification_label.style().unpolish(self.notification_label)
        self.notification_label.style().polish(self.notification_label)

        QTimer.singleShot(
            Config.NOTIFICATION_DISAPPEAR_MS_TIME,
            lambda: self.notification_label.setText(""))

    def closeEvent(self, a0):
        """Chamado automaticamente quando o usuário fecha o programa.
           Encerra as threads e salva o monitoramento, caso esteja habilitado.
        """
        self.stop_tracking.emit()

        return super().closeEvent(a0)

    def load_available_ports(self, ports):
        self.connection_page.port_selector.addItems(ports)

    def align_center(self, screen, width, height):
        return ((screen.width() - width) // 2, (screen.height() - height) // 2)
    
    def update_ui(self):
        self.dashboard_page.update_page()
