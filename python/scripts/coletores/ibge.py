# =====================================================
# Coletor de dados do IBGE (SIDRA — API de agregados)
# =====================================================

import requests
from utils import periodo_ibge_para_texto


URL_BASE = "https://servicodados.ibge.gov.br/api/v3/agregados"


# Tabela 5932 = Taxa de variação do PIB trimestral
TABELA_PIB = "5932"
VARIAVEL_TAXA_TRIMESTRAL = "6561"
LOCALIDADE_BRASIL = "N1[all]"
CLASSIFICACAO_SETORES = "11255"


def buscar_ultimos_valores(
    categoria: int,
    tabela: str = TABELA_PIB,
    variavel: str = VARIAVEL_TAXA_TRIMESTRAL,
    quantidade_periodos: int = 2,
) -> list[dict]:
    """
    Busca os últimos N valores de uma categoria (setor ou componente)
    da tabela de PIB trimestral do IBGE.

    Retorna uma lista de dicionários no formato:
        [{"periodo": "1º tri/2026", "valor": 1.8}, ...]

    Os dados vêm do IBGE com período em AAAAQQ e valores em string;
    aqui já são convertidos.
    """
    url = (
        f"{URL_BASE}/{tabela}"
        f"/periodos/-{quantidade_periodos}"
        f"/variaveis/{variavel}"
        f"?localidades={LOCALIDADE_BRASIL}"
        f"&classificacao={CLASSIFICACAO_SETORES}[{categoria}]"
    )

    resposta = requests.get(url, timeout=20)
    resposta.raise_for_status()

    dados_brutos = resposta.json()

    # Estrutura: lista com 1 variável → dentro, "resultados" com 1 item
    resultados = dados_brutos[0]["resultados"]
    if not resultados:
        raise ValueError(f"Nenhum resultado retornado para categoria {categoria}.")

    serie_bruta = resultados[0]["series"][0]["serie"]

    dados_processados = []
    for periodo_ibge, valor_str in serie_bruta.items():
        dados_processados.append({
            "periodo": periodo_ibge_para_texto(periodo_ibge),
            "valor": float(valor_str),
        })

    return dados_processados
