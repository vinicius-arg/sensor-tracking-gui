import sys

from zenithgui import config
from PyQt5.QtWidgets import QApplication
from zenithgui.util.path_utils import resource_path

from zenithgui.view.main_window import MainWindow

style_path = resource_path("assets", "styles", "styles.qss")
icon_path = resource_path("assets", "images", "scooby.png")

with style_path.open("r", encoding="utf-8") as f:
    style = f.read()

def main():
    app = QApplication(sys.argv)

    width, height = 800, 600
    screen = QApplication.primaryScreen().geometry()

    main_window = MainWindow(screen, width, height, str(icon_path.resolve()))
    main_window.setStyleSheet(style)
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()