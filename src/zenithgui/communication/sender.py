from zenithgui.communication.packet import Packet
from queue import Queue

class Sender:
    """Classe responsável por envio de pacotes a partir da leitura da porta serial.
    """
    @staticmethod
    def send_packet_with_note(queue: Queue, msg: str, packet: Packet):
        """Envia pacotes em conjunto com algum outro pacote de notificação.

        Args:
            queue (Queue): Fila de pacotes.
            msg (str): Mensagem a ser posta no pacote de notificação.
            packet (Packet): Pacote de dados/erro a ser enviado a priori.
        """
        note_packet = Packet.as_status(msg)
        queue.put(note_packet)
        queue.put(packet)

    @staticmethod
    def send_packet(queue: Queue, packet: Packet):
        """Envia pacotes quaisquer para o presenter.

        Args:
            queue (Queue): Fila de pacotes.
            packet (Packet): Pacote de dados/informação/erro a ser enviado.
        """
        queue.put(packet)