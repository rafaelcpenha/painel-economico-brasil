# =====================================================
# Utilitários comuns para o projeto Painel Econômico Brasil
# =====================================================

from datetime import datetime


def data_bcb_para_iso(data_bcb: str) -> str:
    """
    Converte data do formato do BCB (DD/MM/AAAA) para ISO 8601 (AAAA-MM-DD).

    Exemplo:
        "04/11/2026" → "2026-11-04"
    """
    dt = datetime.strptime(data_bcb, "%d/%m/%Y")
    return dt.strftime("%Y-%m-%d")


def valor_bcb_para_float(valor_bcb: str) -> float:
    """
    Converte valor do BCB (string, com ponto decimal) para float.

    Exemplo:
        "13.75" → 13.75
    """
    return float(valor_bcb)
