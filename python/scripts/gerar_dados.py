# =====================================================
# Script principal: gera data/dados.json com dados reais
# =====================================================

import json
from pathlib import Path

from coletores.bcb import buscar_ultimos_valores as buscar_bcb
from coletores.ibge import buscar_ultimos_valores as buscar_ibge


# --- Configuração ---

# Caminho para o data/dados.json (relativo à raiz do projeto)
RAIZ_PROJETO = Path(__file__).resolve().parent.parent.parent
CAMINHO_DADOS = RAIZ_PROJETO / "data" / "dados.json"


# --- Catálogo de séries do BCB ---
# (código_sgs, id_no_json, unidade)
SERIES_BCB = [
    (432,   "selic",         "% a.a."),
    (13522, "ipca",          "%"),
    (1,     "cambio",        "R$"),
    (20622, "credito",       "% PIB"),
    (29037, "endividamento", "% renda"),
]

# (categoria, id_no_json, unidade)
SERIES_IBGE = [
    (90707, "pib-mercado",        "% a.a."),
    (93404, "consumo-familias",   "% a.a."),
    (93405, "consumo-governo",    "% a.a."),
    (93406, "fbcf",               "% a.a."),
    (93407, "exportacoes-ibge",   "% a.a."),
    (93408, "importacoes-ibge",   "% a.a."),
    (90687, "agropecuaria",       "% a.a."),
    (90691, "industria",          "% a.a."),
    (90696, "servicos",           "% a.a."),
    (90706, "impostos",           "% a.a."),
]

def buscar_serie_do_bcb(codigo: int) -> dict:
    """
    Busca os últimos 2 valores de uma série do BCB e retorna
    o valor atual e a variação em relação ao anterior.
    """
    valores = buscar_bcb(codigo, quantidade=2)
    atual = valores[-1]
    anterior = valores[-2]

    variacao = atual["valor"] - anterior["valor"]

    return {
        "valor": atual["valor"],
        "data": atual["data"],
        "variacao": variacao,
            "variacao_direcao": "alta" if variacao > 0 else ("baixa" if variacao < 0 else "neutro"),
    }

def buscar_serie_do_ibge(categoria: int) -> dict:
    """
    Busca os últimos 2 trimestres de uma categoria do IBGE e retorna
    o valor atual e a variação em relação ao anterior.
    """
    valores = buscar_ibge(categoria, quantidade_periodos=2)
    atual = valores[-1]
    anterior = valores[-2]

    variacao = atual["valor"] - anterior["valor"]

    return {
        "valor": atual["valor"],
        "data": atual["periodo"],
        "variacao": variacao,
        "variacao_direcao": "alta" if variacao > 0 else ("baixa" if variacao < 0 else "neutro"),
    }

def atualizar_indicador(dados: dict, id_indicador: str, resultado: dict, unidade: str) -> bool:
    """
    Atualiza um indicador no dicionário `dados` com o resultado coletado.
    Retorna True se encontrou, False caso contrário.
    """
    for indicador in dados["indicadores"]:
        if indicador.get("id") == id_indicador:
            indicador["valor"] = resultado["valor"]
            indicador["unidade"] = unidade
            indicador["periodo"] = resultado["data"]
            indicador["variacao"] = {
                "direcao": resultado["variacao_direcao"],
                "texto": f"{abs(resultado['variacao']):.2f}".replace(".", ","),
            }
            return True
    return False


def gerar_dados():
    """
    Coleta os indicadores e grava o data/dados.json.
    """
    # Carrega o dados.json atual (mantém os indicadores fictícios)
    with open(CAMINHO_DADOS, "r", encoding="utf-8") as f:
        dados = json.load(f)

    # --- Coleta do BCB ---
    print("🔎 Coletando dados do BCB...")
    for codigo, id_indicador, unidade in SERIES_BCB:
        resultado = buscar_serie_do_bcb(codigo)
        print(f"  {id_indicador}: {resultado['valor']} ({resultado['data']})")

        if not atualizar_indicador(dados, id_indicador, resultado, unidade):
            print(f"  ⚠️  Indicador '{id_indicador}' não encontrado no dados.json.")

    # --- Coleta do IBGE ---
    print("\n🔎 Coletando dados do IBGE...")
    for categoria, id_indicador, unidade in SERIES_IBGE:
        resultado = buscar_serie_do_ibge(categoria)
        print(f"  {id_indicador}: {resultado['valor']} ({resultado['data']})")

        if not atualizar_indicador(dados, id_indicador, resultado, unidade):
            print(f"  ⚠️  Indicador '{id_indicador}' não encontrado no dados.json.")

    # Grava o arquivo atualizado
    with open(CAMINHO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Arquivo gravado: {CAMINHO_DADOS}")


if __name__ == "__main__":
    gerar_dados()
