# zenithgui/controller/main_controller.py (versão modificada)

from PyQt6.QtCore import QObject
from crc import Calculator, Crc16
from model.telemetry_model import RocketData, TelemetryPacket
from communication.serial_reader import SerialReader
# --- ADICIONE A IMPORTAÇÃO DO SIMULADOR ---
from communication.serial_simulator import SerialSimulator 

CRC_CALCULATOR = Calculator(Crc16.CCITT_FALSE)

class MainController(QObject):
    def __init__(self, use_simulator: bool = False, parent=None): # Adicionamos um seletor
        super().__init__(parent)
        self.rocket_data = RocketData()

        # --- LÓGICA PARA ESCOLHER ENTRE O REAL E O SIMULADOR ---
        if use_simulator:
            self.reader = SerialSimulator()
            # Conecta o sinal do simulador ao nosso slot de processamento
            self.reader.packet_received.connect(self._on_new_packet_simulated)
        else:
            self.reader = SerialReader()
            # Conecta o sinal do leitor serial ao nosso slot de processamento
            self.reader.packet_received.connect(self._on_new_packet_real)

    # --- MÉTODO PARA PROCESSAR DADOS REAIS (COM VALIDAÇÃO DE CRC) ---
    def _on_new_packet_real(self, raw_data: bytes):
        payload = raw_data[:-2]
        received_crc = int.from_bytes(raw_data[-2:], 'little')
        calculated_crc = CRC_CALCULATOR.checksum(payload)

        if calculated_crc == received_crc:
            self.rocket_data.update_from_bytes(raw_data)
        else:
            print(f"CRC Inválido! Esperado: {calculated_crc}, Recebido: {received_crc}")

    # --- MÉTODO PARA PROCESSAR DADOS SIMULADOS (SEM VALIDAÇÃO DE CRC) ---
    # Como o simulador já gera o CRC correto, podemos pular a verificação para economizar CPU
    def _on_new_packet_simulated(self, raw_data: bytes):
        self.rocket_data.update_from_bytes(raw_data)

    # --- MÉTODOS PARA A VIEW CHAMAR ---
    def start_tracking(self, port: str, baud: int):
        if isinstance(self.reader, SerialReader):
            self.reader.connect_to(port, baud)

    def stop_tracking(self):
        if isinstance(self.reader, SerialReader):
            self.reader.disconnect()

    def start_simulation(self):
        if isinstance(self.reader, SerialSimulator):
            self.reader.start_simulation()

    def stop_simulation(self):
        if isinstance(self.reader, SerialSimulator):
            self.reader.stop_simulation()

    def list_ports(self):
        return SerialReader.list_available_ports()