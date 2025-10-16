import os
from PyQt5.QtWidgets import QWidget, QCheckBox, QLineEdit, QPushButton, QFileDialog, QHBoxLayout
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import QDir

from zenithgui.util.write_csv import write_csv

class FileHandler(QWidget):
    SAVE_STR = "~/path/to/recordings"
    SELECTOR_DLG = "Selecione um diretório para salvar os dados"
    SELECTOR_STR = "Open..."

    def __init__(self, rec: QCheckBox):
        super().__init__()
        self.recording = rec
        
        self._create_widget()
        self._create_layout()
        self._connect_signals()
        self._apply_styles()

        self.setLayout(self.content)

    def _create_widget(self):
        self.file_path = QLineEdit()
        self.dir_selector = QPushButton(self.SELECTOR_STR)

    def _create_layout(self):
        self.content = QHBoxLayout()

        self.content.addWidget(self.file_path)
        self.content.addWidget(self.dir_selector)

    def _connect_signals(self):
        self.dir_selector.pressed.connect(self._get_dir)

    def _apply_styles(self):
        self.file_path.setPlaceholderText(self.SAVE_STR)
        self.file_path.setReadOnly(True)

        self.file_path.setProperty("class", "input")
        self.dir_selector.setProperty("class", "menuBtn")

    def _get_dir(self):
        self.dialog = QFileDialog()

        palette = self.dialog.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#1e1e1e"))
        self.dialog.setPalette(palette)

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
   
        path = self.dialog.getExistingDirectory(
            parent=self,
            caption=self.SELECTOR_DLG,
            directory=QDir.homePath(),
            options=options
        )

        if path:
            self.file_path.setText(path)
            self.path = path

    def save_data(self, data: dict[str, list], path: str):
        if self.recording.isChecked():
            write_csv(data, path)

    def get_file_path(self):
        return self.path