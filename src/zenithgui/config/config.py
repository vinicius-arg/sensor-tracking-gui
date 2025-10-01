# TODO(vinicius)Refatorar o gerenciamento de configurações (baudrates, etc.) 
# Usar a classe QSettings. Isso permitirá salvar a última porta e baudrate selecionados pelo usuário, 
# melhorando a usabilidade.

DEV_MODE = True

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
    "accel_x",
    "accel_y",
    "accel_z",
    "gyro_x",
    "gyro_y",
    "gyro_z",
    "pressure",
    "height",
    "latitude",
    "longitude",
    "speed_xy"
    ]
