from enum import Enum, auto
from dataclasses import dataclass

class PacketType(Enum):
    """Define padronização de tipos de pacotes a serem enviados.
    Enums:
        DATA: Pacotes de dados;
        ERROR: Pacotes de report de erro;
        STATUS: Pacotes de controle.
    """
    DATA = auto()
    ERROR = auto()
    STATUS = auto()

@dataclass(frozen=True)
class Packet:
    type: PacketType
    payload: object
    
    @classmethod
    def as_data(cls, payload: bytes) -> "Packet":
        """Cria um pacote de dados."""
        return cls(PacketType.DATA, payload)

    @classmethod
    def as_error(cls, error_msg: str) -> "Packet":
        """Cria um pacote informando erro."""
        return cls(PacketType.ERROR, error_msg)

    @classmethod
    def as_status(cls, status_msg: str) -> "Packet":
        """Cria um pacote informando status."""        
        return cls(PacketType.STATUS, status_msg)
