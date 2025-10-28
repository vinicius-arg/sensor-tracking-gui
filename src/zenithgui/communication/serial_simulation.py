import serial.tools.list_ports
import random
import time
import ctypes

from threading import Thread, Event
from queue import Queue

from zenithgui.communication.packet import Packet
from zenithgui.communication.sender import Sender
from zenithgui.model import telemetry

# Bytes de início de quadro (Start of Frame)
SOF = b'\xAA\xBB'
PACKET_SIZE = ctypes.sizeof(telemetry.TelemetryPacket)

class SerialSimulation(Thread):
    """Thread para simular a leitura da porta serial.
    """
    def __init__(self, port, baudrate, queue: Queue, force):
        super().__init__()
        self._port_name = port
        self._baudrate = baudrate
        self._force_connection = force
        self._pause_event = Event()
        
        self.packet_queue = queue
        self.is_connected = False
        self.is_running = False
        self.is_paused = True

        self.__serial_connect(self._port_name, self._baudrate, self._force_connection)


    def __serial_connect(self, port, baudrate=9600, force=False):
        """Realiza a conexão com a porta serial passada como argumento.
        """
        print(f"Conectado ao simulador: port={port}, bdr={baudrate}, f={force}")
        self.packet_queue.put(Packet.as_status("Conexão bem sucedida!"))
        self.is_connected = True


    def run(self):
        """Executado quando self.start() é chamado.
        """
        #self.__serial_connect(self._port_name, self._baudrate, self._force_connection)
        self.is_running = True
        self.is_paused = False

        while self.is_running:
            if self.packet_queue.qsize() == 0:
                data = self.generate_test_data()
                if not self._pause_event.is_set():
                    packet = Packet.as_data(data)
                    Sender.send_packet(self.packet_queue, packet)
                else:
                    time.sleep(0.1)
            else:
                time.sleep(0.1)


    def generate_test_data(self):
        p = telemetry.TelemetryPacket()
        p.status.as_byte = 0xf7
        p.temperature = 25.0 + random.uniform(-5, 5)
        p.accel_x, p.accel_y, p.accel_z = (0.0 + random.uniform(-1, 1), 0.0 + random.uniform(-1, 1), -9.81 + random.uniform(-.1, .1))
        p.gyro_x, p.gyro_y, p.gyro_z = (0.0 + random.uniform(-1, 1), 0.0 + random.uniform(-1, 1), 0.0 + random.uniform(-1, 1))
        p.pressure = 1.0 + random.uniform(-.1, .1)
        p.height = 0.0 + random.uniform(-1, 1)
        p.latitude, p.longitude = (-10.921946 + random.uniform(-.1, .1), -37.104649 + random.uniform(-.1, .1))
        p.speed_xy = 0.0 + random.uniform(-1, 1)
        p.battery = 5 << 16
        p.crc = 0xa04c
        return bytes(p)


    def get_rocket_data(self):
        return self._rocket_data.get_data()
    

    def pause(self):
        self._pause_event.set()
        self.is_paused = True


    def resume(self):
        self._pause_event.clear()
        self.is_paused = False


    def disconnect(self):
        """Para a thread e fecha a conexão.
        """
        self._pause_event.set()
        self.is_connected = False
        self.is_running = False
        self.join()


    @staticmethod
    def list_available_ports() -> list[str]:
        """Verifica o sistema e retorna uma lista de portas seriais disponíveis.

        Returns:
            list[str]: Retorna um lista do tipo { port.device[1], ..., port.device[n] }
        """
        ports = serial.tools.list_ports.comports()
        available_ports = []
        if not ports:
            return ["<Nenhuma porta encontrada>"]

        for port in ports:
            #if sys.platform.startswith("win") or "USB" in port.description or "ACM" in port.device:
            available_ports.append(port.device)
            
        return available_ports
    

def main():
    s = SerialSimulation("COM3", 9600, Queue(), False)
    print(s.generate_test_data())

if __name__ == "__main__":
    main()