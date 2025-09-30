import ctypes
import numpy as np
from collections import deque

from zenithgui.config import config

# Nota de Engenharia: A discrepância "Bateria" foi resolvida adicionando o campo
# 'battery'. O firmware do ESP32 precisa ser atualizado para incluir este
# dado na mesma posição. O tamanho total do pacote agora é 57 bytes.

class StatusFlags(ctypes.LittleEndianStructure):
    """ Mapeamento de bitfields para os flags de status. """
    _fields_ = [
        ("circuit_on", ctypes.c_uint8, 1),
        ("mpu_on", ctypes.c_uint8, 1),
        ("bmp_on", ctypes.c_uint8, 1),
        ("gps_on", ctypes.c_uint8, 1),
        ("sd_on", ctypes.c_uint8, 1),
        ("reserved", ctypes.c_uint8, 3)
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
    _pack_ = 1 
    _fields_ = [
        ("status", Status),
        ("temperature", ctypes.c_float),
        ("accel_x", ctypes.c_float),   
        ("accel_y", ctypes.c_float),
        ("accel_z", ctypes.c_float),
        ("gyro_x", ctypes.c_float),
        ("gyro_y", ctypes.c_float),
        ("gyro_z", ctypes.c_float),
        ("pressure", ctypes.c_float),
        ("height", ctypes.c_float),
        ("latitude", ctypes.c_float),
        ("longitude", ctypes.c_float),
        ("speed_xy", ctypes.c_float),
        ("battery", ctypes.c_float),
        ("crc", ctypes.c_uint16),
    ]

class RocketData():
    """
    Classe central que armazena o estado da aplicação.
    Ela contém o último pacote de dados e o histórico para os gráficos.
    Emite um sinal 'data_updated' sempre que novos dados chegam.
    """
    def __init__(self, history_size: int = 200):
        super().__init__()
        self._latest_packet = TelemetryPacket()
        self._history_size = history_size

        self._setup_data()

    def _setup_data(self):
        self._data = {
            "status": np.zeros(self._history_size, dtype=float),
            "temperature": np.zeros(self._history_size, dtype=float),
            "accel_x": np.zeros(self._history_size, dtype=float),
            "accel_y": np.zeros(self._history_size, dtype=float),
            "accel_z": np.zeros(self._history_size, dtype=float),
            "gyro_x": np.zeros(self._history_size, dtype=float),
            "gyro_y": np.zeros(self._history_size, dtype=float),
            "gyro_z": np.zeros(self._history_size, dtype=float),
            "pressure": np.zeros(self._history_size, dtype=float),
            "height": np.zeros(self._history_size, dtype=float),
            "latitude": np.zeros(self._history_size, dtype=float),
            "longitude": np.zeros(self._history_size, dtype=float),
            "speed_xy": np.zeros(self._history_size, dtype=float),
            "battery": np.zeros(self._history_size, dtype=float)
        }

    def _update_field(self, value, field: deque,):
        field.append(value)
        field.popleft()

    def get_data(self):
        return self._data

    def update_data(self, raw_bytes: bytes):
        """
        Atualiza o estado com um novo pacote de dados a partir de bytes brutos.
        """
        self._latest_packet = TelemetryPacket.from_buffer_copy(raw_bytes)

        # Atualização de dados (remove mais antigo)
        for field, field_type in TelemetryPacket._fields_:
            if field in config.TRACKABLE_DATA:
                value = getattr(self._latest_packet, field)
                self._update_field(value, self._data["field"])

        # self._update_field(self._latest_packet.temperature)
        # self._update_field(self._latest_packet.accel_x)
        # self._update_field(self._latest_packet.accel_y)
        # self._update_field(self._latest_packet.accel_z)
        # self._update_field(self._latest_packet.gyro_x)
        # self._update_field(self._latest_packet.gyro_y)
        # self._update_field(self._latest_packet.gyro_z)
        # self._update_field(self._latest_packet.pressure)
        # self._update_field(self._latest_packet.height)
        # self._update_field(self._latest_packet.latitude)
        # self._update_field(self._latest_packet.longitude)
        # self._update_field(self._latest_packet.battery)