import os

from dotenv import load_dotenv

load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL")
LORA_PORT = os.getenv("LORA_PORT")
BAUDRATE = os.getenv("BAUDRATE")