# tests/test_backend.py

# --- INÍCIO DO BLOCO DE CONFIGURAÇÃO DE PATH ---
import sys
import os

# Adiciona o diretório raiz do projeto (a pasta acima de 'tests') ao path do Python
# Isso permite que o script encontre a pasta 'zenithgui'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
# --- FIM DO BLOCO DE CONFIGURAÇÃO DE PATH ---

# Agora as importações do seu projeto funcionarão
import time
from zenithgui.controller import MainController

# test_backend.py
import time
from zenithgui.controller import MainController

# --- Funções (slots) para receber os sinais ---
def on_status_change(message, is_active):
    print(f"[STATUS] Mensagem: '{message}', Ativo: {is_active}")

def on_data_update():
    # Acessa os dados mais recentes através do controller
    latest_altitude = controller.rocket_data.latest_packet.altura
    latest_accel_z = controller.rocket_data.latest_packet.aceleracao_z
    print(f"-> Novo Dado Recebido! Altitude: {latest_altitude:.2f} m, Acel Z: {latest_accel_z:.2f} m/s²")

if __name__ == "__main__":
    print("--- INICIANDO TESTE DO BACKEND EM MODO SIMULADOR ---")
    
    # 1. Instancia o controller em modo de simulação
    controller = MainController(use_simulator=True)
    
    # 2. Conecta os sinais do backend às nossas funções de teste
    controller.reader.status_changed.connect(on_status_change)
    controller.rocket_data.data_updated.connect(on_data_update)
    
    # 3. Inicia a simulação
    controller.start_simulation()
    
    # Deixa o backend rodar por 5 segundos
    # (Em uma aplicação real, o loop de eventos da UI faria isso)
    try:
        time.sleep(5)
    except KeyboardInterrupt:
        pass
    
    # 4. Para a simulação
    print("\n--- PARANDO SIMULAÇÃO ---")
    controller.stop_simulation()
    
    # Espera a thread do leitor/simulador fechar
    controller.reader.wait()
    
    print("--- TESTE DO BACKEND CONCLUÍDO ---")

