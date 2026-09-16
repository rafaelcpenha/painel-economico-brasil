# Painel Econômico Brasil

Painel web com os principais indicadores econômicos do Brasil, com foco em
macroeconomia. Os dados são organizados em seis blocos analíticos: política
monetária, atividade econômica, crédito, mercado de trabalho, setor público e
comércio exterior.

## Status

🚧 **Em construção** — v0.3 (dados separados em JSON, renderizados via JavaScript)

## O que já existe

- ✅ **v0.1** — Home inicial publicada
- ✅ **v0.2** — Painel com 16 cards distribuídos em 6 seções temáticas
- ✅ **v0.3** — Arquitetura orientada a dados:
  - Indicadores separados em `dados.json` (dados ≠ apresentação)
  - JavaScript carrega o JSON e gera os cards dinamicamente
  - Editar um valor exige mudar **apenas** o `dados.json`
  - Formatação de números no padrão brasileiro (`toLocaleString("pt-BR")`)
  - Seções identificadas por slugs (`politica-monetaria`, `atividade`, etc.)

⚠️ **Os valores exibidos são fictícios**, apenas para desenvolvimento. As
versões seguintes integrarão dados reais de fontes oficiais.

## Roadmap

- [x] **v0.1** — Estrutura inicial e home publicada
- [x] **v0.2** — Layout em grid de cards por indicador, com seções temáticas
- [x] **v0.3** — Dados manuais via JSON, renderizados dinamicamente
- [ ] **v0.4** — Integração com APIs oficiais:
  - Banco Central (SGS) — Selic, IPCA, câmbio, crédito
  - IBGE (SIDRA) — PIB, desemprego, PEA, consumo
  - Tesouro Nacional — gasto público, resultado primário
  - Comex Stat (MDIC) — exportações, importações, saldo
- [ ] **v0.5** — Gráficos de séries históricas (Chart.js)
- [ ] **v0.6** — Treemap de parceiros comerciais (principais países compradores/vendedores)
- [ ] **v1.0** — Detalhamento de gasto público e orçamento (livre vs. vinculado)

## Fontes de dados planejadas

| Indicador | Fonte | Código/Série |
|---|---|---|
| Taxa Selic | BCB SGS | 432 |
| IPCA (12 meses) | BCB SGS | 13522 |
| Câmbio (USD/BRL) | BCB SGS | 1 |
| PIB | IBGE SIDRA | — |
| Desemprego / PEA | IBGE PNAD Contínua | — |
| Crédito / Endividamento | BCB | — |
| Gasto Público / Resultado Primário | Tesouro Nacional | — |
| Exportações / Importações | Comex Stat (MDIC) | — |

## Tecnologias

**Atuais:**
- HTML5 (estrutura semântica)
- CSS3 (variáveis, flexbox, grid, responsividade)
- JavaScript (fetch, async/await, manipulação de DOM)
- JSON (formato de dados)
- Git e GitHub Pages

**Futuras:**
- Python + Anaconda (coleta e tratamento de dados)
- JavaScript + Chart.js (visualizações)

## Estrutura do projeto

```
painel-economico-brasil/
├── index.html      # Estrutura da página (esqueleto, sem cards hard-coded)
├── style.css       # Estilos e design tokens
├── script.js       # Lógica: carrega JSON e renderiza cards
├── dados.json      # Dados dos indicadores (única fonte de verdade)
├── README.md       # Este arquivo
└── .gitignore      # Arquivos ignorados pelo Git
```

### Fluxo de dados

```
dados.json  ──fetch──▶  script.js  ──DOM──▶  index.html (renderizado)
  (dados)                (lógica)              (apresentação)
```

## Autor

**Rafael Penha** — estudante de Economia
GitHub: [@rafaelcpenha](https://github.com/rafaelcpenha)

## Licença

Projeto de estudo. Código aberto para fins educacionais.
