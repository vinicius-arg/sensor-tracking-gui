from PyQt5.QtCore import QTimer
from queue import Queue

from zenithgui.model.main_model import MainModel
from zenithgui.view.main_window import MainWindow
from zenithgui.communication import Packet, PacketType

class MainPresenter:
    def __init__(self, model: MainModel, view: MainWindow):
        self.packet_queue = Queue()
        self.queue_timer = QTimer()
        self.model = model
        self.view = view

        self._connect_signals()

    def _connect_signals(self):
        self.view.connection_requested.connect(self._handle_connection_request)
        self.view.available_ports_requested.connect(self._handle_ports_request)
        self.queue_timer.timeout.connect(self._process_queue)

    def _process_queue(self):
        packet: Packet = self.packet_queue.get() 
        if packet.type == PacketType.DATA:
            self.model.update_rocket_data(packet.payload)
            rocket_data = self.model.get_rocket_data()
            self.view.update_graphs(rocket_data)
        elif packet.type == PacketType.STATUS:
            self.view.show_info_as_popup(True, packet.payload)
        elif packet.type == PacketType.ERROR:
            self.view.show_info_as_popup(False, packet.payload)

    def stop_app(self):
        self.model.stop_tracking()
        self.queue_timer.stop()

    def _handle_ports_request(self):
        available_ports = self.model.list_available_ports()
        self.view.load_available_ports(available_ports)

    def _handle_connection_request(self, port, baudrate, force=False):
        self.model.connect_to_lora(port, baudrate, self.packet_queue, force)

        result = self.packet_queue.get()
        success = result.type == PacketType.STATUS
        self.view.show_info_as_popup(success, result.payload)

        if success:
            self.view.goto_dashboard_page()
            self.queue_timer.start(33) # 33ms são 30 chamadas por segundo
