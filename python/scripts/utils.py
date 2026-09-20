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

def periodo_ibge_para_texto(periodo_ibge: str) -> str:
    """
    Converte período trimestral do IBGE (formato AAAAQQ) para texto legível.

    Exemplo:
        "202602" → "2º tri/2026"
        "202503" → "3º tri/2025"
    """
    ano = periodo_ibge[:4]
    trimestre = int(periodo_ibge[4:])
    return f"{trimestre}º tri/{ano}"

def data_tesouro_para_texto(data_iso: str) -> str:
    """
    Converte data ISO 8601 do Tesouro para texto legível (Mmm/AAAA).

    Exemplo:
        "2026-07-01T00:00:00.000Z" → "Jul/2026"
    """
    # Pega só a parte "AAAA-MM-DD" (primeiros 10 caracteres)
    dt = datetime.strptime(data_iso[:10], "%Y-%m-%d")

    meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
             "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

    return f"{meses[dt.month - 1]}/{dt.year}"

def meses_atras(n: int) -> str:
    """
    Retorna o mês que está N meses atrás do mês atual, no formato MM/AAAA.

    Usa aritmética de meses (ano * 12 + mês), evitando aproximações com dias.
    """
    hoje = datetime.today()
    mes_total = hoje.year * 12 + (hoje.month - 1) - n
    ano = mes_total // 12
    mes = (mes_total % 12) + 1
    return f"{mes:02d}/{ano}"
