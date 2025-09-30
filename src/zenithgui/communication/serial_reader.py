import ctypes
import time
from serial import Serial, SerialException
import serial.tools.list_ports
from threading import Thread

from typing import Tuple, Optional

from model import telemetry

# Bytes de início de quadro (Start of Frame)
SOF = b'\xAA\xBB'
PACKET_SIZE = ctypes.sifzeof(telemetry.TelemetryPacket)

class HandshakeException(Exception):
    """Classe pra lançar exceção caso dê problema no hanshake."""
    pass

class SerialReader(Thread):
    """
    Thread para ler continuamente a porta serial sem bloquear a UI.
    """
    def __init__(self, telemetry_layer):
        super().__init__()
        self._telemetry = telemetry_layer 
        self.is_running = False

    def start_tracking(self, port: str, baudrate: int, force=False) -> Tuple[Optional[Serial], bool, str]:
        """ Inicia a conexão e a thread de leitura da porta serial."""
        self.port_name = port
        self.baud_rate = baudrate
        
        res = self._serial_connect(port, baudrate, force)
        self.is_running = True
        self.start()

        return res

    def _serial_connect(self, port, baudrate=9600, force=False):
        """Realiza a conexão com a porta serial passada como argumento."""
        try:
            self.serial = Serial(port, baudrate=int(baudrate), timeout=2)
            time.sleep(2)
            
            if force == False: # Parâmetro que força conexão
                self._serial_handshake(self.serial)
            
            return (self.serial, True, f"Conexão bem sucedida!")
        except SerialException as e:
            return (None, False, f"Erro ao conectar-se: {e}")
        except HandshakeException as e:
            return (None, False, f"Erro no handshake: {e}\n*Se nada resolver, ative a conexão forçada.")
    
    def _serial_handshake(self, ser: Serial):
        """Verifica se o dispositivo foi realmente conectado; se pode ler e transmitir dados."""
        ser.flush()
        # Comando AT (Attention). Resposta esperada: OK
        ser.write(b'AT\r\n')
        res = ser.readline()
        res_str = res.decode('utf-8').strip()

        if "OK" not in res_str:
            raise HandshakeException("HandshakeException: Serial connection not estabelished.")

    def disconnect(self):
        """ Para a thread e fecha a conexão. """
        self.is_running = False
        self.serial.close()

    def run(self):
        """Este método é executado quando self.start() é chamado. """
        while self.is_running:
            try:
                if self.serial.read(1) == SOF[0:1]:
                    if self.serial.read(1) == SOF[1:2]:
                        packet_data = self.serial.read(PACKET_SIZE)
                        if len(packet_data) == PACKET_SIZE:
                            crc = self._calculate_crc()
                            self._send_packet(packet_data)
            except SerialException:
                #TODO Inserir pacotes de erro em fila compartilhada com o front.
                self.is_running = False

    def _calculate_crc(self):
        #TODO Implementar calculo de CRC-16
        ...

    def _send_packet(self, payload):
        #TODO Implementar envio de pacote sem PyQt
        ...

    @staticmethod
    def list_available_ports():
        """
        Verifica o sistema e retorna uma lista de portas seriais disponíveis.
        Retorna uma lista: [port.device..1, ..., port.device..n]
        """
        ports = serial.tools.list_ports.comports()
        available_ports = []
        if not ports:
            return ["<Nenhuma porta encontrada>"]

        for port in ports:
            #if sys.platform.startswith("win") or "USB" in port.description or "ACM" in port.device:
            available_ports.append(port.device)
            
        return available_ports