import sys
import inspect

from pathlib import Path

def resource_path(*paths: str) -> Path:
    """
    Retorna o caminho absoluto de um recurso.
    Funciona tanto no modo desenvolvimento quanto após empacotar com PyInstaller.
    """
    caller_file = inspect.stack()[1].filename

    if "main.py" not in caller_file:
        print("**resource_path() deve ser chamada apenas por src/zenithgui/main.py") 

    if getattr(sys, 'frozen', False):  # se estiver rodando como executável
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent.parent  # src/zenithgui

    return base_path.joinpath(*paths)