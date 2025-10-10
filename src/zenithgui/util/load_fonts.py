import os, sys
from pathlib import Path
from PyQt5.QtGui import QFontDatabase

def load_fonts(*paths: str):
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent.parent

    path = base_path.joinpath(*paths).resolve()
    fonts = os.listdir(path)
    [QFontDatabase.addApplicationFont(str(path.joinpath(font).resolve())) for font in fonts]
