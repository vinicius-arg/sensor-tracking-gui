import ctypes
import numpy as np
from PyQt6.QtCore import QObject, pyqtSignal

# Nota de Engenharia: A discrepância "Bateria" foi resolvida adicionando o campo
# 'tensao_bateria'. O firmware do ESP32 precisa ser atualizado para incluir este
# dado na mesma posição. O tamanho total do pacote agora é 57 bytes.

class StatusFlags(ctypes.LittleEndianStructure):
    """ Mapeamento de bitfields para os flags de status. """
    _fields_ = [
        ("circuito_energizado", ctypes.c_uint8, 1),
        ("mpu_inicializado", ctypes.c_uint8, 1),
        ("bmp_inicializado", ctypes.c_uint8, 1),
        ("gps_inicializado", ctypes.c_uint8, 1),
        ("sd_inicializado", ctypes.c_uint8, 1),
        ("reservado", ctypes.c_uint8, 3),
    ]

class Status(ctypes.Union):
    """ Union permite acessar os flags como um byte ou individualmente. """
    _fields_ = [("flags", StatusFlags),
                ("as_byte", ctypes.c_uint8)]

class TelemetryPacket(ctypes.LittleEndianStructure):
    """
    Representação exata da struct enviada pelo foguete.
    O uso de ctypes garante uma conversão de bytes para objeto Python
    extremamente rápida e livre de erros.
    """
    _pack_ = 1  # Garante que não haja preenchimento de bytes (padding)
    _fields_ = [
        ("status", Status),            # 1 byte
        ("temperatura", ctypes.c_float),     # 4 bytes
        ("aceleracao_x", ctypes.c_float),    # 4 bytes
        ("aceleracao_y", ctypes.c_float),    # 4 bytes
        ("aceleracao_z", ctypes.c_float),    # 4 bytes
        ("giroscopio_x", ctypes.c_float),    # 4 bytes
        ("giroscopio_y", ctypes.c_float),    # 4 bytes
        ("giroscopio_z", ctypes.c_float),    # 4 bytes
        ("pressao", ctypes.c_float),         # 4 bytes
        ("altura", ctypes.c_float),          # 4 bytes
        ("latitude", ctypes.c_float),        # 4 bytes
        ("longitude", ctypes.c_float),       # 4 bytes
        ("velocidade_xy", ctypes.c_float),   # 4 bytes
        ("tensao_bateria", ctypes.c_float),  # 4 bytes (NOVO CAMPO)
        ("crc", ctypes.c_uint16),            # 2 bytes
    ] # Tamanho total = 57 bytes

class RocketData(QObject):
    """
    Classe central que armazena o estado da aplicação.
    Ela contém o último pacote de dados e o histórico para os gráficos.
    Emite um sinal 'data_updated' sempre que novos dados chegam.
    """
    data_updated = pyqtSignal()

    def __init__(self, history_size: int = 200):
        super().__init__()
        self.latest_packet = TelemetryPacket()
        self.history_size = history_size

        # Usamos numpy para eficiência no armazenamento e manipulação de dados numéricos
        self.altitude_history = np.zeros(self.history_size, dtype=float)
        self.accel_x_history = np.zeros(self.history_size, dtype=float)
        self.accel_y_history = np.zeros(self.history_size, dtype=float)
        self.accel_z_history = np.zeros(self.history_size, dtype=float)
        # ... crie outros arrays numpy para os dados que desejar plotar

    def update_from_bytes(self, raw_bytes: bytes):
        """
        Atualiza o estado com um novo pacote de dados a partir de bytes brutos.
        """
        # Converte os bytes recebidos diretamente para o objeto TelemetryPacket
        self.latest_packet = TelemetryPacket.from_buffer_copy(raw_bytes)

        # Adiciona o novo dado no final do array de histórico e remove o mais antigo
        self.altitude_history = np.roll(self.altitude_history, -1)
        self.altitude_history[-1] = self.latest_packet.altura
        
        self.accel_x_history = np.roll(self.accel_x_history, -1)
        self.accel_x_history[-1] = self.latest_packet.aceleracao_x
        
        # ... atualize os outros históricos da mesma forma

        # Notifica toda a aplicação (as Views) que um novo dado está disponível
        self.data_updated.emit()
