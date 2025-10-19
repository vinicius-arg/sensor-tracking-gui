# TODO(vinicius)Refatorar o gerenciamento de configurações (baudrates, etc.) 
# Usar a classe QSettings. Isso permitirá salvar a última porta e baudrate selecionados pelo usuário, 
# melhorando a usabilidade.

DEV_MODE = True

APP_NAME = "ZeSTIn"
APP_SUBTITLE = "Zenith's Sensor Telemetry Interface"
DATA_WINDOW_LENGTH = 50

PACKET_QUEUE_MS_TIME = 100
GRAPH_UPDATE_MS_TIME = 100
NOTIFICATION_DISAPPEAR_MS_TIME = 5000

DEFAULT_BAUDRATE = "9600"

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

ROCKET_DATA_MAP: dict[str, list[str]] = {
    "Acceleration": ["accel_{}".format(x) for x in "xyz"],
    "Gyro": ["gyro_{}".format(x) for x in "xyz"],
    "Pressure": ["pressure"],
    "Height": ["height"],
    "Temperature": ["temperature"],
    "GPS": ["longitude", "latitude"],
    "XY Speed": ["speed_xy"]
    }

ROCKET_DATA_ALIAS: dict[str, list[str]] = {
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