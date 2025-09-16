# check_env.py
import sys
import os

print("--- VERIFICAÇÃO DE AMBIENTE PYTHON ---")

# 1. Qual executável Python está rodando este script?
print(f"\n[EXECUTÁVEL ATUAL]:")
print(sys.executable)

# 2. Quais pastas o Python está usando para encontrar módulos? (sys.path)
print("\n[PYTHONPATH ATUAL (sys.path)]:")
for path in sys.path:
    print(f"  - {path}")

# 3. Tentativa de importar uma dependência externa
try:
    import crc
    print("\n[DEPENDÊNCIA EXTERNA]: OK - 'crc' importado com sucesso.")
except ImportError:
    print("\n[DEPENDÊNCIA EXTERNA]: FALHA - Não foi possível importar 'crc'.")

# 4. Tentativa de importar um módulo do seu projeto
try:
    # Adicionamos 'src' ao path para simular o que o VS Code deveria fazer
    # Isso nos ajuda a isolar o problema
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    from zenithgui.model import TelemetryPacket
    print("[MÓDULO DO PROJETO]: OK - 'TelemetryPacket' importado com sucesso.")
except ImportError as e:
    print(f"[MÓDULO DO PROJETO]: FALHA - Não foi possível importar 'TelemetryPacket'. Erro: {e}")

print("\n--- FIM DA VERIFICAÇÃO ---")