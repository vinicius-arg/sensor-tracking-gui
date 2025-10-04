import serial.tools.list_ports
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
        self._rocket_data = telemetry.RocketData()
        self._stop_event = Event()
        
        self.packet_queue = queue
        self.is_running = False

    def run(self):
        """Executado quando self.start() é chamado.
        """
        self._serial_connect(self._port_name, self._baudrate, self._force_connection)

        while self.is_running:
            data = self._generate_test_data()
            packet = Packet.as_data()
            self.rocket_data.update_data(data)
            Sender.send_packet(self.packet_queue, packet)

    def _generate_test_data(self):
        ...

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