# =====================================================
# Script principal: gera data/dados.json com dados reais
# =====================================================

import json
from pathlib import Path

from coletores.bcb import buscar_ultimos_valores


# --- Configuração ---

# Caminho para o data/dados.json (relativo à raiz do projeto)
RAIZ_PROJETO = Path(__file__).resolve().parent.parent.parent
CAMINHO_DADOS = RAIZ_PROJETO / "data" / "dados.json"


# --- Catálogo de séries do BCB ---
# (código_sgs, id_no_json, unidade)
SERIES_BCB = [
    (432,   "selic",  "% a.a."),
    (13522, "ipca",   "%"),
    (1,     "cambio", "R$"),
]


def buscar_serie_do_bcb(codigo: int) -> dict:
    """
    Busca os últimos 2 valores de uma série do BCB e retorna
    o valor atual e a variação em relação ao anterior.
    """
    valores = buscar_ultimos_valores(codigo, quantidade=2)
    atual = valores[-1]
    anterior = valores[-2]

    variacao = atual["valor"] - anterior["valor"]

    return {
        "valor": atual["valor"],
        "data": atual["data"],
        "variacao": variacao,
        "variacao_direcao": "alta" if variacao >= 0 else "baixa",
    }


def gerar_dados():
    """
    Coleta os indicadores e grava o data/dados.json.
    """
    print("🔎 Coletando dados do BCB...")

    # Carrega o dados.json atual (mantém os indicadores fictícios)
    with open(CAMINHO_DADOS, "r", encoding="utf-8") as f:
        dados = json.load(f)

    # Atualiza apenas os indicadores que temos coleta real
    for codigo, id_indicador, unidade in SERIES_BCB:
        resultado = buscar_serie_do_bcb(codigo)
        print(f"  {id_indicador}: {resultado['valor']} ({resultado['data']})")

        # Encontra o indicador no JSON pelo id
        for indicador in dados["indicadores"]:
            if indicador["id"] == id_indicador:
                indicador["valor"] = resultado["valor"]
                indicador["unidade"] = unidade
                indicador["periodo"] = resultado["data"]
                indicador["variacao"] = {
                    "direcao": resultado["variacao_direcao"],
                    "texto": f"{abs(resultado['variacao']):.2f}",
                }
                break

    # Grava o arquivo atualizado
    with open(CAMINHO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    print(f"✅ Arquivo gravado: {CAMINHO_DADOS}")


if __name__ == "__main__":
    gerar_dados()
