import ctypes
from collections import deque

from zenithgui.config import config

# Nota de Engenharia: A discrepância "Bateria" foi resolvida adicionando o campo
# 'battery'. O firmware do ESP32 precisa ser atualizado para incluir este
# dado na mesma posição. O tamanho total do pacote agora é 57 bytes.

class StatusFlags(ctypes.LittleEndianStructure):
    """Mapeamento de bits para as flags de status.
    """
    _fields_ = [
        ("circuit_on", ctypes.c_uint8, 1),
        ("mpu_on", ctypes.c_uint8, 1),
        ("bmp_on", ctypes.c_uint8, 1),
        ("gps_on", ctypes.c_uint8, 1),
        ("sd_on", ctypes.c_uint8, 1),
        ("reserved", ctypes.c_uint8, 3)
    ]

class Status(ctypes.Union):
    """Classe de união das flags de status.
    """
    _fields_ = [("flags", StatusFlags),
                ("as_byte", ctypes.c_uint8)]

class TelemetryPacket(ctypes.LittleEndianStructure):
    """Representação exata da struct enviada pelo foguete.
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
    """Classe central que armazena o estado da aplicação.
    """
    def __init__(self, history_size: int = 200):
        super().__init__()
        self._latest_packet = TelemetryPacket()
        self._history_size = history_size

        self._setup_data()

    def get_data(self):
        return self._data
    
    def get_latest_packet(self):
        return self._latest_packet

    def _setup_data(self):
        self._data = {
            "status": deque(maxlen=self._history_size),
            "temperature": deque(maxlen=self._history_size),
            "accel_x": deque(maxlen=self._history_size),
            "accel_y": deque(maxlen=self._history_size),
            "accel_z": deque(maxlen=self._history_size),
            "gyro_x": deque(maxlen=self._history_size),
            "gyro_y": deque(maxlen=self._history_size),
            "gyro_z": deque(maxlen=self._history_size),
            "pressure": deque(maxlen=self._history_size),
            "height": deque(maxlen=self._history_size),
            "latitude": deque(maxlen=self._history_size),
            "longitude": deque(maxlen=self._history_size),
            "speed_xy": deque(maxlen=self._history_size),
            "battery": deque(maxlen=self._history_size)
        }

    def _update_field(self, value, field: deque):
        field.append(value)

    def update_data(self, raw_bytes: bytes):
        """Atualiza o estado com um novo pacote de dados a partir de bytes brutos.
        """
        try:
            self._latest_packet = TelemetryPacket.from_buffer_copy(raw_bytes)
        except ValueError as e:
            print(e)

        # Atualização de dados
        for field, _ in TelemetryPacket._fields_:
            if field in config.TRACKABLE_DATA:
                try:
                    value = getattr(self._latest_packet, field)
                    self._update_field(value, self._data[field])
                except KeyError:
                    pass

def main():
    r = RocketData()
    r.update_data(b"weyrutiuboinjmkinuobiyvutyrdyexdfchjgvk124")
    print(r.get_data())

if __name__ == "__main__":
    main()