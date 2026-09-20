# =====================================================
# Coletor de dados do Banco Central (SGS)
# =====================================================

import requests
from utils import data_bcb_para_iso, valor_bcb_para_float


URL_BASE = "https://api.bcb.gov.br/dados/serie/bcdata.sgs."


def buscar_ultimos_valores(codigo_serie: int, quantidade: int = 2) -> list[dict]:
    """
    Busca os últimos N valores de uma série do SGS.

    Retorna uma lista de dicionários no formato:
        [{"data": "AAAA-MM-DD", "valor": 13.75}, ...]

    Os dados vêm do BCB em DD/MM/AAAA e strings; aqui já são
    convertidos para ISO 8601 e float.
    """
    url = f"{URL_BASE}{codigo_serie}/dados/ultimos/{quantidade}?formato=json"

    resposta = requests.get(url, timeout=20)
    resposta.raise_for_status()  # lança exceção se status != 200

    dados_brutos = resposta.json()

    dados_processados = []
    for item in dados_brutos:
        dados_processados.append({
            "data": data_bcb_para_iso(item["data"]),
            "valor": valor_bcb_para_float(item["valor"]),
        })

    return dados_processados
