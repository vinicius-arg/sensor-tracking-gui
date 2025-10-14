import pyqtgraph as pg

from dataclasses import dataclass
from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QVBoxLayout, QHBoxLayout

@dataclass
class GraphData:
    """Container para os widgets de um único gráfico.
    """
    _id: int
    name: str
    frame: QFrame
    plot_widget: pg.PlotWidget
    curve: pg.PlotDataItem
    current: QLabel

class Graph(QWidget):
    graph_id = 0
    
    INITIAL_VALUE = "0.00"

    def __init__(self, name: str):
        super().__init__()

        self.graph = None
        self.graph_name = name

        self._create_widget()
        self._create_layout()
        self._apply_styles()

        Graph.graph_id += 1

    def get_graph(self):
        return self.graph

    def _create_widget(self):
        self.frame = QFrame()
        self.name = QLabel(self.graph_name)

        self.plotter = pg.PlotWidget()
        self.curve = self.plotter.plot(pen=pg.mkPen(color="purple", width=2))
        self.current = QLabel(self.INITIAL_VALUE)

        self.graph = GraphData(
            _id=self.graph_id,
            name=self.graph_name,
            frame=self.frame,
            plot_widget=self.plotter,
            curve=self.curve,
            current=self.current
            )

    def _create_layout(self):
        self.graph_layout = QVBoxLayout(self.frame)

        self.header_layout = QHBoxLayout()
        self.header_layout.addWidget(self.name)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.current)

        self.graph_layout.addLayout(self.header_layout)
        self.graph_layout.addWidget(self.plotter)
            
    def _apply_styles(self):
        self.frame.setObjectName("GraphFrame")

        self.plotter.showGrid(x=True, y=True, alpha=0.3)
        self.plotter.setYRange(-10, 10)

        self.current.setProperty("class", "currentValue")
