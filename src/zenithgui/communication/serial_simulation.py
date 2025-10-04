import serial.tools.list_ports
import random
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
        self._stop_event = Event()
        
        self.packet_queue = queue
        self.is_running = False

    def run(self):
        """Executado quando self.start() é chamado.
        """
        self._serial_connect(self._port_name, self._baudrate, self._force_connection)

        while self.is_running:
            data = self.generate_test_data()
            packet = Packet.as_data(data)
            Sender.send_packet(self.packet_queue, packet)

    def generate_test_data(self):
        p = telemetry.TelemetryPacket()
        p.status.as_byte = 0xf7
        p.temperature = 25.0 + random.randint(-5, 5)
        p.accel_x, p.accel_y, p.accel_z = (0.0 + random.randint(-1, 1), 0.0 + random.randint(-1, 1), -9.81 + random.uniform(-.1, .1))
        p.gyro_x, p.gyro_y, p.gyro_z = (0.0 + random.randint(-1, 1), 0.0 + random.randint(-1, 1), 0.0 + random.randint(-1, 1))
        p.pressure = 1.0 + random.uniform(-.1, .1)
        p.height = 0.0 + random.randint(-1, 1)
        p.latitude, p.longitude = (-10.921946 + random.uniform(-.1, .1), -37.104649 + random.uniform(-.1, .1))
        p.speed_xy = 0.0 + random.randint(-1, 1)
        p.battery = 5 << 16
        p.crc = 0xa04c
        return bytes(p)

    def _bin(self, n: float):
        import struct
        return struct.unpack('!I', struct.pack('!f', n))[0]

    def _serial_connect(self, port, baudrate=9600, force=False):
        """Realiza a conexão com a porta serial passada como argumento.
        """
        print(port, baudrate, force)
        self.packet_queue.put(Packet.as_status("Conexão bem sucedida!"))

    def get_rocket_data(self):
        return self._rocket_data.get_data()

    def disconnect(self):
        """Para a thread e fecha a conexão.
        """
        self._stop_event.set()
        self.join()
        self.is_running = False

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