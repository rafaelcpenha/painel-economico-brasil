# Painel Econômico Brasil

Painel web com os principais indicadores econômicos do Brasil, com foco em
macroeconomia. Os dados são organizados em seis blocos analíticos: política
monetária, atividade econômica, crédito, mercado de trabalho, setor público e
comércio exterior.

## Status

🚧 **Em construção** — v0.2 (painel com 16 cards organizados em 6 seções)

## O que já existe

- ✅ **v0.1** — Home inicial publicada
- ✅ **v0.2** — Painel com 16 cards de indicadores distribuídos em 6 seções:
  - Política Monetária e Preços (Selic, IPCA, Câmbio)
  - Atividade Econômica (PIB demanda, PIB oferta, Investimento, Consumo)
  - Crédito e Endividamento (Crédito Total, Endividamento das Famílias)
  - Mercado de Trabalho (Desemprego, PEA)
  - Setor Público (Gasto Público, Resultado Primário)
  - Comércio Exterior (Exportações, Importações, Saldo Comercial)

⚠️ **Os valores exibidos são fictícios**, apenas para desenvolvimento do layout.
As versões seguintes integrarão dados reais de fontes oficiais.

## Roadmap

- [x] **v0.1** — Estrutura inicial e home publicada
- [x] **v0.2** — Layout em grid de cards por indicador, com seções temáticas
- [ ] **v0.3** — Dados manuais via JSON
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
- Git e GitHub Pages

**Futuras:**
- Python + Anaconda (coleta e tratamento de dados)
- JavaScript + Chart.js (visualizações)

## Estrutura do projeto

```
painel-economico-brasil/
├── index.html      # Página principal com os cards
├── style.css       # Estilos e design tokens
├── README.md       # Este arquivo
└── .gitignore      # Arquivos ignorados pelo Git
```

## Autor

**Rafael Penha** — estudante de Economia
GitHub: [@rafaelcpenha](https://github.com/rafaelcpenha)

## Licença

Projeto de estudo. Código aberto para fins educacionais.
