import sys

from PyQt5.QtWidgets import QApplication

from zenithgui.presenter import MainPresenter
from zenithgui.model import MainModel
from zenithgui.view import MainWindow
from zenithgui.util import ThemeUtils

def main():
    app = QApplication(sys.argv)

    width, height = 800, 600
    screen = QApplication.primaryScreen().geometry()
    icon_path = ThemeUtils.find_icon()

    # Definição das camadas da aplicaçãos
    model = MainModel()
    main_window = MainWindow(screen, width, height, str(icon_path.resolve()))
    presenter = MainPresenter(model=model, view=main_window)

    ThemeUtils.setup_and_apply_stylesheets(main_window)
    ThemeUtils.setup_fonts()

    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()