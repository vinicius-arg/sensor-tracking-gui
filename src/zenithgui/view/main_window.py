from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.QtGui import QIcon

from zenithgui.view.pages.connection_page import ConnectionPage
from zenithgui.view.pages.dashboard_page import DashboardPage

def align_center(screen, width, height):
    return ((screen.width() - width) // 2, (screen.height() - height) // 2)

class MainWindow(QMainWindow):
    def __init__(self, screen, width, height, icon_path):
        super().__init__()
        x, y = align_center(screen, width, height)
        self.setWindowTitle("Zenith GUI")
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

    def _promote_signals(self):
        """Torna sinais de páginas internas à camada view visíveis a camadas superiores
        da aplicação. Reduz acoplamento."""

        self.connection_requested = self.connection_page.connection_requested

    def goto_dashboard_page(self):
        self.stack.setCurrentWidget(self.dashboard_page)

    def show_connection_result(self, connection_ok):
        # TODO Implementar janela de diálogo
        if connection_ok:
            print("Conexao bem sucedida.")
        else:
            print('Conexao falhou')
