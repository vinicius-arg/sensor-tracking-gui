from PyQt5.QtCore import pyqtSignal

class MainPresenter():
    def __init__(self, model, view):
        self.model = model
        self.view = view
   
        self._connect_signals()

    def _connect_signals(self):
        self.view.connection_page.connect_btn.connect(self.handle_connect_btn_clicked)

    def handle_connect_btn_clicked(self):
        print("click presenter")
        
