from zenithgui.model.main_model import MainModel
from zenithgui.view.main_window import MainWindow

class MainPresenter:
    def __init__(self, model: MainModel, view: MainWindow):
        self.model = model
        self.view = view

        self._connect_signals()

    def _connect_signals(self):
        self.view.connection_requested.connect(self._handle_connection_request)
        self.view.available_ports_requested.connect(self._handle_ports_request)

    def _handle_ports_request(self):
        available_ports = self.model.list_available_ports()
        self.view.load_available_ports(available_ports)

    def _handle_connection_request(self, port, baudrate, force=False):
        serial, success, message = self.model.connect_to_lora(port, baudrate, force)
        self.view.show_connection_result(success, message)

        if success:
            self.view.goto_dashboard_page(serial)
