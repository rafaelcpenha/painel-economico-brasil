# =====================================================
# Coletor de dados do Comex Stat (MDIC)
# =====================================================

import time
import requests
from datetime import datetime
from utils import meses_atras, requisitar_com_retry


URL_BASE = "https://api-comexstat.mdic.gov.br/general"

# Meses de histórico a pedir (para comparação ano a ano)
MESES_HISTORICO = 14


def _formatar_mes_para_texto(ano: str, mes: str) -> str:
    """
    Converte ano (AAAA) e mês (MM) em texto legível (Mmm/AAAA).
    Exemplo: ("2026", "07") → "Jul/2026"
    """
    meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
             "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    return f"{meses[int(mes) - 1]}/{ano}"


def _buscar_mensal(flow: str) -> list[dict]:
    """
    Busca os valores mensais de exportação ou importação.

    flow: "export" ou "import"
    Retorna lista de {periodo_iso, periodo_texto, valor_bi} ordenada asc.

    A API do Comex Stat tem rate limit (~1 chamada a cada 10 segundos).
    Por isso, aguardamos antes de cada chamada.
    """
    # Pausa preventiva (a API aceita ~1 chamada/10s)
    print(f"  Aguardando 10s antes de consultar {flow}...")
    time.sleep(10)

    data_inicio = meses_atras(MESES_HISTORICO)
    partes = data_inicio.split("/")
    data_inicio_iso = f"{partes[1]}-{partes[0]}"

    hoje = datetime.today()
    to_iso = f"{hoje.year}-{hoje.month:02d}"

    body = {
        "flow": flow,
        "monthDetail": True,
        "period": {"from": data_inicio_iso, "to": to_iso},
        "filters": [],
        "details": [],
        "metrics": ["metricFOB"],
    }

    # Tenta até 3 vezes em caso de rate limit
    for tentativa in range(3):
        resposta = requisitar_com_retry(URL_BASE, method="post", json=body, timeout=30)

        if resposta.status_code == 429:
            print(f"  ⏳ Rate limit atingido. Aguardando 15s... (tentativa {tentativa + 1}/3)")
            time.sleep(15)
            continue

        resposta.raise_for_status()
        break
    else:
        raise RuntimeError("Comex Stat: rate limit persistente após 3 tentativas.")

    dados = resposta.json()
    lista = dados.get("data", {}).get("list", [])

    dados_processados = []
    for item in lista:
        valor_bruto = float(item["metricFOB"])
        dados_processados.append({
            "periodo_iso": f"{item['year']}-{item['monthNumber']}",
            "periodo_texto": _formatar_mes_para_texto(item["year"], item["monthNumber"]),
            "valor_bi": valor_bruto / 1_000_000_000,
        })

    dados_processados.sort(key=lambda x: x["periodo_iso"])
    return dados_processados


def buscar_exportacoes() -> list[dict]:
    """Busca os valores mensais de exportações (US$ bi)."""
    return _buscar_mensal("export")


def buscar_importacoes() -> list[dict]:
    """Busca os valores mensais de importações (US$ bi)."""
    return _buscar_mensal("import")
