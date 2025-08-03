import sys

from zenithgui import config
from PyQt5.QtWidgets import QApplication

from zenithgui.view.main_window import MainWindow

def main():
    app = QApplication(sys.argv)

    width, height = 800, 600
    screen = QApplication.primaryScreen().geometry()

    main_window = MainWindow(screen, width, height)
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()