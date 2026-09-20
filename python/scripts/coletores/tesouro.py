# =====================================================
# Coletor de dados do Tesouro Nacional (API Aria)
# =====================================================

import requests
from datetime import datetime
from utils import data_tesouro_para_texto, meses_atras


URL_BASE = "https://apiapex.tesouro.gov.br/aria/v1/series-temporais/custom"

# Temas disponíveis no RTN:
#   10 → Tabela 1.2 (Resultado Fiscal do Governo Central)
#   13 → Tabela 1.3 (Investimentos)
#   20 → Tabela 1.4 (Custeio Administrativo)
TEMA_RESULTADO_FISCAL = 10





def buscar_ultimos_valores(
    codigo_serie: str,
    tema: int = TEMA_RESULTADO_FISCAL,
    meses_historico: int = 14,
) -> list[dict]:
    """
    Busca os últimos N meses de uma série do Tesouro (API Aria).

    Retorna uma lista de dicionários no formato:
        [{"periodo": "Jul/2026", "valor": 10.78}, ...]

    Valores vêm em R$ milhões; são convertidos para R$ bilhões (÷ 1000).
    Datas vêm em ISO 8601 com timestamp; são convertidas para "Mmm/AAAA".
    """
    data_inicio = meses_atras(meses_historico)

    url = f"{URL_BASE}/resultado-fiscal"
    params = {
        "tema": tema,
        "codigo_da_serie": codigo_serie,
        "data_inicio": data_inicio,
    }

    resposta = requests.get(url, params=params, timeout=15)
    resposta.raise_for_status()

    dados_brutos = resposta.json()
    registros = dados_brutos.get("registros", [])

    dados_processados = []
    for reg in registros:
        dados_processados.append({
            "periodo": data_tesouro_para_texto(reg["data"]),
            "valor": float(reg["valor"]) / 1000,  # R$ milhões → R$ bilhões
            "data_iso": reg["data"][:10],          # guardamos também o ISO, útil
        })

    return dados_processados
