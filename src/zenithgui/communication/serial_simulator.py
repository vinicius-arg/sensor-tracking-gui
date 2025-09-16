import time
import math
import random
import ctypes
from PyQt6.QtCore import QThread, pyqtSignal

# Importamos as definições do nosso backend
from model.telemetry_model import TelemetryPacket
from controller.main_controller import CRC_CALCULATOR

# O simulador precisa saber o tamanho do pacote para gerar os bytes corretamente
PACKET_SIZE = ctypes.sizeof(TelemetryPacket)

class SerialSimulator(QThread):
    """
    Uma classe que simula o SerialReader. Em vez de ler uma porta serial,
    ela gera pacotes de telemetria falsos em uma thread e os emite
    através do mesmo sinal 'packet_received'.
    """
    packet_received = pyqtSignal(bytes)
    status_changed = pyqtSignal(str, bool)

    def __init__(self, frequency_hz: int = 10, parent=None):
        super().__init__(parent)
        self.is_running = False
        self.frequency = frequency_hz
        self.packet_count = 0

    def start_simulation(self):
        """ Inicia a simulação e a thread. """
        self.is_running = True
        self.status_changed.emit(f"Simulador iniciado ({self.frequency} Hz)", True)
        self.start()

    def stop_simulation(self):
        """ Para a thread de simulação. """
        self.is_running = False
        self.wait()

    def run(self):
        """ O coração da thread de simulação. Gera dados em loop. """
        while self.is_running:
            # 1. Criar uma instância vazia do nosso pacote de telemetria
            packet = TelemetryPacket()

            # 2. Preencher o pacote com dados simulados e dinâmicos
            # Usamos o contador de pacotes para criar uma onda senoidal para a altitude
            packet.altura = 500 * (1 + math.sin(self.packet_count / 50)) + random.uniform(-10, 10)
            
            # Simular aceleração com algum ruído
            packet.aceleracao_x = random.uniform(-0.5, 0.5)
            packet.aceleracao_y = random.uniform(-0.5, 0.5)
            packet.aceleracao_z = 9.81 + random.uniform(-1.0, 1.0)
            
            packet.temperatura = 25 + math.sin(self.packet_count / 200) * 5
            packet.tensao_bateria = 4.15 - (self.packet_count / 5000)

            packet.status.as_byte = 0b00011111 # Ligar todos os flags de status

            # 3. Converter a estrutura para bytes, exceto os 2 últimos bytes do CRC
            payload = bytes(packet)[:-2]

            # 4. Calcular o CRC sobre o payload
            calculated_crc = CRC_CALCULATOR.checksum(payload)
            packet.crc = calculated_crc

            # 5. Emitir o pacote completo como bytes
            self.packet_received.emit(bytes(packet))
            
            self.packet_count += 1
            
            # 6. Esperar o tempo certo para simular a frequência
            time.sleep(1 / self.frequency)
        
        self.status_changed.emit("Simulador parado", False)
