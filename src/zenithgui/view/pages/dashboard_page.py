import pyqtgraph as pg
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QCheckBox, QFrame, QGridLayout
from PyQt5.QtCore import pyqtSignal

from zenithgui.view.graph import Graph
from zenithgui import config

class DashboardPage(QWidget):
    stop_tracking = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#1e1e1e"))
        self.setPalette(palette)

        self.graphs: dict[str, Graph] = {}
        self.sensors_to_plot = config.TRACKABLE_DATA

        self._load_sensors()
        self._create_widgets()
        self._create_layouts()
        self._connect_signals()
    
    def _load_sensors(self):
        self.sensors: dict[str, list[str]] = {
            "Acceleration": ["accel_x", "accel_y", "accel_z"],
            "Gyro": ["gyro_x", "gyro_y", "gyro_z"],
            "Pressure": ["pressure"],
            "Height": ["height"],
            "Temperature": ["temperature"],
            "GPS": ["longitude", "latitude"],
            "XY Speed": ["speed_xy"]
            }

    def _create_widgets(self):
        self.title = QLabel("NOME")
        self.subtitle = QLabel("Zenith's Sensors Telemetry Interface")
        self.subtitle.setWordWrap(True)
        self.subtitle.setObjectName("AppName")
        self.sidebar = QFrame()
        self.sidebar.setObjectName("SideBar")

        self.sensors_buttons = []
        for sensor in ["All sensors", *self.sensors.keys()]:
            self.sensors_buttons.append(QPushButton(sensor))
            self.sensors_buttons[-1].setProperty("class", "sidebarButton")

        self.start_btn = QPushButton("Start tracking")
        self.stop_btn = QPushButton("Stop")
        self.record_checkbox = QCheckBox("Record samples")
        self.save_path = QLineEdit("~/path/to/recordings")

    def _create_layouts(self):
        # Sidebar (com os sensores)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(15, 15, 15, 15)
        self.sidebar_layout.addWidget(self.title)
        self.sidebar_layout.addWidget(self.subtitle)

        for sidebar_btn in self.sensors_buttons:
            self.sidebar_layout.addWidget(sidebar_btn)
        
        # Conteúdo principal da tela
        self.main_content = QVBoxLayout()

        self.control_bar = QHBoxLayout()
        self.control_bar.addWidget(self.start_btn)
        self.control_bar.addWidget(self.stop_btn)
        self.control_bar.addWidget(self.record_checkbox)
        self.control_bar.addWidget(self.save_path)
        
        self._create_graphs()

        self.main_content.addLayout(self.control_bar, stretch=1)
        self.main_content.addLayout(self.graph_grid, stretch=5)

        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.sidebar, stretch=1)
        self.main_layout.addLayout(self.main_content, stretch=4)
        
        self.setLayout(self.main_layout)

    def _create_graphs(self):
        self.graph_grid = QGridLayout()
        self.graph_grid.setSpacing(15)

        num_columns = 3
        for i, sensor_name in enumerate(self.sensors_to_plot):
            # Widgets
            frame = QFrame()
            frame.setObjectName("GraphFrame")
            graph_layout = QVBoxLayout(frame)

            name_label = QLabel(sensor_name.replace("_", " ").title())
            expand_btn = QPushButton("Expand")
            
            plot_widget = pg.PlotWidget()
            plot_widget.showGrid(x=True, y=True, alpha=0.3)
            plot_widget.setYRange(-10, 10)
            curve = plot_widget.plot(pen=pg.mkPen(color="purple", width=2))
            
            current_value_label = QLabel("0.00")

            # Layout interno
            header_layout = QHBoxLayout()
            header_layout.addWidget(name_label)
            header_layout.addStretch()
            header_layout.addWidget(expand_btn)
            
            graph_layout.addLayout(header_layout)
            graph_layout.addWidget(plot_widget)
            graph_layout.addWidget(current_value_label)

            # Esquematização do grid
            row, col = divmod(i, num_columns)
            self.graph_grid.addWidget(frame, row, col)

            self.graphs[sensor_name] = Graph(
                name=sensor_name,
                frame=frame,
                plot_widget=plot_widget,
                curve=curve,
                current_value_label=current_value_label
                )

    def _connect_signals(self):
        for sidebar_btn in self.sensors_buttons:
            sidebar_btn.clicked.connect(self.show_sensor_details)

        self.stop_btn.pressed.connect(self.stop_tracking.emit)

    def update_data(self, rocket_data: dict):
        for name, data in rocket_data.items():
            if name in self.graphs:
                graph_object = self.graphs[name]                
                graph_object.curve.setData(data) # Atualiza o gráfico
                
                if data: # Atualiza último valor
                    last_value = data[-1]
                    graph_object.current_value_label.setText(f"{last_value:.2f}")

    def show_sensor_details(self):
        ...