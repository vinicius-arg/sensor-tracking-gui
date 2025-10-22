from PyQt5.QtCore import QTimer
from queue import Queue, Empty

from zenithgui.model.main_model import MainModel
from zenithgui.view.main_window import MainWindow
from zenithgui.communication import Packet, PacketType

from zenithgui.config import config
from zenithgui.config import messages as msg

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
        self.view.start_tracking.connect(self.start_tracking)
        self.view.pause_tracking.connect(self.pause_tracking)
        self.view.stop_tracking.connect(self.stop_tracking)

    def _process_queue(self):
        try:
            packet: Packet = self.packet_queue.get_nowait()
            if packet.type == PacketType.DATA:
                self.model.update_rocket_data(packet.payload)
                rocket_data = self.model.get_rocket_data()
                self.view.update_graphs(rocket_data)
            elif packet.type == PacketType.STATUS:
                self.view.show_info_as_notification(True, packet.payload)
            elif packet.type == PacketType.ERROR:
                self.view.show_info_as_popup(False, packet.payload)
        except Empty:
            pass

    def start_tracking(self):
        self.model.start_tracking()
        self.queue_timer.start(config.PACKET_QUEUE_MS_TIME)
        self.set_buttons_state()

    def stop_tracking(self):
        if self.model.reader_is_running():
            self.queue_timer.stop()
            self.model.stop_tracking()
            self.set_buttons_state()
            self.view.start_btn.setEnabled(False)

            if self.view.checkbox.isChecked():
                path = self.view.file_handler.path
                data = self.view.history
                success = self.model.save_data_to_csv(data, path)

                message_scs = msg.NOTIFICATION_TRACKING_SAVED.format(path)
                message_err = msg.NOTIFICATION_TRACKING_SAVE_ERROR

                self.view.show_info_as_notification(
                    success, 
                    message_scs if success else message_err)
            else:
                self.view.show_info_as_notification(True, msg.NOTIFICATION_TRACKING_STOPPED)

    def pause_tracking(self):
        self.queue_timer.stop()
        self.model.pause_tracking()
        self.set_buttons_state()

        self.view.show_info_as_notification(True, msg.NOTIFICATION_TRACKING_PAUSED)

    def set_buttons_state(self):
        state = self.model.reader_is_running()

        self.view.stop_btn.setEnabled(state)
        self.view.pause_btn.setEnabled(state)
        self.view.start_btn.setEnabled(not state)
        self.view.checkbox.setEnabled(not state)
        self.view.file_handler.setEnabled(not state)

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
            self.set_buttons_state()