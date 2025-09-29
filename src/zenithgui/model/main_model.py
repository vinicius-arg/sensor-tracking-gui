import serial.tools.list_ports
import sys

class MainModel():
    def connect_to_lora(self, port, brate):
        # TODO Implementar
        return True, "msg"
    
    def list_available_ports(self):
        """
        Verifica o sistema e retorna uma lista de portas seriais disponíveis.
        Retorna uma lista: [port.device..1, ..., port.device..n]
        """
        ports = serial.tools.list_ports.comports()
        available_ports = []
        if not ports:
            return ["<Nenhuma porta encontrada>"]

        for port in ports:
            #if sys.platform.startswith("win") or "USB" in port.description or "ACM" in port.device:
            available_ports.append(port.device)
            
        return available_ports
