from PyQt5.QtWidgets import QMessageBox

class MessageWindow(QMessageBox):
    def __init__(self, title, message, success):
        super().__init__()
        self.title = title
        self.msg = message
        self.success = success

        self.icon = QMessageBox.Information if success else QMessageBox.Critical
        
        self.setWindowTitle(self.title)
        self.setText(self.msg)
        self.setStandardButtons(QMessageBox.Ok)
        self.setIcon(self.icon)