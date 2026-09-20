# Painel Econômico Brasil

Painel web com os principais indicadores econômicos do Brasil, com foco em
macroeconomia. Os dados são organizados em seis blocos analíticos: política
monetária, atividade econômica, crédito, mercado de trabalho, setor público e
comércio exterior.

## Status

🚧 **Em construção** — v0.5 (dados reais de 4 fontes, higiene do repositório)

## O que já existe

- ✅ **v0.1** — Home inicial publicada
- ✅ **v0.2** — Painel com 16 cards distribuídos em 6 seções temáticas
- ✅ **v0.3** — Arquitetura orientada a dados (JSON + JavaScript)
- ✅ **v0.4** — Integração com BCB e IBGE; subseções; semântica de cores
- ✅ **v0.5** — Integração completa com 4 fontes oficiais:
  - **BCB (SGS)**: Selic, IPCA, Câmbio, Crédito Total, Endividamento
  - **IBGE (SIDRA)**: PIB, Consumo das Famílias, Consumo do Governo,
    FBCF, Exportações (PIB), Importações (PIB), Agropecuária,
    Indústria, Serviços, Impostos Líquidos
  - **Tesouro Nacional (Aria)**: Resultado Primário, Gasto Público
  - **Comex Stat (MDIC)**: Exportações, Importações, Saldo Comercial
  - **Higiene**: `nbstripout` para notebooks; sufixos e percentuais
    nas variações em R$ bi e US$ bi; timeout robusto

**20 dos 22 indicadores** têm dados reais. Os 2 restantes
(Desemprego e PEA, da PNAD Contínua) serão integrados na v0.6.

## Roadmap

- [x] **v0.1** — Estrutura inicial e home publicada
- [x] **v0.2** — Layout em grid de cards por indicador, com seções temáticas
- [x] **v0.3** — Dados manuais via JSON, renderização dinâmica
- [x] **v0.4** — Integração com BCB e IBGE; semântica de cores por polaridade
- [x] **v0.5** — Integração com Tesouro e Comex Stat; higiene do repositório
- [ ] **v0.6** — Integração com PNAD Contínua (desemprego, PEA)
- [ ] **v0.7** — Automação via GitHub Actions
- [ ] **v0.8** — Gráficos de séries históricas (Chart.js)
- [ ] **v0.9** — Treemap de parceiros comerciais
- [ ] **v1.0** — Detalhamento de gasto público e orçamento (livre vs. vinculado)

## Fontes de dados

| Indicador | Fonte | Status |
|---|---|---|
| Taxa Selic | BCB SGS 432 | ✅ Integrado |
| IPCA (12 meses) | BCB SGS 13522 | ✅ Integrado |
| Câmbio (USD/BRL) | BCB SGS 1 | ✅ Integrado |
| Crédito Total (% PIB) | BCB SGS 20622 | ✅ Integrado |
| Endividamento das Famílias | BCB SGS 29037 | ✅ Integrado |
| PIB (variação) | IBGE SIDRA 5932 | ✅ Integrado |
| Consumo das Famílias | IBGE SIDRA 5932 | ✅ Integrado |
| Consumo do Governo | IBGE SIDRA 5932 | ✅ Integrado |
| FBCF | IBGE SIDRA 5932 | ✅ Integrado |
| Exportações (PIB) | IBGE SIDRA 5932 | ✅ Integrado |
| Importações (PIB) | IBGE SIDRA 5932 | ✅ Integrado |
| Agropecuária | IBGE SIDRA 5932 | ✅ Integrado |
| Indústria | IBGE SIDRA 5932 | ✅ Integrado |
| Serviços | IBGE SIDRA 5932 | ✅ Integrado |
| Impostos Líquidos | IBGE SIDRA 5932 | ✅ Integrado |
| Taxa de Desemprego | IBGE PNAD Contínua | ⏳ Pendente |
| PEA | IBGE PNAD Contínua | ⏳ Pendente |
| Gasto Público (União) | Tesouro Nacional | ✅ Integrado |
| Resultado Primário | Tesouro Nacional | ✅ Integrado |
| Exportações (US$ bi) | Comex Stat (MDIC) | ✅ Integrado |
| Importações (US$ bi) | Comex Stat (MDIC) | ✅ Integrado |
| Saldo Comercial | Comex Stat (MDIC) | ✅ Integrado |

## Arquitetura

### Fluxo de dados

```
[APIs oficiais: BCB, IBGE, ...]
│
│ Python (requests)
▼
[python/scripts/gerar_dados.py]
│
│ chama
▼
[python/scripts/coletores/*.py]
│ (bcb.py, ibge.py, ...)
│
│ usa
▼
[python/scripts/utils.py]
│
│ grava
▼
[data/dados.json]
│
│ fetch
▼
[script.js] → [index.html + style.css]
│
▼
[Site publicado no GitHub Pages]

```

### Tecnologias

- **HTML5 / CSS3** — estrutura e apresentação
- **JavaScript** — fetch, DOM, lógica de renderização
- **JSON** — formato de dados
- **Python 3.11** — coleta e tratamento
- **requests, pandas** — bibliotecas Python
- **Conda** — gerenciamento de ambiente
- **Git / GitHub Pages** — versionamento e publicação

## Estrutura do projeto

```
painel-economico-brasil/
├── index.html              # Estrutura da página
├── style.css               # Estilos e design tokens
├── script.js               # Lógica de renderização (fetch + DOM)
├── .gitattributes          # Configuração do nbstripout
├── README.md               # Este arquivo
├── .gitignore
├── data/
│   └── dados.json          # Dados dos indicadores (fonte de verdade do site)
└── python/
    ├── README.md           # Documentação do módulo Python
    ├── notebooks/          # Exploração de APIs (Jupyter)
    └── scripts/
        ├── gerar_dados.py  # Script principal — orquestra a coleta
        ├── utils.py        # Funções auxiliares
        └── coletores/
            ├── __init__.py
            ├── bcb.py      # Banco Central (SGS)
            ├── ibge.py     # IBGE (SIDRA)
            ├── tesouro.py  # Tesouro Nacional (Aria)
            └── comex.py    # Comex Stat (MDIC)
```

## Autor

**Rafael Penha** — estudante de Economia
GitHub: [@rafaelcpenha](https://github.com/rafaelcpenha)

## Licença

Projeto de estudo. Código aberto para fins educacionais.

