# =====================================================
# Teste de ambiente — Painel Econômico Brasil
# Verifica se o Python do ambiente Conda está funcionando
# =====================================================

import sys
import requests
import pandas as pd

print("🐍 Python está funcionando!")
print(f"Versão do Python: {sys.version}")
print(f"Localização: {sys.executable}")
print()
print(f"requests  → versão {requests.__version__}")
print(f"pandas    → versão {pd.__version__}")
print()

# Teste rápido: chamada HTTP ao site do Banco Central
try:
    resposta = requests.get("https://www.bcb.gov.br", timeout=5)
    print(f"✅ Conexão com BCB: status HTTP {resposta.status_code}")
except Exception as e:
    print(f"❌ Erro ao conectar: {e}")
