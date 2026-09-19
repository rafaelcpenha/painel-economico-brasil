# Módulo Python — Painel Econômico Brasil

Este diretório contém o código Python responsável por **coletar, tratar e
gerar** o arquivo `data/dados.json` que o site consome.

## Estrutura
```
python/
├── notebooks/ # Exploração interativa (Jupyter)
├── scripts/
│ ├── coletores/ # Um módulo por fonte de dados
│ │ ├── init.py
│ │ ├── bcb.py # (a criar) Banco Central — SGS
│ │ ├── ibge.py # (a criar) IBGE — SIDRA / PNAD
│ │ ├── tesouro.py # (a criar) Tesouro Nacional
│ │ └── comex.py # (a criar) Comex Stat — MDIC
│ ├── gerar_dados.py # (a criar) Script principal
│ └── utils.py # (a criar) Funções auxiliares
└── README.md # Este arquivo
```
## Ambiente

O código Python deste projeto requer o ambiente Conda `painel-economico-brasil`.

Para ativar:

```
conda activate painel-economico-brasil
```
Bibliotecas instaladas: requests, pandas, jupyter.


Como rodar (futuro)

```
python python/scripts/gerar_dados.py
```
Isso gera/atualiza data/dados.json com dados reais das APIs oficiais.


---

## 3. Rodar tudo de novo para confirmar

Depois das mudanças, verifique:

**Passo A — Testar o site no Live Server:**
- Os 16 cards continuam carregando?
- O console do DevTools não tem erro?

Se sim, o `fetch("data/dados.json")` está correto.

**Passo B — Confirmar o estado do Git:**

```
git status
```
