import serial.tools.list_ports
from zenithgui.model import RocketData
from zenithgui.config import DEV_MODE

class MainModel():
    def __init__(self):
        self._serial_reader = None
        self._rocket = RocketData()

    def connect_to_lora(self, port, baudrate, queue, force=False):
        """Conecta ao LoRa, dispositivo serial, no modo de desenvolvimento conecta-se a
        um módulo de simulação de dados. No modo de produção, conecta-se ao dispositivo
        serial normalmente.

        Args:
            port (str): Porta serial.
            baudrate (int): Baudrate do dispositivo serial.
            queue (Queue): Fila de pacotes.
            force (bool, optional): Forçar conexão (ignora handshake). Falso por padrão.
        """
        from zenithgui.communication import SerialReader, SerialSimulation
        if not self._serial_reader or not self._serial_reader.is_alive():
            # Passando canal de comunicação (queue) para o produtor
            if DEV_MODE:
                self._serial_reader = SerialSimulation(port, baudrate, queue, force)
            else:
                self._serial_reader = SerialReader(port, baudrate, queue, force)
            self._serial_reader.start()

    def stop_tracking(self):
        """Finaliza o monitoramento dos sensores.
        """
        self._serial_reader.disconnect()

    def get_rocket_data(self) -> dict:
        """Obtém o histórico de dados coletados.

        Returns:
            dict: Dicionário contendo dados de cada sensor.
        """
        return self._rocket.get_data()
    
    def update_rocket_data(self, data: bytes):
        """Atualiza dados de sensoriamento baseando-se no último pacote a chegar.

        Args:
            data (bytes): Último pacote a chegar.
        """
        self._rocket.update_data(data)

    def list_available_ports(self) -> list[str]:
        """Lista portas disponíveis no sistema operacional.

        Returns:
            list[str]: Retorna um lista do tipo { port.device[1], ..., port.device[n] }
        """
        ports = serial.tools.list_ports.comports()
        available_ports = []
        if not ports:
            return ["<Nenhuma porta encontrada>"]

        for port in ports:
            #if sys.platform.startswith("win") or "USB" in port.description or "ACM" in port.device:
            available_ports.append(port.device)
        return available_ports
