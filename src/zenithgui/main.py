import sys

# ### NOVO: Importa o nosso controlador ###
from zenithgui.controller import MainController

from zenithgui import config
from PyQt6.QtWidgets import QApplication
from zenithgui.util.path_utils import resource_path
from zenithgui.view.main_window import MainWindow

# --- Arquivos de Estilo e Ícone (sem alterações) ---
style_path = resource_path("assets", "styles", "styles.qss")
icon_path = resource_path("assets", "images", "scooby.png")
with style_path.open("r", encoding="utf-8") as f:
    style = f.read()

# ### NOVO: Chave seletora para modo de operação ###
# Mude para False para usar a porta serial real
USE_SIMULATOR = True

def main():
    app = QApplication(sys.argv)

    # ### NOVO: Instancia o "cérebro" da aplicação primeiro ###
    # A lógica de usar o simulador ou o leitor real está encapsulada aqui
    controller = MainController(use_simulator=USE_SIMULATOR)

    width, height = 800, 600
    screen = QApplication.primaryScreen().geometry()

    # ### NOVO: Entrega o controller para a MainWindow ###
    # A janela agora é criada com uma referência ao seu controlador
    main_window = MainWindow(
        screen,
        width,
        height,
        str(icon_path.resolve()),
        controller=controller  # Passa o cérebro para a interface
    )
    
    main_window.setStyleSheet(style)
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()