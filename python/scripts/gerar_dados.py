# =====================================================
# Script principal: gera data/dados.json com dados reais
# =====================================================

import json
from pathlib import Path

from coletores.bcb import buscar_ultimos_valores as buscar_bcb
from coletores.ibge import buscar_ultimos_valores as buscar_ibge
from coletores.tesouro import buscar_ultimos_valores as buscar_tesouro


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

# (codigo_serie, id_no_json, unidade)
SERIES_TESOURO = [
    ("10.04.1", "resultado-primario", "R$ bi"),
    ("10.03.1", "gasto-publico",      "R$ bi"),
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

def buscar_serie_do_tesouro(codigo: str) -> dict:
    """
    Busca o último valor de uma série do Tesouro e calcula a variação
    ano a ano (mesmo mês do ano anterior).
    """
    valores = buscar_tesouro(codigo, meses_historico=14)

    # Ordena cronologicamente crescente
    valores.sort(key=lambda v: v["data_iso"])

    if len(valores) < 2:
        raise ValueError(f"Tesouro: série {codigo} retornou menos de 2 períodos.")

    atual = valores[-1]
    # Encontra o mesmo mês do ano anterior
    mes_atual = atual["data_iso"][:7]  # "AAAA-MM"
    ano_anterior = str(int(mes_atual[:4]) - 1)  # "AAAA" - 1
    mes_alvo = ano_anterior + mes_atual[4:]  # "AAAA-MM" do ano anterior

    anterior = None
    for v in valores:
        if v["data_iso"][:7] == mes_alvo:
            anterior = v
            break

    if anterior is None:
        raise ValueError(
            f"Tesouro: não encontrado mesmo mês do ano anterior para {codigo}."
        )

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

    # --- Coleta do Tesouro ---
    print("\n🔎 Coletando dados do Tesouro...")
    for codigo, id_indicador, unidade in SERIES_TESOURO:
        resultado = buscar_serie_do_tesouro(codigo)
        print(f"  {id_indicador}: {resultado['valor']:.2f} ({resultado['data']})")

        if not atualizar_indicador(dados, id_indicador, resultado, unidade):
            print(f"  ⚠️  Indicador '{id_indicador}' não encontrado no dados.json.")

    # Grava o arquivo atualizado
    with open(CAMINHO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Arquivo gravado: {CAMINHO_DADOS}")


if __name__ == "__main__":
    gerar_dados()
