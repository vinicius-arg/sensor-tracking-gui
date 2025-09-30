import sys

from zenithgui.communication import serial_reader as serial

class MainModel():
    def __init__(self, serial_reader: serial.SerialReader):
        self.serial_reader = serial_reader

    def connect_to_lora(self, port, baudrate):
        res = self.serial_reader.start_tracking(port, baudrate)            
        return res
    
    def list_available_ports(self):
        serial.SerialReader.list_available_ports()
