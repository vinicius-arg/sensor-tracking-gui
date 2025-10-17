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
    """Thread para ler continuamente a porta serial.
    """
    CORRUPT_PACKET_MSG = "Notificação: Pacote provavelmente corrompido."

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

        self._connect(self._port_name, self._baudrate, self._force_connection)

    def run(self):
        """Executado quando self.start() é chamado.
           Quando pause_event está setado, os pacotes lidos são descartados.
        """
        self.is_running = True

        while self.is_running:
            try:
                if self._check_sof() and self._can_recv_packet():
                    data = self.serial.read(PACKET_SIZE)
                    if not self._pause_event.is_set():
                        packet = Packet.as_data(data)

                        if self._packet_is_valid(data):
                            Sender.send_packet(self.packet_queue, packet)
                        else:
                            Sender.send_packet_with_note(
                                queue=self.packet_queue, 
                                msg=self.CORRUPT_PACKET_MSG, 
                                packet=packet)
                else:
                    time.sleep(0.1)
            except SerialException as e: # Vamos tentar não interromper a conexão
                err_packet = Packet.as_error(f"{self.CORRUPT_PACKET_MSG}\n{e}")
                Sender.send_packet(self.packet_queue, err_packet)

    def pause(self):
        self._pause_event.set()
        self.is_paused = True

    def resume(self):
        self._pause_event.clear()
        self.is_paused = False

    def _can_recv_packet(self):
        return self.packet_queue.qsize() == 0
    
    def _packet_is_valid(self, data):
        return len(data) == PACKET_SIZE

    def _check_sof(self) -> bool:
        return self.serial.read(len(SOF)) == SOF

    def _connect(self, port, baudrate=9600, force=False):
        """Realiza a conexão com a porta serial passada como argumento.

        Args:
            port (str): Porta de conexão
            baudrate (int, optional): Baudrate de comunicação com o dispositivo. 9600 por padrão.
            force (bool, optional): Força conexão (ignora handshake). Falso por padrão.
        """
        try:
            self.serial = Serial(port, baudrate=int(baudrate), timeout=2)
            time.sleep(2)
            if not force: # Força conexão sem handshake
                self._handshake(self.serial)
            self.packet_queue.put(Packet.as_status("Conexão bem sucedida!"))
        
        except SerialException as e:
            self.packet_queue.put(Packet.as_error(f"Erro ao conectar-se:\n{e}"))
            self.disconnect()
        
        except HandshakeException as e:
            hint = "Se nada resolver, ative a conexão forçada."
            self.packet_queue.put(Packet.as_error(f"Erro no handshake:\n{e}\n*{hint}"))
            self.disconnect()

        self.is_connected = True
        
    def _handshake(self, serial: Serial):
        """Verifica se o dispositivo foi realmente conectado; se pode ler e transmitir dados.
        """
        serial.flush()
        serial.write(b'AT\r\n') # Comando AT (Attention). Resposta esperada: OK
        res = serial.readline()
        res_str = res.decode('utf-8').strip()
        if "OK" not in res_str:
            raise HandshakeException("HandshakeException: Serial connection not estabelished.")

    def disconnect(self):
        """Para a thread e fecha a conexão.
        """
        self.serial.close()
        self._pause_event.set()
        self.join()
        self.is_running = False
        self.is_connected = False