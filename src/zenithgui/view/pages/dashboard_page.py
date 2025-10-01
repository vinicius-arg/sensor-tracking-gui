import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget

import random
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QCheckBox, QFrame, QGridLayout, QDialog
)

from PyQt5.QtCore import Qt, QTimer

# class GraphData():
#     def __init__(self):
#         self.name
#         self.data_remetent
#         self.is_active
#         self.latest_data
#         self.plot

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()

        self.load_sensors(sensors=...)
        self._create_widgets()
        self._create_layouts()
        self._connect_signals()
    
    def load_sensors(self, sensors: list):
        self.sensors = ["Acceleration", "Gyro", "Pressure", "Height", "Temperature", "GPS", "XY Speed"]

    def _create_widgets(self):
        self.title = QLabel("Zenith's Sensors Telemetry Interface")
        self.title.setObjectName("AppName")

        self.sensors_buttons = []
        for sensor in ["All sensors", *self.sensors]:
            self.sensors_buttons.append(QPushButton(sensor))
            self.sensors_buttons[-1].setProperty("class", "sidebarButton")

        self.start_btn = QPushButton("Start tracking")
        self.stop_btn = QPushButton("Stop")
        self.record_checkbox = QCheckBox("Record samples")
        self.save_path = QLineEdit("~/path/to/recordings")


    def _create_layouts(self):
        # Sidebar (com os sensores)
        self.sidebar_layout = QVBoxLayout()
        self.sidebar_layout.setContentsMargins(15, 15, 15, 15)
        self.sidebar_layout
        self.sidebar_layout.addWidget(self.title)

        for sidebar_btn in self.sensors_buttons:
            self.sidebar_layout.addWidget(sidebar_btn)

        # Conteúdo principal da tela
        self.main_content = QVBoxLayout()

        # ---- Painel de controle
        self.control_bar = QHBoxLayout()
        self.control_bar.addWidget(self.start_btn)
        self.control_bar.addWidget(self.stop_btn)
        self.control_bar.addWidget(self.record_checkbox)
        self.control_bar.addWidget(self.save_path)

        # ---- Gráficos
        self.graph_grid = QGridLayout()
        self.graph_grid.setSpacing(15)

        # for sensor in self.sensors:
        #     self.graph_name = QLabel(sensor.name)
        #     self.data_remetent = QLabel(sensor.font)
        #     ...



        self.main_content.addLayout(self.control_bar, stretch=1)
        self.main_content.addLayout(self.graph_grid, stretch=5)

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.sidebar_layout, stretch=1)
        self.main_layout.addLayout(self.main_content, stretch=6)
        
        self.setLayout(self.main_layout)

    def _connect_signals(self):
        for sidebar_btn in self.sensors_buttons:
            sidebar_btn.clicked.connect(self.show_sensor_details)

        # # ==== Grid de sensores ====
        # self.plots = []  # guardo os gráficos aqui
        # grid = QGridLayout()
        # grid.setSpacing(15)

        # for i in range(6):
        #     sensor_frame = QFrame()
        #     sensor_frame.setStyleSheet("background-color: #3c3c3c; border-radius: 8px;")
        #     sensor_layout = QVBoxLayout(sensor_frame)
        #     sensor_layout.setContentsMargins(10, 10, 10, 10)

        #     # Layout para o título e o botão na mesma linha
        #     header_layout = QHBoxLayout()
        #     sensor_label = QLabel(f"Sensor {i+1} 🔴")
        #     sensor_label.setStyleSheet("color: white; font-weight: bold;")
            
        #     # Botão para expandir
        #     expand_button = QPushButton("Expandir")
        #     expand_button.setFixedWidth(80)
            
        #     # A MÁGICA ACONTECE AQUI:
        #     # Usamos uma função lambda para "capturar" o valor atual de `i`.
        #     # Sem o `idx=i`, o lambda usaria o último valor de `i` no loop (5) para todos os botões.
        #     expand_button.clicked.connect(lambda _, idx=i: self.show_sensor_details(idx))

        #     header_layout.addWidget(sensor_label)
        #     header_layout.addStretch()
        #     header_layout.addWidget(expand_button)
            
        #     sensor_layout.addLayout(header_layout)

        #     plot_widget = pg.PlotWidget()
        #     plot_widget.setBackground("#3c3c3c")
        #     plot_widget.showGrid(x=True, y=True, alpha=0.3)
        #     plot_widget.setYRange(-10, 10)
        #     curve = plot_widget.plot(pen=pg.mkPen(color="yellow", width=2))

        #     # Vamos guardar a curva e uma lista para os dados
        #     self.plots.append((curve, [])) 
        #     sensor_layout.addWidget(plot_widget)

        #     grid.addWidget(sensor_frame, i // 3, i % 3)

        # content.addLayout(grid)

        # # ===== Monta tudo =====
        # main_layout.addWidget(sidebar)
        # main_layout.addLayout(content)

        # # ===== Timer para simular dados =====
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.update_data)
        # self.timer.start(200)  # atualiza a cada 200 ms

    def update_data(self):
        """Simula dados chegando dos sensores"""
        for curve, data in self.plots:
            if len(data) > 50:  # mantém só 50 pontos
                data.pop(0)
            data.append(random.uniform(-8, 8))  # dado fake
            curve.setData(data)

    def show_sensor_details(self, sensor_index):
        """Mostra o gráfico de um sensor específico em uma nova janela."""
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Gráfico Detalhado - Sensor {sensor_index + 1}")
        dialog.setGeometry(200, 100, 800, 600) # Ajuste o tamanho se desejar

        # 1. Crie um NOVO PlotWidget para o diálogo
        #    É melhor criar um novo do que tentar "mover" o original.
        big_plot_widget = pg.PlotWidget(self)
        big_plot_widget.setBackground("#3c3c3c")
        big_plot_widget.showGrid(x=True, y=True, alpha=0.5)
        big_plot_widget.setTitle(f"Dados do Sensor {sensor_index + 1}", color="white", size="14pt")
        
        # Configure eixos, etc., se desejar
        label_style = {'color': '#AAAAAA', 'font-size': '10pt'}
        big_plot_widget.getAxis('left').setLabel('Valores', **label_style)
        big_plot_widget.getAxis('bottom').setLabel('Tempo (amostras)', **label_style)

        # 2. Recupere os dados do sensor específico que já estão guardados
        #    Lembre-se que self.plots guarda uma tupla (curve, data_list)
        #    Acessamos a lista de dados pelo índice [1] da tupla.
        try:
            dados_do_sensor = self.plots[sensor_index][1]
        except IndexError:
            print(f"Erro: não foram encontrados dados para o sensor de índice {sensor_index}")
            return

        # 3. Plote os dados existentes no NOVO widget do diálogo
        #    Você pode até usar uma cor ou estilo diferente para o gráfico grande.
        big_curve = big_plot_widget.plot(
            dados_do_sensor, 
            pen=pg.mkPen(color="#00D0FF", width=3) # Um ciano vibrante
        )

        # 4. Adicione o widget do gráfico ao layout do diálogo
        layout = QVBoxLayout()
        layout.addWidget(big_plot_widget)
        dialog.setLayout(layout)

        # Lembre-se da nossa conversa anterior: use show() e guarde a referência!
        self.graph_windows.append(dialog)
        dialog.show()