import os

from PyQt5.QtGui import QFontDatabase

from zenithgui.config import Config

class ThemeUtils:
    @staticmethod
    def setup_styles() -> str:
        """Importa estilos para aplicação. Modifique a função para suportar estilos divididos
        em vários arquivos, caso necessário. Após essa função chame *apply_styles*.

        Returns:
            str: Arquivo de estilos lido e pronto para aplicar.
        """
        from zenithgui.util import PathUtils

        style_path = PathUtils.resource_path(*Config.PATH["styles"])

        # Importação dos estilos .qss
        with style_path.open("r", encoding="utf-8") as f:
            style_file = f.read()

        return style_file


    @staticmethod
    def setup_fonts():
        """Importa fontes para a aplicação.
        """
        from zenithgui.util import PathUtils

        font_path = PathUtils.resource_path(*Config.PATH["font"])

        path = font_path.resolve()
        fonts = os.listdir(path)
        [QFontDatabase.addApplicationFont(str(path.joinpath(font).resolve())) for font in fonts]
    

    @staticmethod
    def find_icon():
        from zenithgui.util import PathUtils

        return PathUtils.resource_path("assets", "images", "scooby.png")


    @staticmethod
    def apply_styles(window, style):
        """Aplica estilos *style* à janela *window* especificada.

        Args:
            window (QWidget): Widget de janela.
            style (str): Arquivo de estilos lido.
        """
        window.setStyleSheet(style)


    @staticmethod
    def setup_and_apply_stylesheets(window):
        stylesheet = ThemeUtils.setup_styles()
        ThemeUtils.apply_styles(window, stylesheet)