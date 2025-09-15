import sys

from zenithgui import config
from PyQt5.QtWidgets import QApplication
from zenithgui.util.path_utils import resource_path

from zenithgui.view.main_window import MainWindow
from zenithgui.presenter.main_presenter import MainPresenter
from zenithgui.model.main_model import MainModel

style_path = resource_path("assets", "styles", "styles.qss")
icon_path = resource_path("assets", "images", "scooby.png")

# Importação dos estilos .qss
with style_path.open("r", encoding="utf-8") as f:
    style = f.read()

def main():
    app = QApplication(sys.argv)

    width, height = 800, 600
    screen = QApplication.primaryScreen().geometry()

    # Definição das camadas da aplicação 
    main_window = MainWindow(screen, width, height, str(icon_path.resolve()))
    model = MainModel()
    presenter = MainPresenter(model=model, view=main_window)

    main_window.setStyleSheet(style)

    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()