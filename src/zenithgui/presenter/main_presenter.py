from zenithgui.model.main_model import MainModel
from zenithgui.view.main_window import MainWindow

class MainPresenter:
    def __init__(self, model: MainModel, view: MainWindow):
        self.model = model
        self.view = view

        self._connect_signals()

    def _connect_signals(self):
        self.view.connection_requested.connect(self._handle_connection_request)

    def _handle_connection_request(self):
        connection_succeeded = self.model.connect_to_lora()

        self.view.show_connection_result(connection_succeeded)

        if connection_succeeded:
            self.view.goto_dashboard_page()