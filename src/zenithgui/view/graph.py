import pyqtgraph as pg

from dataclasses import dataclass
from PyQt5.QtWidgets import QLabel, QFrame

@dataclass
class Graph:
    """Container para os widgets de um único gráfico.
    """
    name: str
    frame: QFrame
    plot_widget: pg.PlotWidget
    curve: pg.PlotDataItem
    current_value_label: QLabel