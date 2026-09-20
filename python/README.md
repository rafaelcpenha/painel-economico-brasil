````markdown
# Módulo Python — Painel Econômico Brasil

Este diretório contém o código Python responsável por **coletar, tratar e
gerar** o arquivo `data/dados.json` consumido pelo site.

## Estrutura

```
python/
├── notebooks/                         # Exploração interativa (Jupyter)
│   ├── teste.ipynb                    # Teste do ambiente
│   ├── exploracao-bcb.ipynb           # Exploração da API SGS do BCB
│   ├── exploracao-ibge.ipynb          # Exploração da API SIDRA do IBGE
│   ├── exploracao-tesouro.ipynb       # Exploração da API Aria do Tesouro
│   └── exploracao-comex.ipynb         # Exploração da API do Comex Stat
├── scripts/
│   ├── gerar_dados.py                 # Script principal — orquestra a coleta
│   ├── utils.py                       # Funções auxiliares
│   └── coletores/                     # Um módulo por fonte de dados
│       ├── __init__.py
│       ├── bcb.py                     # Banco Central — SGS
│       ├── ibge.py                    # IBGE — SIDRA
│       ├── tesouro.py                 # Tesouro Nacional — Aria
│       └── comex.py                   # Comex Stat — MDIC
└── README.md                          # Este arquivo
````

## Ambiente

O código Python deste projeto requer o ambiente Conda
`painel-economico-brasil`.

### Ativação

```bash
conda activate painel-economico-brasil
```

### Bibliotecas

As principais bibliotecas utilizadas são:

* `requests`
* `pandas`
* `jupyter`

## Como rodar

> **Importante:** o script deve ser executado de dentro de
> `python/scripts/`, para que os imports relativos entre `utils` e
> `coletores` funcionem corretamente.

No terminal:

```bash
cd python/scripts
conda activate painel-economico-brasil
python gerar_dados.py
```

### Saída esperada

O script deve apresentar logs de coleta por fonte, seguidos da confirmação
de gravação do arquivo `data/dados.json`.

## Fontes integradas

| Fonte | Módulo | Status | Séries |
|---|---|---|---|
| Banco Central (SGS) | `coletores/bcb.py` | ✅ | Selic, IPCA, Câmbio, Crédito, Endividamento |
| IBGE (SIDRA) | `coletores/ibge.py` | ✅ | PIB, Consumo (2), FBCF, Export/Import, Agro, Indústria, Serviços, Impostos |
| Tesouro Nacional (Aria) | `coletores/tesouro.py` | ✅ | Resultado Primário, Gasto Público |
| Comex Stat (MDIC) | `coletores/comex.py` | ✅ | Exportações, Importações, Saldo |

**Notas técnicas:**
- **Comex Stat** tem rate limit (~1 chamada/10s). O coletor aguarda entre chamadas.
- **Comparação temporal** varia por fonte: mês a mês (BCB, IBGE), ano a ano (Tesouro, Comex).
- **Percentuais nas variações** são exibidos apenas quando o valor-base é positivo.

## Fontes planejadas

| Fonte                | Módulo futuro          |
| -------------------- | ---------------------- |
| IBGE — PNAD Contínua | `coletores/pnad.py`    |

## Notas técnicas

### Formato de datas

O BCB entrega datas no formato `DD/MM/AAAA`, enquanto o IBGE entrega
períodos trimestrais no formato `AAAAQQ`.

Ambos são convertidos para formatos legíveis antes de serem gravados no
JSON.

### Valores numéricos

Os valores numéricos são sempre armazenados como `float` no JSON, mesmo
quando a API de origem os entrega como `string`.

### Variações

As variações são calculadas pela diferença entre o último e o penúltimo
valor da série.

## Verificação

Após qualquer alteração no código, execute o script para verificar se o
pipeline continua funcionando normalmente:

```bash
cd python/scripts
conda activate painel-economico-brasil
python gerar_dados.py
```
## Higiene

- **`nbstripout`** configurado para remover outputs dos notebooks antes de commit.
- **Timeout** de 20s em todos os coletores.
- **`.gitignore`** exclui dados brutos, ambientes virtuais e checkpoints de Jupyter.
