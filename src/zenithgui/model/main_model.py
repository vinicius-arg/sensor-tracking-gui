import sys

from zenithgui.communication import SerialReader
from zenithgui.config import DEV_MODE

class MainModel():
    def __init__(self, serial_reader: SerialReader):
        self.serial_reader = serial_reader

    def connect_to_lora(self, port, baudrate, force=False):
        res = self.serial_reader.start_tracking(port, baudrate, force)

        if DEV_MODE:
            return (None, True, "Conexão bem sucedida!")
        else:
            return res
    
    def list_available_ports(self):
        return SerialReader.list_available_ports()
