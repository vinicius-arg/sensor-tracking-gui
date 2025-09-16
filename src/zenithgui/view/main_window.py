from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from PyQt6.QtGui import QIcon

# ### NOVO: Importa o controller para anotação de tipo ###
from zenithgui.controller import MainController 

from zenithgui.view.pages.connection_page import ConnectionPage
from zenithgui.view.pages.dashboard_page import DashboardPage

def align_center(screen, width, height):
    return ((screen.width() - width) // 2, (screen.height() - height) // 2)

class MainWindow(QMainWindow):
    # ### NOVO: Modifica o __init__ para aceitar o controller ###
    def __init__(self, screen, width, height, icon_path, controller: MainController):
        super().__init__()
        
        # ### NOVO: Armazena a referência do controller ###
        self.controller = controller

        x, y = align_center(screen, width, height)
        self.setWindowTitle("Zenith GUI")
        self.setGeometry(x, y, width, height)
        self.setWindowIcon(QIcon(icon_path))

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack) 

        # ### NOVO: Passa o controller para as páginas na criação ###
        # Agora as páginas sabem com quem conversar para obter dados e enviar comandos.
        self.connection_page = ConnectionPage(self.controller)
        self.dashboard_page = DashboardPage(self.controller)

        self.stack.addWidget(self.connection_page)
        self.stack.addWidget(self.dashboard_page)

        # ### NOVO (BOA PRÁTICA): Conecta o status bar aos sinais do backend ###
        self.setup_status_bar()

    def setup_status_bar(self):
        """ Configura a barra de status para exibir mensagens do backend. """
        # Cria a barra de status
        self.statusBar().showMessage("Pronto para conectar...")

        # Conecta o sinal 'status_changed' do leitor/simulador a um método local
        self.controller.reader.status_changed.connect(self.update_status_bar)

    def update_status_bar(self, message: str, is_connected: bool):
        """ Atualiza a mensagem e a cor da barra de status. """
        self.statusBar().showMessage(message)
        if is_connected:
            self.statusBar().setStyleSheet("background-color: #4CAF50; color: white;") # Verde
        else:
            self.statusBar().setStyleSheet("background-color: #F44336; color: white;") # Vermelho