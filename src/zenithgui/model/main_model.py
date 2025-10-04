from zenithgui.communication import SerialReader
from zenithgui.model import RocketData

class MainModel():
    def __init__(self):
        self._serial_reader = None
        self._rocket = RocketData()

    def connect_to_lora(self, port, baudrate, queue, force=False):
        if not self._serial_reader or not self._serial_reader.is_alive():
            # Passando canal de comunicação (queue) para o produtor
            self._serial_reader = SerialReader(port, baudrate, queue, force)
            self._serial_reader.start()

    def stop_tracking(self):
        self._serial_reader.disconnect()

    def get_rocket_data(self):
        return self._rocket.get_data()
    
    def update_rocket_data(self, data):
        self._rocket.update_data(data)

    def list_available_ports(self):
        return self._serial_reader.list_available_ports()
