import serial
import serial.tools.list_ports
import ctypes
from PyQt6.QtCore import QThread, pyqtSignal

# Importa a definição do nosso pacote para sabermos o tamanho esperado
from model.telemetry_model import TelemetryPacket

# Bytes de início de quadro (Start of Frame)
SOF = b'\xAA\xBB'
PACKET_SIZE = ctypes.sizeof(TelemetryPacket)

class SerialReader(QThread):
    """
    Thread para ler continuamente a porta serial sem bloquear a UI.
    """
    # Sinais que esta thread pode emitir
    packet_received = pyqtSignal(bytes)  # Emite um pacote de dados brutos válido
    status_changed = pyqtSignal(str, bool) # Emite o status da conexão (e.g., "Conectado", True)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.serial_port = None
        self.port_name = ""
        self.baud_rate = 0
        self.is_running = False

    def connect_to(self, port: str, baud: int):
        """ Inicia a conexão e a thread. """
        self.port_name = port
        self.baud_rate = baud
        self.is_running = True
        self.start() # Inicia a execução do método run() em uma nova thread

    def disconnect(self):
        """ Para a thread e fecha a conexão. """
        self.is_running = False
        self.wait() # Espera a thread terminar de forma limpa

    def run(self):
        """ O coração da thread. Este método é executado quando self.start() é chamado. """
        try:
            self.serial_port = serial.Serial(self.port_name, self.baud_rate, timeout=1)
            self.status_changed.emit(f"Conectado a {self.port_name}", True)
        except serial.SerialException as e:
            self.status_changed.emit(f"Erro: {e}", False)
            return

        while self.is_running:
            try:
                # 1. Procurar o primeiro byte do SOF
                if self.serial_port.read(1) == SOF[0:1]:
                    # 2. Se encontrou, procurar o segundo byte do SOF
                    if self.serial_port.read(1) == SOF[1:2]:
                        # 3. Se encontrou o SOF completo, ler o restante do pacote
                        packet_data = self.serial_port.read(PACKET_SIZE)
                        if len(packet_data) == PACKET_SIZE:
                            self.packet_received.emit(packet_data)
            except serial.SerialException:
                self.status_changed.emit("Erro: Dispositivo desconectado.", False)
                self.is_running = False
        
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        self.status_changed.emit("Desconectado", False)

    @staticmethod
    def list_available_ports():
        """ Retorna uma lista de portas seriais disponíveis. """
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]