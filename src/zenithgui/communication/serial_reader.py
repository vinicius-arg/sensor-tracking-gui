import serial.tools.list_ports
import ctypes
import time

from serial import Serial, SerialException
from threading import Thread, Event
from queue import Queue

from zenithgui.communication.packet import Packet
from zenithgui.communication.sender import Sender
from zenithgui.model.telemetry import TelemetryPacket
from zenithgui.util import _calculate_crc
from zenithgui.config import DEV_MODE

# Bytes de início de quadro (Start of Frame)
SOF = b'\xAA\xBB'
PACKET_SIZE = ctypes.sizeof(TelemetryPacket)

class HandshakeException(Exception):
    """Classe pra lançar exceção caso dê problema no hanshake.
    """
    pass

class SerialReader(Thread):
    """Thread para ler continuamente a porta serial sem bloquear a UI.
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
            try:
                if self.serial.read(1) == SOF[0:1]:
                    if self.serial.read(1) == SOF[1:2]:
                        data = self.serial.read(PACKET_SIZE)
                        packet = Packet.as_data(data)
                        if len(data) == PACKET_SIZE:
                            # Necessário calcular crc?
                            Sender.send_packet(self.packet_queue, packet)
                        else:
                            msg = "Notificação: Pacote provavelmente corrompido."
                            Sender.send_packet_with_note(self.packet_queue, msg, packet)
            except SerialException as e:
                # Vamos tentar não interromper a conexão
                err_packet = Packet.as_error(f"{msg}\n{e}")
                Sender.send_packet(self.packet_queue, err_packet)

    def _serial_connect(self, port, baudrate=9600, force=False):
        """Realiza a conexão com a porta serial passada como argumento.

        Args:
            port (str): Porta de conexão
            baudrate (int, optional): Baudrate de comunicação com o dispositivo. 9600 por padrão.
            force (bool, optional): Força conexão (ignora handshake). Falso por padrão.
        """
        if DEV_MODE:
            self.packet_queue.put(Packet.as_status("Conexão bem sucedida!"))
        else:
            try:
                self.serial = Serial(port, baudrate=int(baudrate), timeout=2)
                time.sleep(2)
                if not force:
                    # Força conexão sem handshake
                    self._serial_handshake(self.serial)
                self.packet_queue.put(Packet.as_status("Conexão bem sucedida!"))
            
            except SerialException as e:
                self.packet_queue.put(Packet.as_error(f"Erro ao conectar-se:\n{e}"))
                self.disconnect()
            
            except HandshakeException as e:
                hint = "Se nada resolver, ative a conexão forçada."
                self.packet_queue.put(Packet.as_error(f"Erro no handshake:\n{e}\n*{hint}"))
                self.disconnect()
        
    def _serial_handshake(self, ser: Serial):
        """Verifica se o dispositivo foi realmente conectado; se pode ler e transmitir dados.
        """
        ser.flush()
        ser.write(b'AT\r\n') # Comando AT (Attention). Resposta esperada: OK
        res = ser.readline()
        res_str = res.decode('utf-8').strip()
        if "OK" not in res_str:
            raise HandshakeException("HandshakeException: Serial connection not estabelished.")

    def disconnect(self):
        """Para a thread e fecha a conexão.
        """
        self.serial.close()
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