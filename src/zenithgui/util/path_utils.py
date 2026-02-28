import sys

from pathlib import Path

class PathUtils:
    @staticmethod
    def resource_path(*paths: str) -> Path:
        """
        Retorna o caminho absoluto de um recurso.
        Funciona tanto no modo desenvolvimento quanto após empacotar com PyInstaller.
        """
        if getattr(sys, 'frozen', False):  # Rodando como executável
            base_path = Path(sys._MEIPASS)
        else:
            base_path = Path(__file__).resolve().parent.parent  # src/zenithgui

        return base_path.joinpath(*paths)
    