# TODO(vinicius)Refatorar o gerenciamento de configurações (baudrates, etc.) 
# Usar a classe QSettings. Isso permitirá salvar a última porta e baudrate selecionados pelo usuário, 
# melhorando a usabilidade.

APP_NAME = "ZeSTIn"
APP_SUBTITLE = "Zenith's Sensor Telemetry Interface"
VERSION = "1.0.0"

DEV_MODE = True

DATA_WINDOW_LEN = 50
TIME_PQUEUE = 100 #ms

SUPPORTED_BAUDRATES = [
    "1200", 
    "2400", 
    "4800", 
    "9600", 
    "19200", 
    "38400", 
    "57600", 
    "115200", 
    "230400", 
    "460800", 
    "921600"
    ]

DEFAULT_BAUDRATE = "9600"

TRACKABLE_DATA = [
    "temperature", 
    "pressure",
    "height",
    "accel_x",
    "accel_y",
    "accel_z",
    "gyro_x",
    "gyro_y",
    "gyro_z",
    "latitude",
    "longitude",
    "speed_xy"
    ]

DATA_MAP: dict[str, list[str]] = {
    "Acceleration": ["accel_x", "accel_y", "accel_z"],
    "Gyro": ["gyro_x", "gyro_y", "gyro_z"],
    "Pressure": ["pressure"],
    "Height": ["height"],
    "Temperature": ["temperature"],
    "GPS": ["longitude", "latitude"],
    "XY Speed": ["speed_xy"]
    }

DATA_ALIAS: dict[str, list[str]] = {
    "accel_x": "Acceleration_x",
    "accel_y": "Acceleration_y",
    "accel_z": "Acceleration_z",
    "gyro_x": "Gyroscope_x",
    "gyro_y": "Gyroscope_y",
    "gyro_z": "Gyroscope_z",
    "pressure": "Pressure",
    "height": "Height",
    "temperature": "Temperature",
    "longitude": "Longitude",
    "latitude": "Latitude",
    "speed_xy": "XY Speed"
    }