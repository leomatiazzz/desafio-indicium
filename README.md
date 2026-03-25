# Desafio Indicium — LH Nautical

## Contexto do desafio
Este projeto simula o cenário da **LH Nautical**, varejista de peças e acessórios para embarcações (loja física + e-commerce), que enfrenta um "caos dos dados": bases sujas, processos desconectados e baixa confiabilidade para tomada de decisão.

O objetivo foi responder às questões do desafio cobrindo:
- EDA
- Tratamento de dados
- Análise de vendas
- Análise de clientes
- Previsão de demanda
- Sistema de recomendações

## Entregáveis principais
1. `apresentacao_desafio_indicium.ipynb`
   - Notebook com narrativa executiva, KPIs, análises por questão e visuais complementares.

2. `app_desafio_indicium.py`
   - Dashboard Streamlit com filtros, KPIs, evolução de faturamento, top produtos, recomendação e visuais de Q4/Q5/Q6.

## Deploy
- No streamlit: https://desafio-indicium-2026.streamlit.app/
- No render: https://desafio-indicium.onrender.com/

## Documentação
- [Índice da documentação](docs/INDICE_DOCUMENTACAO.md)
- [Dicionário de dados](docs/DICIONARIO_DADOS.md)
- [Metodologia analítica](docs/METODOLOGIA_ANALITICA.md)
- [Guia DBeaver + SQLite](docs/GUIA_DBEAVER_SQLITE.md)

## Como executar

### Instalação (projeto completo)
```bash
pip install -r requirements.txt
```

### Notebook
Abra e execute `apresentacao_desafio_indicium.ipynb` no VS Code/Jupyter.

### Streamlit
```bash
pip install -r requirements.txt
streamlit run app_desafio_indicium.py
```

## Fontes de dados utilizadas
- `datasets/vendas_2023_2024.csv` (fonte canônica de vendas)
- `datasets/produtos_raw.csv`
- `datasets/clientes_crm.json`
- `features/custos_importacao_normalizado.csv`
- `features/cambio.csv`

Fallback técnico:
- `features/vendas_normalizado.csv` apenas se o bruto não estiver disponível.

## Observações analíticas
- Recomendação: filtragem colaborativa item-item (similaridade cosseno em matriz binária usuário-item).
- Previsão: baseline para demanda, passível de evolução para métodos de demanda intermitente.
- Margem/prejuízo: estimados via custo em USD vigente por produto + taxa de câmbio por data de venda.
