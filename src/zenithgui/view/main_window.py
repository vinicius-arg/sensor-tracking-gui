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

        self.connection_page = ConnectionPage()
        self.dashboard_page = DashboardPage()

        self.stack.addWidget(self.connection_page)
        self.stack.addWidget(self.dashboard_page)

# Exemplo de múltiplas telas do GPT:
# Cria o QStackedWidget
# self.stack = QStackedWidget()
# self.setCentralWidget(self.stack)

# # Adiciona as telas
# self.dashboard_page = DashboardPage()
# self.settings_page = SettingsPage()

# self.stack.addWidget(self.dashboard_page)
# self.stack.addWidget(self.settings_page)

# # Toolbar para navegação
# toolbar = QToolBar("Navigation")
# self.addToolBar(toolbar)

# dashboard_action = QAction("Dashboard", self)
# dashboard_action.triggered.connect(lambda: self.stack.setCurrentWidget(self.dashboard_page))
# toolbar.addAction(dashboard_action)

# settings_action = QAction("Configurações", self)
# settings_action.triggered.connect(lambda: self.stack.setCurrentWidget(self.settings_page))
# toolbar.addAction(settings_action)